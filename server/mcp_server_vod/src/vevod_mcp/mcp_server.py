 # Copyright 2025 Beijing Volcano Engine Technology Ltd.
 # SPDX-License-Identifier: MIT
import os
import json
import time
import random
import string
from mcp.server.fastmcp import FastMCP
from .api.vod import VodAPI
from volcengine.vod.models.request.request_vod_pb2 import *
from volcengine.vod.models.business.vod_workflow_pb2 import *
from volcengine.util.Functions import Function


def create_mcp_server():
    vod_service = VodAPI()

    """Create and configure VOD MCP server instance"""
    mcp = FastMCP(
        "VOD MCP"
    )
    
    @mcp.tool()
    def guide():
        """VOD MCP is the Volcengine VOD MCP Server.

        (en)Before using the VOD service, please note:
        - `create_space` creates a test space without requiring parameters (recommended to create by default, space names must be globally unique)
        - Before `create_space`, use `list_space` to check existing spaces. If a space starting with 'mcp-test-space-' exists, use it. Otherwise create one.
        - After `create_space` use `list_space` list the avaliable spaces，get the SpaceName as params for  `upload_media`
        - `upload_media` requires an available space. Specify a space before uploading. If none specified, check for existing test space or create one.
        - Before `upload_media`, use `list_space` to verify space availability.
        - `upload_media` requires user to input local video file path. Other parameters use default values unless specified.
        - If `upload_media` fails, recheck space availability and upload address configuration.
        - If `get_play_info` (get video playback URL) fails due to missing domain configuration, show error guidance.
        - `submit_direct_edit_task_async` video editing depends on `upload_media` and `get_play_info` to get vid. Before editing, use `get_media_info` to get video duration as TargetTime for video/text types.
        - `submit_direct_edit_task_async` requires TargetTime parameter to be non-empty array.
        - For `submit_direct_edit_task_async`, refer to examples for parameter construction.

        (zh)在使用点播服务服务之前，需要知道以下事情:
        - 创建测试空间之前先使用 `list_space` 查询空间列表，如果有返回mcp-test-space-开头的空间，则直接推荐使用该空间，如果没有使用`create_space`创建一个测试空间，不需要传入参数，可以直接使用默认参数
        - 在使用`create_space`创建空间之前，先使用`list_space`查询可用空间，如果存在可用空间则直接使用（空间名称对应字段是SpaceName），创建完成之后可以通过`list_space`获取可用空间
        - 使用`upload_media`上传视频时需要先通过`list_space`查询该空间（SpaceName）是否可用，使用SpaceName作为参数（space_name），并需要输入本地文件地址
        - 可以通过`upload_media`上传视频到指定空间，上传视频之前需要指定一个空间，用户没有主动指定时可以先看是否已经有创建测试空间，有则直接使用，没有则创建一个测试空间
        - 上传视频需要用户输入本地视频资源地址，其他参数可以使用内部默认值，除非用户需要主动输入
        - 如果上传失败，需要重新检查空间是否可用，以及是否有设置上传地址
        - 如果指定Vid，可以通过`get_media_info`查询该视频的完整信息，作为参数给`submit_direct_edit_task_async`执行
        - get_play_info（获取视频播放地址）失败因为没有配置域名时，直接展示错误引导就行，不用再执行后续tool
        - 在执行`submit_direct_edit_task_async`之前，先通过`get_media_info`查询视频信息(获取视频时长、Vid)，将视频时长作为`submit_direct_edit_task_async` video、text等类型的TargetTime输入，TargetTime不能为空数组，默认使用get_media_info获取视频播放信息
        - `submit_direct_edit_task_async`执行剪辑任务的参数拼接参照示例进行
            - 文字叠加示例Track要放在轨道的最前面
               Extra示例：         
                "Extra": [
                    {
                        "Type": "transform",
                        "PosX": 0,
                        "PosY": 0,
                        "Width": 100,
                        "Height": 100
                    }
                ]
            - 一个视频截取多段拼接时，需要设置Extra字段，不要跟TargeTime混淆
              Extra示例（EndTime、StartTime对应想要在原视频中截取的时间段）：
                "Extra": [
                    {
                        "EndTime": 15000,
                        "StartTime": 5000,
                        "Type": "trim"
                    }
                ],
            - 转场动画需要在前一个视频中增加Extra字段
                Extra设置示例（Duration是持续时间）
                  "Extra": [{
                        "Type": "transition",
                        "Source": "1182359",
                        "Duration": 2000
                    }]
        - submit_direct_edit_task_async 执行完成后需要根据`get_direct_edit_progress`查询任务处理进度，再根据`get_direct_edit_result`查询处理结果
        - 任务执行完成通过`get_play_info`获取相应VID视频的播放信息

        """
        return """use `guide` description to get how to use VOD Mcp Server"""

    
    # ========================
    # Space Management Functions
    # ========================
    @mcp.tool()
    def get_space_detail(space_name: str) -> str:
        """Get space details
        获取空间详细信息
            Args:
                space_name: Space name (required)
            Returns:
                space info as a string.
        """
        try:
            req = VodGetSpaceDetailRequest()
            req.SpaceName = space_name
            resp = vod_service.get_space_detail(req)
            return str(resp)
        except Exception as e:
            return str(e)

    @mcp.tool()
    def list_space() -> str:
        """List available spaces for the user
        获取空间列表
            Returns:
                list of space info as a string.
        """
        try:
            req = VodListSpaceRequest()
            resp = vod_service.list_space(req)
            return str(resp)
        except Exception as e:
            return str(e)

    @mcp.tool()
    def create_space(space_name: str = None, project_name: str = None, space_desc:str = None, region:str = "cn-north-1") -> str:
        """Create VOD space. For test spaces, no parameters needed - uses defaults.
            Args:
                space_name: Space name, defaults to randomly generated 'mcp-test-space-' prefix
                project_name: Project name, defaults to 'default'
                space_desc: Space description, defaults to empty
            创建点播空间，需要创建测试空间时不需要传入参数，可以直接使用默认参数
             Args:
                space_name: 空间名称, 默认使用mcp-test-space-开始随机生成的空间名称
                project_name: 项目名称, 默认使用default
                space_desc: 空间描述，默认为空

            Returns:
                result of space info as a string.

        """
        try:
            req = VodCreateSpaceRequest()
            req.Region = region
            req.SpaceName = space_name if space_name else 'mcp-test-space-' + ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(8))
            req.ProjectName = project_name if project_name else "default"
            req.Description = space_desc if space_desc else ""
            resp = vod_service.create_space(req)
            return str(resp)
        except Exception as e:
            return str(e)

    @mcp.tool()
    def upload_media(
        space_name: str, 
        file_path: str, 
        functions: list = None,
        callback_args: str = '',
        file_name: str = None,
        storage_class: int = 1,
        upload_host_prefer: str = ''
    ) -> str:
        """Upload audio/video to specified space via synchronous upload
            Args:
                space_name: Space name (required)
                file_path: Local file path with extension (required)
            同步上传音频、视频到指定的空间里
             Args:
                space_name: 空间名称 (必须)
                file_path: 带有扩展名的本地文件路径 (必须)
            Returns:
                media info as a string.
        """
        try:
            req = VodUploadMediaRequest()
            req.SpaceName = space_name
            req.FilePath = file_path
            req.Functions = json.dumps(functions or [])
            req.CallbackArgs = callback_args
            req.FileName = file_name if file_name else os.path.basename(file_path)
            req.FileExtension = os.path.splitext(file_path)[1]
            req.StorageClass = storage_class
            req.UploadHostPrefer = upload_host_prefer
            
            resp = vod_service.upload_media(req)
            return str(resp)
        except Exception as e:
            return str(e)

    # ========================
    # Direct Editing Task Functions
    # ========================

    @mcp.tool()
    def submit_direct_edit_task_async(
        space_name: str,
        edit_param: dict,
    ) -> str:
        """Submit audio/video editing task asynchronously, supporting:
           - Video splicing/composition
           - Audio-video mixing
           - Transition effects
           - Text overlays
           - And other scenarios
            Args:
                space_name: Space name (required)
                edit_param: Editing parameters object containing:
                    Upload (UploadInfo): Upload settings (required)
                        SpaceName (str): Upload space for output (required)
                        VideoName (str): Output video name in VOD space (optional)
                        FileName (str): Output file path (optional)
                    Output (Output): Encoding output settings (optional)
                        Alpha (bool): Include alpha channel (default false)
                        Format (str): Output format (mp4/hls/mp3)
                        Fps (float): Output frame rate (default 30fps)
                        Codec (dict): Audio/video codec settings
                            VideoCodec (str): Video codec (h264/h265/vp9)
                            AudioCodec (str): Audio codec (aac)
                        DisableVideo (bool): Audio-only output (default false)
                        DisableAudio (bool): Video-only output (default false)
                        Cover (dict): Frame extraction settings
                        CanvasWithMax (bool): Follow max resolution (default false)
                    Canvas (Canvas): Rendering canvas settings (required)
                        Width (int|str): Output width (default 720px), use the source vid's Width default
                        Height (int|str): Output height (default 1280px),use the source vid's Height default
                        BackgroundColor (str): Canvas color (RGBA)
                        Long/Short (int): Long/short side settings (requires CanvasWithRatio=true)
                        Ratio (str): Aspect ratio (e.g. "16:9")
                    Track (Track[]): Track list (required)
                        Type (str): Resource type (audio/video/text - currently supported)
                        TargetTime (list[int]): Resource timeline [start,end] in ms (required, non-empty array)
                        Source (str): Resource URL (vid:// or tos:// format)
                        Extra (list[dict]): Extended resources (filter types)

            提交异步音视频剪辑任务，支持视频拼接、画中画、音视频混合、转场特效、文字叠加等场景
             Args:
                space_name: 空间名称（必选）
                edit_param: 编辑参数对象，包含以下字段:
                    Upload (UploadInfo): 业务上传设置(必选)
                        SpaceName (str): 任务产物的上传空间(必选)
                        VideoName (str): 任务产物在点播空间中的名称(可选)
                        FileName (str): 任务产物的文件路径(可选)
                    Output (Output): 编码输出设置(可选)
                        Alpha (bool): 是否包含alpha通道(默认false)
                        Format (str): 输出文件封装格式(mp4/hls/mp3)
                        Fps (float): 输出视频帧率(默认30fps)
                        Codec (dict): 音视频编码参数设置
                            VideoCodec (str): 视频编码格式(h264/h265/vp9)
                            AudioCodec (str): 音频编码格式(aac)
                        DisableVideo (bool): 是否仅输出音频(默认false)
                        DisableAudio (bool): 是否仅输出视频(默认false)
                        Cover (dict): 抽帧抽封面设置
                        CanvasWithMax (bool): 画布分辨率是否遵循最大分辨率(默认false)
                    Canvas (Canvas): 渲染画布设置(可选)
                        Width (int|str): 输出视频宽度(默认720px)
                        Height (int|str): 输出视频高度(默认1280px)
                        BackgroundColor (str): 画布颜色(RGBA格式)
                        Long/Short (int): 长/短边设置(需CanvasWithRatio=true)
                        Ratio (str): 长短边比(如"16:9")
                    Track (Track[]): 轨道列表(必选)
                        Type (str): 资源类型(audio/video/text，目前只支持这三种)
                        TargetTime (list[int]): 资源在轨道中的时间[开始,结束](ms)，单位是ms，用户可以指定资源轨道的起始、截止时间，不能为空数组
                        Source (str): 资源下载地址(vid://或tos://格式)
                        Extra (list[dict]): 拓展资源(filter类型)
                Returns:
                    result of edit task as a string.

                Examples:
                    1. Video timeline splicing example (demonstrates how to splice 2 videos into one), request parameters:
                       视频时域拼接示例（本示例演示如何将2个视频按时域拼接为一个视频），请求参数如下:
                    {
                       "Canvas": {
                            "Height": 720,
                            "Width": 1280
                        },
                        "Track": [
                            [
                                {
                                    "Source": "vid://v03567g100***2ljht77lji4oeg",
                                    "TargetTime": [],
                                    "Type": "video"
                                },
                                {
                                    "Source": "vid://v02567g1006***grjaljhtfnjiifjg0", 
                                    "TargetTime": [],
                                    "Type": "video"
                                }
                            ]
                        ],
                        "Upload": {
                            "SpaceName": "vod-**-2025"
                        }
                    }

                    2. Multi-segment video extraction example (demonstrates extracting segments at 5-15s, 25-35s, 50-60s, 80-100s and recomposing into one video), request parameters:
                       视频多段截取合成示例（本示例演示如何截取一个视频里时域在 5-15 秒、25-35 秒、50-60 秒、80-100 秒的内容，并重新合成一个视频。）请求参数如下:
                       - 注意，多段视频截取合成时需要使用Extra字段，StartTime、EndTime是想要在原视频中截取的时间段
                       - TargetTime是想要拼接的视频在轨道里的起始、截止时间
                    {
                        "Canvas": {
                            "Height": 720,
                            "Width": 1280
                        },
                        "Output": {
                            "Fps": 25
                        },
                        "Track": [
                            [
                                {
                                    "Extra": [
                                        {
                                            "EndTime": 15000,
                                            "StartTime": 5000,
                                            "Type": "trim"
                                        }
                                    ],
                                    "Source": "vid://v02b6d97000***pi6vambf9r4s5qhg",
                                    "TargetTime": [0, 10000],
                                    "Type": "video"
                                },
                                {
                                    "Extra": [
                                        {
                                            "EndTime": 35000,
                                            "StartTime": 25000,
                                            "Type": "trim"
                                        }
                                    ],
                                    "Source": "vid://v02b6d970000***6vambf9r4s5qhg",
                                    "TargetTime": [10000, 20000],
                                    "Type": "video"
                                },
                                {
                                    "Extra": [
                                        {
                                            "EndTime": 60000,
                                            "StartTime": 50000,
                                            "Type": "trim"
                                        }
                                    ],
                                    "Source": "vid://v02b6d970000***i6vambf9r4s5qhg",
                                    "TargetTime": [20000, 30000],
                                    "Type": "video"
                                },
                                {
                                    "Extra": [
                                        {
                                            "EndTime": 100000,
                                            "StartTime": 80000,
                                            "Type": "trim"
                                        }
                                    ],
                                    "Source": "vid://v02b6d97000***i6vambf9r4s5qhg",
                                    "TargetTime": [30000, 50000],
                                    "Type": "video"
                                }
                            ]
                        ],
                        "Upload": {
                            "SpaceName": "edit_test",
                            "VideoName": "edit_test"
                        }
                    }
                3. Audio-video mixing example (demonstrates combining video with audio), request parameters:
                   音视频混合示例（本示例演示如何将一个视频跟一个音频合成在一起），请求参数如下:
                {
                    "Canvas": {
                        "Height": 720,
                        "Width": 1280
                    },
                    "Track": [
                        [
                            {
                                "Source": "vid://v03567g1006***grj2ljht77lji4oeg",
                                "TargetTime": [],
                                "Type": "video"
                            }
                        ],
                        [
                            {
                                "Source": "vid://a02567g10064***rjaljhtfnjiifjg0",
                                "TargetTime": [],
                                "Type": "audio"
                            }
                        ]
                    ],
                    "Output": {
                        "Format": "mp4",
                        "Fps": 30
                    },
                    "Upload": {
                        "SpaceName": "vod-**-2025"
                    }
                }

                4. Video splicing with transitions example (demonstrates splicing two videos with alternating transitions), request parameters:
                   视频拼接转场示例（本示例演示如何将两个视频按时域拼接为一个视频并添加交替出场的转场效果），请求参数如下:
                {
                    "Upload": {
                        "SpaceName": "edit_test",
                        "VideoName": "video-transition-example"
                    },
                    "Canvas": {
                        "Width": "$0|0.h",
                        "Height": "$0|0.w"
                    },
                    "Track": [
                        [
                            {
                                "Source": "vid://v0d399g10001cuh***qljht476t34bc0",
                                "Type": "video",
                                "TargetTime": [0, 4000],
                                "Extra": [{
                                    "Type": "transition",
                                    "Source": "1182359",
                                    "Duration": 2000
                                }]
                            },
                            {
                                "Source": "vid://v02399g10001c***r9qljht49uesktf0",
                                "Type": "video",
                                "TargetTime": [4000, 9000]
                            }
                        ]
                    ]
                }

                5. 文字叠加示例（本示例演示如何将特定的文字压入到视频中），请求参数如下:
                {
                    "Canvas": {
                        "Height": 720,
                        "Width": 1280
                    },
                    "Track": [
                        [
                            {
                                "Type": "text",
                                "TargetTime": [0, 10000],
                                "Text": "example-text",
                                "FontSize": 20,
                                "FontColor":"#FF0000FF",
                                "Extra": [
                                    {
                                        "Type": "transform",
                                        "PosX": 0,
                                        "PosY": 0,
                                        "Width": 100,
                                        "Height": 100
                                    }
                                ]
                            }
                        ],
                        [
                            {
                                "Source": "vid://v03567g1006***grj2ljht77lji4oeg",
                                "TargetTime": [],
                                "Type": "video"
                            }
                        ]
                    ],
                    "Upload": {
                        "SpaceName": "vod-**-2025"
                    }
                }

                6. Adding filters example (demonstrates adding TransformFilter and LutFilter to video), request parameters:
                  添加滤镜（本示例演示如何为视频添加TransformFilter和LutFilter），请求参数如下:
                {
                    "Upload": {
                        "SpaceName": "edit_test",
                        "VideoName": "edit_test"
                    },
                    "Output": {
                        "Alpha": false,
                        "Fps": 24.99,
                        "Codec": {
                            "VideoCodec": "h264",
                            "Preset": "slow",
                            "Crf": 23,
                            "AudioCodec": "aac",
                            "AudioBitrate": 128
                        },
                        "DisableVideo": false,
                        "DisableAudio": true
                    },
                    "Track": [
                        [
                            {
                                "Type": "video",
                                "Source": "vid://v02b6d970***5pi6vambf9r4s5qhg",
                                "TargetTime": [0, 4000],
                                "Extra": [
                                    {
                                        "Type": "transform",
                                        "PosX": 0,
                                        "PosY": 0,
                                        "Width": 720,
                                        "Height": 1280,
                                        "Alpha": 1
                                    },
                                    {
                                        "Type": "lut_filter",
                                        "Source": "loki://1183993",
                                        "TargetTime": [0, 4000],
                                        "Intensity": 1
                                    }
                                ]
                            }
                        ]
                    ],
                    "Canvas": {
                        "Width": 720,
                        "Height": 1280
                    }
                }
        """
        try:
            req = VodSubmitDirectEditTaskAsyncRequest()
            req.Uploader = space_name
            req.Application = "VideoTrackToB"
            req.Priority = 0
            req.EditParam = json.dumps(edit_param).encode('utf-8')
            
            resp = vod_service.submit_direct_edit_task_async(req)
            return str(resp)
        except Exception as e:
            return str(e)

    @mcp.tool()
    def cancel_direct_edit_task(req_id: str) -> str:
        """Cancel editing task
            Args:
                req_id: request id, can get by submit_direct_edit_task_async tool
            Returns:
                result of cancel edit task as a string.
        """
        try:
            req = VodCancelDirectEditTaskRequest()
            req.ReqId = req_id
            resp = vod_service.cancel_direct_edit_task(req)
            return str(resp)
        except Exception as e:
            return str(e)

    @mcp.tool()
    def get_direct_edit_progress(req_id: str) -> str:
        """Check editing task progress (100 means completed)
            Args:
                req_id: request id
            Returns:
                progress of  edit task as a string.
        """
        try:
            req = VodGetDirectEditProgressRequest()
            req.ReqId = req_id
            resp = vod_service.get_direct_edit_progress(req)
            return str(resp)
        except Exception as e:
            return str(e)

    @mcp.tool()
    def get_direct_edit_result(req_ids: list) -> str:
        """Get editing task execution details (Status=success means completed successfully)
            Args:
                req_ids: list of request ids
            Returns:
                progress of  edit task as a string.
        """
        try:
            req = VodGetDirectEditResultRequest()
            req.ReqIds.extend(req_ids)
            resp = vod_service.get_direct_edit_result(req)
            return str(resp)
        except Exception as e:
            return str(e)


    @mcp.tool()
    def upload_by_url(
        space_name: str,
        source_url: str,
        file_extension: str,
        callback_args: str = '',
        custom_headers: dict = None
    ) -> str:
        """Batch URL pull upload
            Args:
                space_name: Space name
                source_url: Video source url
                file_extension: video file extension
            Returns:
                upload result as a string.
        """
        try:
            req = VodUrlUploadRequest()
            req.SpaceName = space_name
            url_set = req.URLSets.add()
            url_set.SourceUrl = source_url
            url_set.FileExtension = file_extension
            url_set.CallbackArgs = callback_args
            if custom_headers:
                url_set.CustomURLHeaders.update(**custom_headers)
            
            resp = vod_service.upload_media_by_url(req)
            return str(resp)
        except Exception as e:
            return str(e)

    @mcp.tool()
    def get_play_info(vid: str, ssl: str = '1') -> str:
        """Get video playback URL
            Args:
                vid: id of vod video
                ssl: use https or not
            Returns:
                video detail info  as a string.
        """
        try:
            req = VodGetPlayInfoRequest()
            req.Vid = vid
            req.Ssl = ssl
            resp = vod_service.get_play_info(req)
            return str(resp)
        except Exception as e:
            return f"{str(e)}\n\nIf failed to get playback info, you can view & preview the video in Volcengine console: https://console.volcengine.com/vod"

    @mcp.tool()
    def list_domain(space_name: str) -> str:
        """List space domains
        获取空间域名列表
            Args:
                space_name: Space name
            Returns:
                list of domain of special spaceName  as a string.
        """
        try:
            req = VodListDomainRequest()
            req.SpaceName = space_name
            resp = vod_service.list_domain(req)
            return str(resp)
        except Exception as e:
            return str(e)

    @mcp.tool()
    def get_media_info(vid: str) -> str:
        """Get media asset information
             Args:
                vid: id of vod video
            Returns:
                media info  as a string.
        """
        try:
            req = VodGetMediaInfosRequest()
            req.Vids = vid
            resp = vod_service.get_media_infos(req)
            return str(resp)
        except Exception as e:
            return str(e)

    @mcp.tool()
    def update_publish_status(vid: str, status: str) -> str:
        """Update media publish status (can publish media)
        修改媒资发布状态，可以发布媒资
            Args:
                vid: id of vod video
                status: Published or Blocked
            Returns:
                publish status info  as a string.
        """
        try:
            req = VodUpdateMediaPublishStatusRequest()
            req.Vid = vid
            req.Status = status
            resp = vod_service.update_media_publish_status(req)
            return str(resp)
        except Exception as e:
            return str(e)


    @mcp.tool()
    def get_media_list(
        space_name: str,
        vid: str = None,
        status: str = None,
        order: str = None,
        start_time: str = None,
        end_time: str = None,
        offset: str = '0',
        page_size: str = '10',
        classification_id: int = None
    ) -> str:
        """List audio/video files uploaded to VOD space
        查询当前空间音视频列表
            Args:
                space_name: space name
                vid: id of vod video
                status: Published or Blocked
                order: Desc
                start_time: start time
                end_time: end time
                offset: offset
                page_size: page size
                classification_id: classification id
            Returns:
                publish status info  as a string.
        """
        try:
            req = VodGetMediaListRequest()
            req.SpaceName = space_name
            if vid: req.Vid = vid
            if status: req.Status = status
            if order: req.Order = order
            if start_time: req.StartTime = start_time
            if end_time: req.EndTime = end_time
            req.Offset = offset
            req.PageSize = page_size
            if classification_id: req.ClassificationId = classification_id
            resp = vod_service.get_media_list(req)
            return str(resp)
        except Exception as e:
            return str(e)


    return mcp
