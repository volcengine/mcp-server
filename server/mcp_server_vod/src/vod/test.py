
from asyncio import constants
from src.vod.api.api import VodAPI
import json
def main():
        vod_api = VodAPI()
        """ Carry out video stitching, audio stitching, and support for transitions and other capabilities.
         Note:
            -  **audio splicing does not support transitions. **
         Args:
            - params(dict): **  必选字段 **
                - SpaceName(str):  **  必选字段 ** , 任务产物的上传空间。AI 处理生成的视频将被上传至此点播空间。
                - videos(List[str]): **  必选字段 **
                    - 待拼接的视频列表：支持 ** vid:// ** 或 ** http:// ** 格式
                       *** 视频要求： *** 
                            - 支持处理 MP4、AVI、MKV、MOV 等常见格式的视频。 
                            - 建议总视频时长在 5 分钟以内。 
                - transitions(List[str]): 非必选字段
                    - 转场效果 ID：例如 ["1182359"]。concat_videos 工具支持非交叠转场的效果，
                        - 可用于非交叠转场的动画
                        - 分类：交替出场，ID：1182359
                        - 分类：旋转放大，ID：1182360
                        - 分类：泛开，ID：1182358
                        - 分类：风车，ID：1182362
                        - 分类：六角形，ID：1182365
                        - 分类：故障转换，ID：1182367
                        - 分类：飞眼，ID：1182368
                        - 分类：梦幻放大，ID：1182369
                        - 分类：开门展现，ID：1182370
                        - 分类：立方转换，ID：1182373
                        - 分类：透镜变换，ID：1182374
                        - 分类：晚霞转场，ID：1182375
                        - 分类：圆形交替，ID：1182378
                        - 注意： 
                        - 如果不提供，则没有转场，** 音频拼接 不支持转场 **
                        - 当视频数量超过转场数量 2 个及以上时，系统将自动循环使用转场。例如有 10 个视频，2 种转场效果，那么在 9 处拼接点上，这 2 种转场效果将被依次循环使用。
        Returns：
            - VCreativeId(str)：AI 智剪任务 ID
            - Code(int):  任务状态码。为 0表示任务执行成功。
            - StatusMessage(str): 接口请求的状态信息。当 StatusCode 为 0 时，此时该字段返回 success，表示成功；其他状态码时，该字段会返回具体的错误信息。
            - StatusCode(int):  接口请求的状态码。0表示成功，其他值表示不同的错误状态。
        
        """
        params=  {
            "SpaceName": "lyh-test",
            "videos": [
                "vid://v0290bg10003d31782aljht92n29lheg",
                "vid://v0290bg10003d313plaljht35casfdjg"
            ],
            "transitions": [
            "1182359"
            ]
        }
        if "SpaceName" not in params:
            raise ValueError("audio_video_stitching: params must contain SpaceName")
        if not isinstance(params["SpaceName"], str):
            raise TypeError("audio_video_stitching: params['SpaceName'] must be a string")
        if not params["SpaceName"].strip():
            raise ValueError("audio_video_stitching: params['SpaceName'] cannot be empty")
        if "videos" not in params:
            raise ValueError("audio_video_stitching: params must contain videos")
        if not isinstance(params["videos"], list):
            raise TypeError("audio_video_stitching: params['videos'] must be a list")
        if not params["videos"]:
            raise ValueError("audio_video_stitching: params['videos'] must contain at least one video")
        
        
        ParamObj = {
            "space_name": params["SpaceName"],
            "videos": params["videos"],
            "transitions": params.get("transitions", []),
        }

        audioVideoStitchingParams ={
            "ParamObj": str(ParamObj),
            "SpaceName": params["SpaceName"],
            "WorkflowId": "loki://1231245",
        }
        print(str(audioVideoStitchingParams))
        try:
            reqs = vod_api.mcp_post("VodMcpAsyncVCreativeTask", {}, json.dumps(audioVideoStitchingParams))
            return reqs
        except Exception as e:
            raise e
    


if __name__ == "__main__":
    main()

