from typing import Any

def create_mcp_server(mcp, public_methods: dict):
    _build_media_input = public_methods["_build_media_input"]
    _start_execution = public_methods["_start_execution"]
    
    @mcp.tool()
    def asr_speech_to_text_task(type: str, video: str, spaceName: str, language: str = None) -> Any:
        """ASR speech-to-text captioning is supported, with two input modes available: `Vid` and  `DirectUrl`.
            Note：
            - `language`:  ** 可选字段 **， 不传会探测, 仅是在 语言较相似的情况下传递 来提高识别效果 
            - `Vid`: vid 模式下不需要进行任何处理
            - `DirectUrl`: directurl 模式下需要传递 FileName，不需要进行任何处理             
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - spaceName(str)： ** 必选字段 **,  视频空间名称
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            - language(str): ** 可选字段 **,  识别提示语言，取值如下：
                - cmn-Hans-CN: 简体中文
                - cmn-Hant-CN: 繁体中文
                - eng-US: 英语
                - jpn-JP: 日语
                - kor-KR: 韩语
                - rus-RU: 俄语
                - fra-FR: 法语
                - por-PT: 葡萄牙语
                - spa-ES: 西班牙语
                - vie-VN: 越南语
                - mya-MM: 缅甸语
                - nld-NL: 荷兰语
                - deu-DE: 德语
                - ind-ID: 印尼语
                - ita-IT: 意大利语
                - pol-PL: 波兰语
                - tha-TH: 泰语
                - tur-TR: 土耳其语
                - ara-SA: 阿拉伯语
                - msa-MY: 马来语
                - ron-RO: 罗马尼亚语
                - fil-PH: 菲律宾语
                - hin-IN: 印地语
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询,type 为 `asr`
         """
        media_input = _build_media_input(type, video, spaceName)
        ask = {
            "WithSpeakerInfo": True,
        }
        if language:
            ask["Language"] = language
        params = {
            "Input": media_input,
            "Operation": {"Type": "Task", "Task": {"Type": "Asr", "Asr": ask }},
        }
        return _start_execution(params)

    # OCR 
    @mcp.tool()
    def ocr_text_to_subtitles_task(type: str, video: str, spaceName: str) -> Any:
        """OCR text to subtitles is supported, with two input modes available: `Vid` and  `DirectUrl`.
            Note：
                - `Vid`: vid 模式下不需要进行任何处理
                - `DirectUrl`: directurl 模式下需要传递 FileName，不需要进行任何处理               
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - spaceName(str)： ** 必选字段 **,  视频空间名称
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询，type 为 `ocr` 
        """
        media_input = _build_media_input(type, video, spaceName)
        params = {
            "Input": media_input,
            "Operation": {"Type": "Task", "Task": {"Type": "Ocr", "Ocr": {}}},
        }
        return _start_execution(params)

    # subtitle removal
    @mcp.tool()
    def video_subtitles_removal_task(type: str, video: str, spaceName: str) -> Any:
        """Video subtitles removal is supported, with two input modes available: `Vid` and  `DirectUrl`.
            Note：
                - `Vid`: vid 模式下不需要进行任何处理
                - `DirectUrl`: directurl 模式下需要传递 FileName，不需要进行任何处理               
            Args：
            - type(str)：** 必选字段 **，文件类型，默认值为 `Vid` 。字段取值如下
                - Vid
                - DirectUrl
            - spaceName(str)： ** 必选字段 **,  视频空间名称
            - video： ** 必选字段 **,  视频文件信息, 当 type 为 `Vid` 时， video 为视频文件 ID；当 type 为 `DirectUrl` 时， video 为 FileName
            Returns
            - RunId(str):  媒体处理任务执行 ID, 可通过 `get_media_execution_task_result` 方法进行结果查询,type 为 `subtitlesRemoval` 
        """
        media_input = _build_media_input(type, video, spaceName)
        params = {
            "Input": media_input,
            "Operation": {
                "Type": "Task",
                "Task": {
                    "Type": "Erase",
                    
                    "Erase": {
                        "Mode": "Auto",
                        "NewVid": True,
                        "Auto": {"Type": "Subtitle"},
                    },
                },
            },
        }
        return _start_execution(params)

    


       
