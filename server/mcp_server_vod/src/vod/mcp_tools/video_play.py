
from src.vod.api.api import VodAPI
from mcp.server.fastmcp import FastMCP

from typing import Any, Dict
from datetime import datetime, timezone, timedelta
import hashlib
from urllib.parse import quote
import secrets
import json
import re

def register_video_play_methods(service: VodAPI, public_methods: dict,):
    def str_to_number(s, default=None):
        if not isinstance(s, str):
            print(f"警告：输入不是字符串（类型：{type(s)}）")
            return default
        
        # Preprocessing: Remove leading and trailing spaces and commas.
        s_clean = s.strip().replace(",", "")
        
        # Regular expression to match pure integers (supporting positive and negative signs, such as "123", "-456")
        int_pattern = re.fullmatch(r"[+-]?\d+", s_clean)
        if int_pattern:
            return int(s_clean)
        
        # Regular expression matching for floating-point numbers (supports decimals, scientific notation, such as "3.14", "1.2e3", "-5.6")
        float_pattern = re.fullmatch(r"[+-]?\d+\.?\d*([eE][+-]?\d+)?", s_clean)
        if float_pattern:
            return float(s_clean)
        
        # match failed
        print(f"警告：'{s}' 无法转换为数字")
        return default
    def _random_string(length: int) -> str:
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def _encode_path_str(s: str = "") -> str:
        return quote(s, safe="-_.~$&+,/:;=@")

    def _encode_rfc3986_uri_component(s: str) -> str:
        return quote(s, safe=":/?&=%-_.~")

    def _parse_time(value: Any):
        if isinstance(value, (int, float)):
            try:
                return datetime.fromtimestamp(float(value), tz=timezone.utc)
            except Exception:
                return None
        if isinstance(value, str):
            try:
                v = value.replace("Z", "+00:00") if "Z" in value else value
                return datetime.fromisoformat(v)
            except Exception:
                return None
        return None

    def _is_https_available(certificate: Dict[str, Any]) -> bool:
        if certificate and certificate.get("HttpsStatus") == "enable":
            exp = _parse_time(certificate.get("ExpiredAt"))
            if exp:
                return exp > datetime.now(timezone.utc)
        return False


    def _get_Domain_config(domain: str, spaceName: str, domain_type: str = "play"):
        detail = service.mcp_get(
                "McpDescribeDomainConfig",
                {"SpaceName": spaceName, "Domain": domain, "DomainType": domain_type},
            )
        auth_info = {}
        if isinstance(detail, str):
            detail = json.loads(detail)
            result = detail.get("Result", {})
            cdn_config = result.get("Config") or {}
            signed_url_auth_control = cdn_config.get("SignedUrlAuthControl") or {}
            signed_url_auth_rules = signed_url_auth_control.get('SignedUrlAuth',{}).get("SignedUrlAuthRules",[])
            signed_url_auth_action = {}
            if len(signed_url_auth_rules) > 0:
                signed_url_auth_action = signed_url_auth_rules[0].get("SignedUrlAuthAction", {})
            base_domain = result.get("Domain",'')
            status = ''
            if base_domain.get("ConfigStatus") == 'online':
                status = 'enable'
            else:
                status = base_domain.get("ConfigStatus") 
            auth_info = {
                "AuthType": signed_url_auth_action.get("URLAuthType"),
                "AuthKey": signed_url_auth_action.get("MasterSecretKey") or signed_url_auth_action.get("BackupSecretKey") or "",
                "Status": status,
                "Domain": base_domain.get("Domain",''),
            }
        return auth_info

    def _get_available_domain(spaceName: str):
        state = service.get_state()
        # if have cache, use cache data
        available_domains_list = state.get("available_domains",{}).get(spaceName) or []
        if available_domains_list:
            return available_domains_list
        
        offset = 0
        total = 1
        domain_list: list[Dict[str, Any]] = []
        while offset < total:
            data = service.mcp_get(
                "McpListDomain",
                {"SpaceName": spaceName, "SourceStationType": 1, "DomainType": "play", "Offset": offset},
            )
            if isinstance(data, str):
                data = json.loads(data)
                offset = int(data.get("Offset", 0))
                total = int(data.get("Total", 0))
                result = data.get("Result", {})
                instances = ((result.get("PlayInstanceInfo") or {}).get("ByteInstances") or [])
                for item in instances:
                    domains = item.get("Domains") or []
                    for domain in domains:
                        d = dict(domain)
                        d["SourceStationType"] = 1
                        d["DomainType"] = "play"
                        domain_list.append(d)
        domain_list = [d for d in domain_list if d.get("CdnStatus") == "enable"]
        enriched = []
        for d in domain_list:
            auth_info = _get_Domain_config(d.get("Domain"), spaceName, d.get("DomainType"))
            d2 = dict(d)
            d2["AuthInfo"] = auth_info
            enriched.append(d2)
        
        available = [d for d in enriched if (not d.get("AuthInfo")) or ((d.get("AuthInfo") or {}).get("AuthType") == "typea")]
        service.set_state({"available_domains":{
            spaceName: available
        }})
        return available

    def _gen_url(spaceName: str,domainObj: Dict[str, Any], path: str, expired_minutes: int) -> str:
        # get available domain list
        available_domains_list = _get_available_domain(spaceName)
        domainLen = len(available_domains_list)
        if domainLen > 0:
             domainObj = available_domains_list[0]
        is_https = _is_https_available(domainObj.get("Certificate"))
        fileName = f"/{path}"
        if ((domainObj.get("AuthInfo") or {}).get("AuthType") == "typea"):
            expire_ts = int((datetime.now(timezone.utc) + timedelta(minutes=expired_minutes)).timestamp())
            randStr = _random_string(16)
            key = (domainObj.get("AuthInfo") or {}).get("AuthKey") or ""
            md5_input = f"{_encode_path_str(fileName)}-{expire_ts}-{randStr}-0-{key}".encode("utf-8")
            md5Str = hashlib.md5(md5_input).hexdigest()
            url = f"{'https' if is_https else 'http'}://{domainObj.get('Domain')}{fileName}?auth_key={expire_ts}-{randStr}-0-{md5Str}"
            return _encode_rfc3986_uri_component(url)
        else:
            url = f"{'https' if is_https else 'http'}://{domainObj.get('Domain')}{fileName}"
            return _encode_rfc3986_uri_component(url)

    def _gen_wild_url(storageConfig: Dict[str, Any], fileName: str) -> str:
        filePath = f"/{fileName}"
        conf = storageConfig.get("StorageUrlAuthConfig") or {}
        if storageConfig.get("StorageType") == "volc" and conf.get("Type") == "cdn_typea" and conf.get("Status") == "enable":
            typeA = conf.get("TypeAConfig") or {}
            expire_ts = int((datetime.now(timezone.utc) + timedelta(seconds=str_to_number(typeA.get("ExpireTime") or 0))).timestamp())
            randStr = _random_string(16)
            key = typeA.get("MasterKey") or typeA.get("BackupKey") or ""
            md5_input = f"{_encode_path_str(filePath)}-{expire_ts}-{randStr}-0-{key}".encode("utf-8")
            md5Str = hashlib.md5(md5_input).hexdigest()
            sig_arg = typeA.get("SignatureArgs") or "auth_key"
            signed = f"{storageConfig.get('StorageHost')}{filePath}?{sig_arg}={expire_ts}-{randStr}-0-{md5Str}&preview=1"
            return _encode_rfc3986_uri_component(signed)
        elif storageConfig.get("StorageType") == "volc" and conf.get("Status") == "disable":
            signed = f"{storageConfig.get('StorageHost')}{filePath}?preview=1"
            return _encode_rfc3986_uri_component(signed)
        return ""

    def get_storage_config(spaceName: str) -> Dict[str, Any]:
        state = service.get_state()
        # if have cache, use cache data
        storage_config_cache = state.get("storage_config",{}).get(spaceName) or {}
        if storage_config_cache:
            return storage_config_cache
        reqs = service.mcp_get(
                "McpGetStorageConfig",
                {"SpaceName": spaceName},
            )

        if isinstance(reqs, str):
            reqs = json.loads(reqs)
            storageConfig = reqs.get("Result") or {}
            service.set_state({"storage_config":{
                spaceName: storageConfig
            }})
        return storageConfig or {}
  
  
    def get_play_directurl(spaceName: str, fileName: str, expired_minutes: int = 60) -> str:
        """
        获取播放地址
        Args:
            - spaceName: **必选字段** 空间名称
            - fileName: **必选字段** 文件名
            - expired_minutes: **可选字段** 过期时间，默认60分钟
        Returns:
            - 播放地址
        """
        available_domains_list = _get_available_domain(spaceName)
        domainLen = len(available_domains_list)
        urlPath = ''
        # if have available domain, use first domain
        if domainLen > 0:
            domainObj = available_domains_list[0]
            urlPath = _gen_url(spaceName, domainObj,fileName, expired_minutes)
        else:
            # if no available domain, use wild url
            storageConfig = get_storage_config(spaceName)
            urlPath = _gen_wild_url(storageConfig, fileName)
        return urlPath
    public_methods["get_play_url"] = get_play_directurl


def create_mcp_server(mcp: FastMCP, public_methods: dict, service: VodAPI):
    @mcp.tool()
    def get_play_url(spaceName: str, fileName: str, expired_minutes: int = 60) -> str:
        """
        Obtain the video playback link through `fileName`
        Args:
            - spaceName: **必选字段** 空间名称
            - fileName: **必选字段** 文件名
            - expired_minutes: **可选字段** 过期时间，默认60分钟
        Returns:
            - 播放地址
        """
        return public_methods["get_play_url"](spaceName, fileName, expired_minutes)

       
