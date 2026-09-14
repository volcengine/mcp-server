"""Encrypted shared drafts and durable mutation deduplication.

PostgreSQL is supported for replicas. SQLite is useful for a single local process.
No credentials or form fields are stored in plaintext.
"""

import hashlib
import json
import secrets
import threading
import time
import uuid
from contextlib import contextmanager

from cryptography.fernet import Fernet
from sqlalchemy import (
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    delete,
    insert,
    select,
    update,
)
from sqlalchemy.exc import IntegrityError


class StoreError(ValueError):
    pass


metadata = MetaData()
records = Table(
    "sms_mcp_records",
    metadata,
    Column("id", String(64), primary_key=True),
    Column("owner", String(64), nullable=False),
    Column("kind", String(32), nullable=False),
    Column("status", String(32), nullable=False),
    Column("data", Text, nullable=False),
    Column("expires", Float, nullable=False, index=True),
    Column("revision", Integer, nullable=False, default=0),
    Column("lease", String(64)),
    Column("lease_until", Float, nullable=False, default=0),
)


class Store:
    def __init__(self, database_url: str, encryption_key: str):
        self.engine = create_engine(database_url, pool_pre_ping=True)
        self.cipher = Fernet(encryption_key.encode())
        metadata.create_all(self.engine)

    def _encode(self, value):
        return self.cipher.encrypt(
            json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode()
        ).decode()

    def _decode(self, value):
        return json.loads(self.cipher.decrypt(value.encode()))

    @staticmethod
    def _owner(owner):
        return hashlib.sha256(owner.encode()).hexdigest()

    def create(self, owner, kind, data, ttl, *, status="ready", record_id=None):
        record_id = record_id or uuid.uuid4().hex
        with self.engine.begin() as connection:
            connection.execute(
                insert(records).values(
                    id=record_id,
                    owner=self._owner(owner),
                    kind=kind,
                    status=status,
                    data=self._encode(data),
                    expires=time.time() + ttl,
                    revision=0,
                    lease_until=0,
                )
            )
        return record_id

    def get(self, record_id, owner, kind):
        with self.engine.connect() as connection:
            row = (
                connection.execute(
                    select(records).where(
                        records.c.id == record_id,
                        records.c.owner == self._owner(owner),
                        records.c.kind == kind,
                        records.c.expires > time.time(),
                    )
                )
                .mappings()
                .first()
            )
        if row is None:
            raise StoreError("记录不存在、已过期或不属于当前用户")
        result = dict(row)
        result["data"] = self._decode(row["data"])
        return result

    def save(self, record_id, owner, data, *, lease, status="ready"):
        with self.engine.begin() as connection:
            result = connection.execute(
                update(records)
                .where(
                    records.c.id == record_id,
                    records.c.owner == self._owner(owner),
                    records.c.lease == lease,
                    records.c.expires > time.time(),
                    records.c.lease_until > time.time(),
                )
                .values(
                    data=self._encode(data),
                    status=status,
                    revision=records.c.revision + 1,
                )
            )
            if result.rowcount != 1:
                raise StoreError("流程已过期或执行权已变化，请查询最新状态")

    @contextmanager
    def locked(self, record_id, owner, kind):
        token, stop = secrets.token_hex(16), threading.Event()
        with self.engine.begin() as connection:
            result = connection.execute(
                update(records)
                .where(
                    records.c.id == record_id,
                    records.c.owner == self._owner(owner),
                    records.c.kind == kind,
                    records.c.expires > time.time(),
                    records.c.lease_until < time.time(),
                )
                .values(lease=token, lease_until=time.time() + 120)
            )
            if result.rowcount != 1:
                raise StoreError("流程不可用或正在处理另一项操作，请稍后查询")

        def renew():
            while not stop.wait(30):
                try:
                    with self.engine.begin() as connection:
                        result = connection.execute(
                            update(records)
                            .where(
                                records.c.id == record_id,
                                records.c.lease == token,
                            )
                            .values(lease_until=time.time() + 120)
                        )
                        if result.rowcount != 1:
                            return
                except Exception:
                    return  # save() rejects a lost lease; mutations have a separate durable guard.

        worker = threading.Thread(target=renew, daemon=True)
        worker.start()
        try:
            yield self.get(record_id, owner, kind), token
        finally:
            stop.set()
            worker.join(timeout=2)
            with self.engine.begin() as connection:
                connection.execute(
                    update(records)
                    .where(records.c.id == record_id, records.c.lease == token)
                    .values(lease=None, lease_until=0)
                )

    def once(self, owner, operation_id, payload, ttl, call):
        digest = hashlib.sha256(
            json.dumps(
                payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
            ).encode()
        ).hexdigest()
        record_id = uuid.uuid5(uuid.NAMESPACE_URL, owner + ":" + operation_id).hex
        try:
            self.create(
                owner,
                "mutation",
                {"digest": digest},
                ttl,
                status="executing",
                record_id=record_id,
            )
        except IntegrityError:
            previous = self.get(record_id, owner, "mutation")
            if previous["data"]["digest"] != digest:
                raise StoreError("同一次操作的内容发生变化")
            if previous["status"] == "completed":
                return previous["data"]["result"]
            return {
                "success": False,
                "error": {
                    "code": "outcome_unknown",
                    "outcome_unknown": True,
                    "message": "该请求已开始处理，请查询结果，不要重复提交",
                },
            }
        try:
            result = call()
        except Exception:
            result = {
                "success": False,
                "error": {
                    "code": "outcome_unknown",
                    "outcome_unknown": True,
                    "message": "请求结果暂时无法确认，请查询结果，不要重复提交",
                },
            }
        with self.engine.begin() as connection:
            connection.execute(
                update(records)
                .where(records.c.id == record_id)
                .values(
                    status="completed",
                    data=self._encode({"digest": digest, "result": result}),
                )
            )
        return result

    def operation(self, owner, operation_id):
        record_id = uuid.uuid5(uuid.NAMESPACE_URL, owner + ":" + operation_id).hex
        try:
            return self.get(record_id, owner, "mutation")
        except StoreError:
            return None

    def cleanup(self):
        with self.engine.begin() as connection:
            connection.execute(
                delete(records).where(
                    records.c.expires <= time.time(),
                    records.c.lease_until < time.time(),
                )
            )

    def delete_file(self, file_id, owner):
        with self.engine.begin() as connection:
            connection.execute(
                delete(records).where(
                    records.c.id == file_id,
                    records.c.owner == self._owner(owner),
                    records.c.kind == "file",
                )
            )
