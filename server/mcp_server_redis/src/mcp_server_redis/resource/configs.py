redis_supported_regions = ["cn-guilin-boe"]
vpc_supported_regions = ["cn-guilin-boe"]

def get_redis_service_endpoint_by_region(region_id: str = None) -> str:
    return "volcengineapi-boe-stable.byted.org"

def get_vpc_service_endpoint_by_region(region_id: str = None) -> str:
    return "volcengineapi-boe-stable.byted.org"
