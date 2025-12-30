import json
from src.vod.api.api import VodAPI
from volcengine.vod.models.request.request_vod_pb2 import VodUrlUploadRequest
from src.vod.models.request.request_models import BatchUploadUrlItem
from typing import List
def create_mcp_server(mcp,  public_methods: dict, service: VodAPI,):
    get_play_url = public_methods['get_play_url']
    @mcp.tool()
    def video_batch_upload(space_name: str, urls: List[BatchUploadUrlItem] = None, ) -> dict:
        """ Batch retrieval and upload of URLs upload video、 audio to specified space via synchronous upload
            Note:
                - 本接口主要适用于文件没有存储在本地服务器或终端，需要通过公网访问的 URL 地址上传的场景。源文件 URL 支持 HTTP 和 HTTPS。
                - 本接口为异步上传接口。上传任务成功提交后，系统会生成异步执行的任务，排队执行，不保证时效性。
                - SourceUrl 必须是可公网直接访问的文件 URL，而非包含视频的网页 URL。
            Args:
                - space_name:** 必选字段 ** 空间名称 
                -  urls(list[dict[str, any]]): ** 必选字段 **  资源URL列表，每个元素是一个包含URL信息的字典
                    - SourceUrl （str）:** 必选字段 **  源文件 URL。
                    - FileExtension（str）:** 必选字段 **  文件后缀，即点播存储中文件的类型
                        - 文件后缀必须以 . 开头，不超过 8 位。
                        - 当您传入 FileExtension 时,视频点播将生成 32 位随机字符串，和您传入的 FileExtension 共同拼接成文件路径。
            Returns:
                JobIds[list[str]]：每个 URL 对应的任务 ID 列表
        """
        try:
            req = VodUrlUploadRequest()
            req.SpaceName = space_name
            for video_info in urls:
                url_set = req.URLSets.add()
                url_set.SourceUrl = video_info.SourceUrl
                url_set.FileExtension = video_info.FileExtension
            resp = service.upload_media_by_url(req)
        except Exception as e:
            raise Exception(f'video_batch_upload failed, space_name: {space_name}, urls: {urls}, error: {e}')
        else:
            if resp.ResponseMetadata.Error.Code == '':
                data = resp.Result.Data
                job_ids = [item.JobId for item in data]
                return {'JobIds': job_ids}
            else:
                raise Exception(resp.ResponseMetadata)

    @mcp.tool()
    def query_batch_upload_task_info(job_ids: str) -> dict:
        """  Obtain the query results of media processing tasks Obtain the query results of batch upload tasks
            Args:
            - job_ids(str): ** 必选字段 ** ，每个 URL 对应的任务 ID。查询多个以 , 逗号分隔，最多 ** 20 条 **。
            Returns：
            - Urls(list[map[str, str]])： 视频播放信息列表
                - Vid(str): 视频 ID。
                - Url(str): 视频 播放链接。
                - DirectUrl(str)：文件名
                - RequestId(str)：	请求唯一标识，可用于日志查询。
                - JobId：任务 ID，可用于查询 URL 上传状态。
                - State(str)： 传状态。取值如下：
                    - initial：初始状态
                    - processing：处理中
                    - success：上传成功
                    - failed：上传失败
                 - SpaceName(str)： 空间名
        """
        try:
            req = {}
            req['JobIds'] = job_ids
            resp = service.mcp_get('McpQueryUploadTaskInfo', req)
        except Exception as e:
            raise e
        else:
            if isinstance(resp, str):
                tempResp = json.loads(resp)
                # add fallback logic to check if Data exists
                result = tempResp.get('Result', {})
                data = result.get('Data', {})
                mediaInfoList = data.get('MediaInfoList', [])
                Urls = []
                for item in mediaInfoList:
                    play_url = ''
                    state = item.get('State', '')
                    space_name = item.get('SpaceName', '')
                    vid = item.get('Vid', '')
                    source_info = item.get('SourceInfo', {})
                    file_name = source_info.get('FileName', '')

                    url_info = {
                        'Vid': vid, 
                        'DirectUrl': file_name, 
                        'RequestId': item.get('RequestId', ''), 
                        'JobId': item.get('JobId', ''), 
                        'State': state, 
                        'SpaceName': space_name
                    }
                    if state == 'success' and space_name and source_info and file_name:
                        play_url = get_play_url(space_name, file_name)
                        url_info['Url'] = play_url
                    Urls.append(url_info)   
                return {'Urls': Urls}
            else:
                return {'Urls': []}
           
