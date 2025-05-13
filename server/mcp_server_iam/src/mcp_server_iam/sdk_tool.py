from volcenginesdkcore import UniversalApi, UniversalInfo, ApiClient, Configuration


def create_universal_info(service, action, version='2021-09-01', method='POST', content_type='application/json'):
    if content_type is None:
        content_type = 'application/json'
    if method == "GET":
        content_type = "text/plain"

    return UniversalInfo(
        method=method,
        service=service,
        version=version,
        action=action,
        content_type=content_type
    )


def create_api_client(ak, sk, session_token='', region='cn-beijing', host='open.volcengineapi.com', scheme='https'):
    config = Configuration()
    config.ak = ak
    config.sk = sk
    config.host = host
    config.scheme = scheme
    config.region = region
    if session_token:
        config.session_token = session_token

    return UniversalApi(ApiClient(config))


# 使用示例
if __name__ == "__main__":
    # 创建API客户端
    client = create_api_client(ak="AK",
                               sk="SK")

    # 创建UniversalInfo
    info = create_universal_info(service='sts', action='AssumeRole', version='2018-01-01', method='GET',
                                 content_type='')

    # 准备请求参数
    params = {
        'RoleTrn': "trn:iam::2102518066:role/my_role",
        'RoleSessionName': "demo"
    }
    # 调用API
    resp, status_code, resp_header = client.do_call_with_http_info(info=info, body=params)
    print(f"Status Code: {status_code}")
    print(f"Response: {resp}")
