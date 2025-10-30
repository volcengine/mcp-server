from os import environ


VOLCENGINE_ACCESS_KEY_ENV = 'VOLCENGINE_ACCESS_KEY'
VOLCENGINE_SECRET_KEY_ENV = 'VOLCENGINE_SECRET_KEY'
VOLCENGINE_SESSION_TOKEN_ENV = 'VOLCENGINE_SESSION_TOKEN'
VOLCENGINE_REGION_ENV = 'VOLCENGINE_REGION'
VOLCENGINE_HOST_ENV = 'VOLCENGINE_ENDPOINT'


def get_volcengine_credentials():
    """Get Volcengine credentials from environment variables."""
    return {
        'access_key_id': environ.get(VOLCENGINE_ACCESS_KEY_ENV, ''),
        'secret_access_key': environ.get(VOLCENGINE_SECRET_KEY_ENV, ''),
        'session_token': environ.get(VOLCENGINE_SESSION_TOKEN_ENV, ''),
        'region': environ.get(VOLCENGINE_REGION_ENV) or 'cn-beijing',
        'host': environ.get(VOLCENGINE_HOST_ENV) or 'cloudcontrol.cn-beijing.volcengineapi.com',
    }
