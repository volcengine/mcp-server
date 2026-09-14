import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest
from sqlalchemy import select, update

from mcp_server_sms.store import Store, StoreError, records


def test_shared_encrypted_draft_survives_new_runtime(settings, owner):
    first = Store(settings.database_url, settings.encryption_key)
    draft = first.create(owner, "form", {"secret": "fixture-private-data"}, 300)
    second = Store(settings.database_url, settings.encryption_key)
    assert second.get(draft, owner, "form")["data"]["secret"] == "fixture-private-data"
    with first.engine.connect() as connection:
        serialized = str(connection.execute(select(records)).all())
    assert "fixture-private-data" not in serialized
    assert owner not in serialized
    with pytest.raises(StoreError):
        second.get(draft, "another-owner", "form")
    with pytest.raises(StoreError):
        second.get(draft, owner, "file")


def test_mutation_deduplicates_across_instances(settings, owner):
    a = Store(settings.database_url, settings.encryption_key)
    b = Store(settings.database_url, settings.encryption_key)
    started, finish = threading.Event(), threading.Event()
    calls = []

    def send():
        calls.append(1)
        started.set()
        assert finish.wait(5)
        return {"success": True, "result": {"messageId": "one"}}

    with ThreadPoolExecutor(2) as pool:
        pending = pool.submit(
            a.once, owner, "send-one", {"message": "fixture"}, 300, send
        )
        assert started.wait(5)
        result = b.once(owner, "send-one", {"message": "fixture"}, 300, send)
        assert result["error"]["outcome_unknown"] is True
        finish.set()
        assert pending.result()["success"] is True
    assert (
        b.once(owner, "send-one", {"message": "fixture"}, 300, send)["success"] is True
    )
    assert calls == [1]
    with pytest.raises(StoreError):
        b.once(owner, "send-one", {"message": "changed"}, 300, send)


def test_unknown_mutation_is_never_automatically_replayed(runtime, owner):
    calls = []

    def send():
        calls.append(1)
        raise TimeoutError("may have reached SMS")

    for _ in range(2):
        assert runtime.store.once(owner, "unknown", {}, 300, send)["error"][
            "outcome_unknown"
        ]
    assert calls == [1]


def test_expiration_and_lost_lease_fail_closed(runtime, owner):
    draft = runtime.store.create(owner, "form", {"value": 1}, 300)
    with runtime.store.locked(draft, owner, "form") as (record, lease):
        with pytest.raises(StoreError):
            runtime.store.save(draft, owner, {"value": 2}, lease="wrong-lease")
        runtime.store.save(draft, owner, {"value": 3}, lease=lease)
    with runtime.store.engine.begin() as connection:
        connection.execute(
            update(records).where(records.c.id == draft).values(expires=time.time() - 1)
        )
    with pytest.raises(StoreError):
        runtime.store.get(draft, owner, "form")
    runtime.store.cleanup()
    with runtime.store.engine.connect() as connection:
        assert connection.execute(select(records)).all() == []
