"""Run against a disposable CI database, in an isolated schema per test."""

import os
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.schema import CreateSchema, DropSchema

from mcp_server_sms.store import Store


@pytest.fixture
def postgres_url():
    value = os.environ.get("SMS_MCP_TEST_DATABASE_URL")
    if not value:
        pytest.skip("No dedicated PostgreSQL test database configured")
    engine = create_engine(value)
    schema = "sms_mcp_test_" + uuid.uuid4().hex
    with engine.begin() as connection:
        connection.execute(CreateSchema(schema))
    url = make_url(value).update_query_dict({"options": "-csearch_path=" + schema})
    try:
        yield url
    finally:
        with engine.begin() as connection:
            connection.execute(DropSchema(schema, cascade=True))
        engine.dispose()


def test_postgresql_shared_draft_and_mutation_guard(postgres_url, settings, owner):
    first = Store(postgres_url, settings.encryption_key)
    second = Store(postgres_url, settings.encryption_key)
    try:
        flow = first.create(owner, "form", {"revision": 1}, 300)
        with second.locked(flow, owner, "form") as (record, lease):
            first.save(flow, owner, {"revision": 2}, lease=lease)
        assert second.get(flow, owner, "form")["data"]["revision"] == 2
        calls = []

        def submit():
            calls.append(1)
            return {"success": True}

        first.once(owner, "pg-submit", {}, 300, submit)
        assert second.once(owner, "pg-submit", {}, 300, submit)["success"]
        assert calls == [1]
    finally:
        first.engine.dispose()
        second.engine.dispose()
