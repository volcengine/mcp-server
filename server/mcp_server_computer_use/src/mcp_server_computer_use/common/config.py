log_config = {
    "level": "INFO",
    "file": "/tmp/computer_use.log",
    "max_size": 1024000,
    "backup_count": 10,
}

tool_server_config = {
    "local": True,
    "endpoint": "",
    # Optional shared secret. When tool_server is configured with a non-empty
    # `auth_key`, clients must send the same value via the `X-API-Key` header.
    # Can be overridden by the AUTH_API_KEY environment variable.
    "auth_key": "",
}

# Optional HTTPS settings. When tool_server is served over HTTPS, set
# `enable_https` to True and provide `client_ca` (the CA certificate path that
# signs tool_server's server certificate) so the SDK can validate the TLS
# server certificate. Both can be overridden by environment variables:
#   - TOOL_SERVER_ENABLE_HTTPS = "true" / "false"
#   - TOOL_SERVER_CLIENT_CA    = "/absolute/path/to/ca.crt"
plugins_config = {
    "enable_https": False,
}

ssl_config = {
    "client_ca": "",
}