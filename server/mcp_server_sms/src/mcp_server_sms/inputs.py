"""Owned file exchange without putting document bytes in MCP arguments."""

import base64
import hashlib
import json
import os
from pathlib import PurePosixPath
import stat

from .core.qualification_upload import _validated_image_bytes
from .store import StoreError

INPUT_LIMITS = {
    "qualification_image": 2 * 1024 * 1024,
    "qualification_data": 64 * 1024,
    "verification_code": 1024,
    "batch_csv": 50 * 1024 * 1024,
}


class InputFiles:
    def __init__(self, store, ttl, local_root):
        self.store, self.ttl, self.local_root = store, ttl, local_root

    def stage(self, owner, kind, content, content_type):
        maximum = INPUT_LIMITS.get(kind)
        if maximum is None or not content or len(content) > maximum:
            raise StoreError("文件类型不支持或文件大小超出限制")
        if kind == "qualification_image":
            content, content_type = _validated_image_bytes(content, content_type)
        elif kind in ("qualification_data", "verification_code"):
            try:
                value = json.loads(content.decode("utf-8"))
                if not isinstance(value, dict):
                    raise ValueError
                if kind == "verification_code" and (
                    set(value) != {"code"}
                    or not isinstance(value["code"], str)
                    or len(value["code"]) != 4
                    or any(c not in "0123456789" for c in value["code"])
                ):
                    raise ValueError
            except (ValueError, UnicodeError):
                raise StoreError("需要符合文件类型的 JSON 对象") from None
            content_type = "application/json"
        else:
            try:
                content.decode("utf-8-sig")
            except UnicodeError:
                raise StoreError("CSV 必须使用 UTF-8 编码") from None
            content_type = "text/csv"
        file_id = self.store.create(
            owner,
            "file",
            {
                "kind": kind,
                "content": base64.b64encode(content).decode(),
                "content_type": content_type,
            },
            self.ttl,
        )
        return {
            "fileId": file_id,
            "kind": kind,
            "fileSize": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
            "expiresInSeconds": self.ttl,
        }

    def read(self, file_id, owner, kind=None):
        record = self.store.get(file_id, owner, "file")["data"]
        if kind is not None and record["kind"] != kind:
            raise StoreError("文件用途不匹配")
        return base64.b64decode(record["content"]), record["content_type"]

    def document(self, file_id, owner, kind="qualification_data"):
        content, _ = self.read(file_id, owner, kind)
        return json.loads(content)

    def _directory(self, relative_path):
        if not self.local_root:
            raise StoreError("未配置本地材料目录 SMS_MCP_INPUT_ROOT")
        path = PurePosixPath(relative_path)
        if path.is_absolute() or not path.parts or any(p == ".." for p in path.parts):
            raise StoreError("只能使用材料目录内的相对路径")
        descriptor = os.open(
            self.local_root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        )
        try:
            for part in path.parts[:-1]:
                child = os.open(
                    part,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=descriptor,
                )
                os.close(descriptor)
                descriptor = child
            return descriptor, path.name
        except BaseException:
            os.close(descriptor)
            raise

    def import_local(self, relative_path, kind, content_type, owner):
        maximum = INPUT_LIMITS.get(kind)
        if maximum is None:
            raise StoreError("文件类型不支持")
        directory = None
        try:
            directory, name = self._directory(relative_path)
            descriptor = os.open(
                name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory
            )
            with os.fdopen(descriptor, "rb") as source:
                info = os.fstat(source.fileno())
                if not stat.S_ISREG(info.st_mode) or info.st_size > maximum:
                    raise StoreError("需要大小符合限制的普通文件")
                content = source.read(maximum + 1)
        except OSError:
            raise StoreError("无法读取材料文件；不允许符号链接或目录外路径") from None
        finally:
            if directory is not None:
                os.close(directory)
        return self.stage(owner, kind, content, content_type)

    def export_local(self, file_id, relative_path, owner):
        # This destination is explicitly configured by the desktop user. Only
        # derived review data can be exported; raw credentials are never files.
        content, _ = self.read(file_id, owner, "qualification_data")
        directory = None
        try:
            directory, name = self._directory(relative_path)
            descriptor = os.open(
                name,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=directory,
            )
            with os.fdopen(descriptor, "wb") as destination:
                destination.write(content)
        except OSError:
            raise StoreError(
                "无法写入核对文件；目标必须位于材料目录内且尚不存在"
            ) from None
        finally:
            if directory is not None:
                os.close(directory)
        return {"fileId": file_id, "status": "exported_for_customer_review"}
