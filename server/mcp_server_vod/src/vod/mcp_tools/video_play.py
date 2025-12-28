
from src.vod.api.api import VodAPI
from mcp.server.fastmcp import FastMCP

from typing import Any, Dict
from datetime import datetime, timezone, timedelta
import hashlib
from urllib.parse import quote, urlparse, urlencode, parse_qs, urlunparse
import secrets
import json
import re
import urllib.request
import urllib.error
import logging
import inspect



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
            if len(signed_url_auth_rules) == 0:
                return {}            
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

    def get_video_audio_info_directurl(spaceName: str, source: str) -> dict:
        """通过 directurl 模式获取音视频元数据
        Args:
            spaceName: 空间名称
            source: 文件名
        Returns:
            音视频元数据字典
        """
        # 获取播放地址
        playUrl = get_play_directurl(spaceName, source, 60)
        if not playUrl:
            raise Exception("get_video_audio_info: failed to get play url")
        
        # 在链接上拼接 x-vod-process=video/info
        parsed = urlparse(playUrl)
        query_params = parse_qs(parsed.query)
        query_params['x-vod-process'] = ['video/info']
        new_query = urlencode(query_params, doseq=True)
        info_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
        
        # 发起 GET 请求
        try:
            req = urllib.request.Request(info_url)
            with urllib.request.urlopen(req, timeout=30) as response:
                result_data = json.loads(response.read().decode('utf-8'))
        except urllib.error.URLError as e:
            raise Exception(f"get_video_audio_info: failed to fetch video info: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"get_video_audio_info: failed to parse JSON response: {e}")
        
        # 解析结果
        format_info = result_data.get("format", {})
        streams = result_data.get("streams", [])
        
        # 提取视频流信息
        video_stream = None
        audio_stream = None
        for stream in streams:
            codec_type = stream.get("codec_type", "")
            if codec_type == "video" and video_stream is None:
                video_stream = stream
            elif codec_type == "audio" and audio_stream is None:
                audio_stream = stream
        
        # 构建返回结果
        durationValue = format_info.get("duration")
        duration = float(durationValue) if durationValue is not None else 0
        sizeValue = format_info.get("size")
        size = float(sizeValue) if sizeValue is not None else 0
        
        result = {
            "FormatName": format_info.get("format_name", ""),
            "Duration": duration,
            "Size": size,
            "BitRate": format_info.get("bit_rate", ""),
            "CodecName": "",
            "AvgFrameRate": "",
            "Width": 0,
            "Height": 0,
            "Channels": 0,
            "SampleRate": "",
            "BitsPerSample": "",
            "PlayURL": playUrl,
        }
        
        # 填充视频信息
        if video_stream:
            result["CodecName"] = video_stream.get("codec_name", "")
            result["AvgFrameRate"] = video_stream.get("avg_frame_rate", "")
            result["Width"] = int(video_stream.get("width", 0)) if video_stream.get("width") else 0
            result["Height"] = int(video_stream.get("height", 0)) if video_stream.get("height") else 0
            if not result["BitRate"]:
                result["BitRate"] = str(video_stream.get("bit_rate", ""))
        
        # 填充音频信息
        if audio_stream:
            result["Channels"] = int(audio_stream.get("channels", 0)) if audio_stream.get("channels") else 0
            result["SampleRate"] = str(audio_stream.get("sample_rate", ""))
            bits_per_sample = audio_stream.get("bits_per_sample")
            if bits_per_sample:
                result["BitsPerSample"] = str(bits_per_sample)
        
        return result
    
    public_methods["get_video_audio_info_directurl"] = get_video_audio_info_directurl


def create_mcp_server(mcp: FastMCP, public_methods: dict, service: VodAPI):
    @mcp.tool()
    def get_play_url(spaceName: str, fileName: str, expired_minutes: int = 60) -> str:
        """
        Obtain the video playback link through `fileName`， 通过 fileName 获取视频播放地址
        Args:
            - spaceName: **必选字段** 空间名称
            - fileName: **必选字段** 文件名
            - expired_minutes: **可选字段** 过期时间，默认60分钟
        Returns:
            - 播放地址
        """
   
        return public_methods["get_play_url"](spaceName, fileName, expired_minutes)

    @mcp.tool()
    def get_video_audio_info(type: str, source: str, space_name: str) -> dict:
        """Obtaining audio and video metadata， 获取音视频播放信息
        Note:
            - ** directurl 模式：仅支持点播存储 **
            - ** vid 模式：通过 get_play_video_info 获取数据 **
            - ** 不支持 http 模式**
        Args:
            - type(str): ** 必选字段 **，文件类型，默认值为 `vid` 。字段取值如下
                - directurl：仅仅支持点播存储
                - vid
            - source(str): 文件信息
            - space_name(str): ** 必选字段 ** , 点播空间
        Returns:
            - FormatName(str): 容器名称。
            - Duration(float): 时长，单位为秒。
            - Size(float): 大小，单位为字节。
            - BitRate(str): 码率，单位为 bps
            - CodecName(str): 编码器名称。
            - AvgFrameRate(str): 视频平均帧率，单位为 fps。
            - Width(int): 视频宽，单位为 px。
            - Height(int): 视频高，单位为 px。
            - Channels(int): 音频通道数
            - SampleRate(str): 音频采样率，单位 Hz。
            - BitsPerSample(str): 音频采样码率，单位 bit。
            - PlayURL(str): 播放地址
        """
        frame = inspect.currentframe()
        arguments = inspect.getargvalues(frame).locals
        ctx = mcp.get_context()
        raw_request: Request = ctx.request_context.request.headers
        logging.info(f"get_play_url: {space_name} {source} {type}")
        logging.info(f"get_play_url_ctx: {raw_request.get('ak')}")
        logging.info(f"get_play_url_ctx: {raw_request.get('sk')}")
        print(f"get_play_urframe: {arguments}")   

        try:
            params = {"type": type, "source": source, "space_name": space_name}
            if "space_name" not in params:
                raise ValueError("get_video_audio_info: params must contain space_name")
            if not isinstance(params["space_name"], str):
                raise TypeError("get_video_audio_info: params['space_name'] must be a string")
            if not params["space_name"].strip():
                raise ValueError("get_video_audio_info: params['space_name'] cannot be empty")
            if "source" not in params:
                raise ValueError("get_video_audio_info: params must contain source")
            
            sourceType = params.get("type", "vid")
            sourceValue = params.get("source", "")
            
            if sourceType == "directurl":
                # directurl 模式
                result = public_methods["get_video_audio_info_directurl"](params["space_name"], sourceValue)
                return json.dumps(result)
            elif sourceType == "vid":
                # vid 模式 - 直接使用 get_play_video_info 的返回结果
                videoInfo = public_methods["get_play_video_info"](sourceValue, params["space_name"])
                if isinstance(videoInfo, str):
                    videoInfo = json.loads(videoInfo)
                
                durationValue = videoInfo.get("Duration")
                duration = float(durationValue) if durationValue is not None else 0
                sizeValue = videoInfo.get("Size")
                size = float(sizeValue) if sizeValue is not None else 0
                
                result = {
                    "FormatName": videoInfo.get("FormatName", ""),
                    "Duration": duration,
                    "Size": size,
                    "BitRate": videoInfo.get("BitRate", ""),
                    "CodecName": videoInfo.get("CodecName", ""),
                    "AvgFrameRate": videoInfo.get("AvgFrameRate", ""),
                    "Width": int(videoInfo.get("Width", 0)) if videoInfo.get("Width") else 0,
                    "Height": int(videoInfo.get("Height", 0)) if videoInfo.get("Height") else 0,
                    "Channels": 0,
                    "SampleRate": "",
                    "BitsPerSample": "",
                    "PlayURL": videoInfo.get("PlayURL", ""),
                }
                
                return json.dumps(result)
            else:
                raise ValueError(f"get_video_audio_info: unsupported type: {sourceType}")
        except Exception as e:
            raise Exception("get_video_audio_info: %s" % e, params)

       
