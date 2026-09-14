import base64
import json
import time
from types import SimpleNamespace

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from mcp_server_sms.auth import (
    AuthenticationError,
    Authenticator,
    sms_credentials,
    subject_identity,
)


def test_jwt_signature_issuer_audience_expiry_and_subject(settings):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    verifier = Authenticator(settings)
    verifier._keys = SimpleNamespace(
        get_signing_key_from_jwt=lambda token: SimpleNamespace(key=key.public_key())
    )
    claims = {
        "iss": settings.oidc_issuer,
        "aud": settings.token_audience,
        "sub": "one",
        "exp": time.time() + 300,
    }
    for sub in ["one", "two"]:
        token = jwt.encode({**claims, "sub": sub}, key, algorithm="RS256")
        assert verifier.owner({"authorization": "Bearer " + token}) == subject_identity(
            settings.oidc_issuer, sub
        )
    for overrides in [
        {"aud": "another-resource"},
        {"iss": "https://foreign.example"},
        {"exp": 1},
        {"sub": ""},
    ]:
        token = jwt.encode({**claims, **overrides}, key, algorithm="RS256")
        with pytest.raises(AuthenticationError):
            verifier.owner({"authorization": "Bearer " + token})
    other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with pytest.raises(AuthenticationError):
        verifier.owner(
            {"authorization": "Bearer " + jwt.encode(claims, other, algorithm="RS256")}
        )


def test_http_credentials_never_fall_back_to_process_identity(monkeypatch):
    monkeypatch.setenv("VOLCENGINE_ACCESS_KEY", "server-identity")
    monkeypatch.setenv("VOLCENGINE_SECRET_KEY", "server-secret")
    with pytest.raises(AuthenticationError):
        sms_credentials({})
    first = {
        "AccessKeyId": "caller-one",
        "SecretAccessKey": "secret-one",
        "SessionToken": "sts-one",
    }
    second = {"AccessKeyId": "caller-two", "SecretAccessKey": "secret-two"}

    def load(value):
        return sms_credentials(
            {
                "x-volcengine-credentials": base64.b64encode(
                    json.dumps(value).encode()
                ).decode()
            }
        )

    assert load(first).access_key == "caller-one"
    assert load(second).access_key == "caller-two"
    assert "secret-one" not in repr(load(first))
