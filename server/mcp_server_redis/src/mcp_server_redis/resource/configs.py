redis_supported_regions = ["cn-beijing", "cn-guangzhou", "cn-shanghai", "cn-hongkong", "ap-southeast-1", "ap-southeast-3"]
vpc_supported_regions = ["cn-beijing", "cn-guangzhou", "cn-shanghai", "cn-hongkong", "ap-southeast-1", "ap-southeast-3"]

def get_redis_service_endpoint_by_region(region_id: str = None) -> str:
    return f"redis.{region_id}.volcengineapi.com"

def get_vpc_service_endpoint_by_region(region_id: str = None) -> str:
    return f"vpc.{region_id}.volcengineapi.com"
