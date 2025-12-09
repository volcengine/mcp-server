import json
from typing import Any, Dict
from urllib.parse import urlparse

from src.vod.api.api import VodAPI


enhance_type = ['enhanceVideo','videSuperResolution','videoInterlacing','audioNoiseReduction']

def register_transcode_base_fn(service: VodAPI, public_methods: dict):
    """Register all VOD media MCP tools."""

    get_play_url = public_methods["get_play_url"]
    
    def _build_media_input(asset_type: str, asset_value: str, space_name: str) -> Dict[str, Any]:
        if asset_type not in {"Vid", "DirectUrl"}:
            raise ValueError(f"type must be Vid or DirectUrl, but got {asset_type}")
        if not asset_value:
            raise ValueError("media asset id is required")
        if not space_name:
            raise ValueError("spaceName is required")

        media_input: Dict[str, Any] = {"Type": asset_type}
        if asset_type == "Vid":
            media_input["Vid"] = asset_value
        else:
            media_input["DirectUrl"] = {"FileName": asset_value, "SpaceName": space_name}
        return media_input

    def _start_execution(payload: Dict[str, Any]) -> Any:
        response = service.mcp_post("McpStartExecution", {}, json.dumps(payload))
        if isinstance(response, str):
            response = json.loads(response)
            result = response.get("Result", {})
            return json.dumps({"RunId": result.get("RunId", "")})
        return response

    def handle_transcode_data(data: Dict[str, Any],spaceName: str) -> Dict[str, Any]:
            """Transcode data to MCP format."""
            FileId = data.get("FileId")
            StoreUri = data.get("StoreUri")
            FileName = ''
            if StoreUri and isinstance(StoreUri, str):
                parsed = urlparse(StoreUri)
                parts = parsed.path.split('/')[1:]
                FileName = '/'.join(parts)
            return {
                "FileId": FileId,
                "DirectUrl": FileName,
                "Url": get_play_url(spaceName, FileName),
            }
    
    def _get_media_execution_task_result(run_id: str, task_type: str) -> Any:
        response = service.mcp_get("McpGetExecution", {"RunId": run_id})
        ## video Processing Result
        video_urls = []
        ## audio Processing Result
        audio_urls = []
        ## text Processing Result
        texts = []
        if isinstance(response, str):
            temp = json.loads(response)
            temp_result = temp.get("Result", {})
            space_name = temp_result.get("Meta", {}).get("SpaceName", "")
            output = temp_result.get("Output", {}).get("Task", {})
            status = temp_result.get("Status", "")
            if status != "Success":
                return {
                        "Status": status,  
                        "Code": temp_result.get("Code", ""), 
                        "SpaceName": space_name,
                    }
            else:
                ## video Matting Result
                video_Matting = ['greenScreen', 'portraitImageRetouching']
                # video enhancement
                if task_type in enhance_type:
                    enhance_type_info = handle_transcode_data(output.get("Enhance", {}), space_name)
                    video_urls.append(enhance_type_info)
                # 人像抠图
                elif task_type in video_Matting:
                    video_matting_result = output.get("VideoMatting", {})
                    video_matting_result_video = video_matting_result.get("Video", {})
                    matting_file_name = video_matting_result_video.get("FileName", "")
                    video_urls.append({
                        "DirectUrl": matting_file_name,
                        "Vid": video_matting_result_video.get("Vid", ""),
                        "Url": get_play_url(space_name, matting_file_name),
                    })
                # 智能切片
                elif task_type == "intelligentSlicing":
                    tmp_segment = output.get("Segment", {})
                    tem_segments = tmp_segment.get("Segments", [])
                    for segment in tem_segments:
                        segment_file = segment.get("File", "")
                        segment_file_name = segment_file.get("FileName", "")
                        video_urls.append({
                            "DirectUrl": segment_file_name,
                            "Vid": segment_file.get("Vid", ""),
                            "Url": get_play_url(space_name, segment_file_name),
                        })
                
                # 人声分离
                elif task_type == "voiceSeparation":
                    audio_extract = output.get("AudioExtract", {})
                    voice_files = audio_extract.get("Voice", [])
                    background_files = audio_extract.get("Background", [])
                    voice_files_name = voice_files.get("FileName", "")
                    background_files_name = background_files.get("FileName", "")
                    audio_urls.append({
                            "DirectUrl": voice_files_name,
                            "Vid": voice_files.get("Vid", ""),
                            "Type": "voice",
                            "Url": get_play_url(space_name, voice_files_name),
                        })
                    
                    audio_urls.append({
                        "DirectUrl": background_files_name,
                        "Vid": background_files.get("Vid", ""),
                        "Type": "background",
                        "Url": get_play_url(space_name, background_files_name),
                    })
                # subtitle removal
                elif task_type == "subtitlesRemoval":
                    subtitles_removal = output.get("Erase", {})
                    subtitles_removal_file = subtitles_removal.get("File", {})
                    subtitles_removal_file_name = subtitles_removal_file.get("FileName", "")
                    video_urls.append({
                        "DirectUrl": subtitles_removal_file_name,
                        "Vid": subtitles_removal_file.get("Vid", ""),
                        "Url": get_play_url(space_name, subtitles_removal_file_name),
                    })
                # OCR
                elif task_type == "ocr":
                    ocr = output.get("Ocr", {})
                    ocr_texts = ocr.get("Texts", [])
                    texts = ocr_texts
                # ASR
                elif task_type == "asr":
                    asr = output.get("Asr", {})
                    utterances = asr.get("Utterances", [])
                    for utterance in utterances:
                        attribute = utterance.get("Attribute", {})
                        speaker = attribute.get("Speaker", "")
                        texts.append({
                            "Speaker": speaker,
                            "Text": utterance.get("Text", ""),
                            "StartTime": utterance.get("Start"),
                            "EndTime": utterance.get("End"),
                        })
                
                return {
                    "Code": temp_result.get("Code", ""), 
                    "SpaceName": space_name,
                    "VideoUrls": video_urls,
                    "AudioUrls": audio_urls,
                    "Texts": texts,
                     "Status": status,  
                }
        return response

    public_methods['_build_media_input'] = _build_media_input
    public_methods['_start_execution'] = _start_execution
    public_methods['handle_transcode_data'] = handle_transcode_data
    public_methods['_get_media_execution_task_result'] = _get_media_execution_task_result


       
