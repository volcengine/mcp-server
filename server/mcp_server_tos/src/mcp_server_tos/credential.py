from dataclasses import dataclass


@dataclass
class Credential:
    access_key: str
    secret_key: str
    security_token: str
    expired_time: str
