"""Pluggable authentication for the OpenViking control plane.

The control-plane TopAPI is served by the OpenViking data-plane cluster and
authenticated with an Ark AgentPlan ApiKey, replayed as an
``Authorization: Bearer <key>`` header on every request (``BearerTokenAuth``).
The ``AuthProvider`` protocol leaves room to plug in a different provider later
(e.g. AK/SK signing) without touching ``client.py`` or the tool/CLI layers.
"""

from typing import Dict, Protocol


class AuthProvider(Protocol):
    """Produces the auth/identity headers for a single control-plane request."""

    def auth_headers(
        self, method: str, path: str, query: Dict[str, str], body_str: str
    ) -> Dict[str, str]:
        ...


class BearerTokenAuth:
    """Authenticate with an Ark AgentPlan ApiKey via ``Authorization: Bearer``.

    The backend's control-plane auth (``authorizeControlPlaneByArk``) reads the
    key only from the ``Authorization: Bearer`` header — it does not accept
    ``X-API-Key``. The token is replayed verbatim on every request, independent
    of method/path/body. A token passed with or without the ``Bearer `` prefix
    is tolerated.
    """

    def __init__(self, token: str):
        token = (token or "").strip()
        if token.lower().startswith("bearer "):
            token = token[len("bearer "):].strip()
        self._token = token

    def auth_headers(
        self, method: str, path: str, query: Dict[str, str], body_str: str
    ) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self._token}"}
