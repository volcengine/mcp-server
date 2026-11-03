from __future__ import annotations

from typing import Annotated, Any
from pydantic import Field, WithJsonSchema
from base.context import get_client
from ..utils.response import (
    async_task_response,
    error_response,
    sync_result_response,
)

TOOL_NAMES = ['detect_voice_activity', 'probe_audio_metadata', 'separate_voice', 'transcode_audio']
DOMAIN = 'audio'


def _structured_error(exc: Exception) -> object:
    response = getattr(exc, "response", None)
    if response is not None:
        try:
            return response.json()
        except Exception:
            pass
    return {"message": str(exc)}


def register_tools(mcp) -> None:
    @mcp.tool(name='detect_voice_activity', description='识别音频或视频中的有效人声片段，定位每段人声的起止时间并返回时间戳列表，可用于为后续语音识别、分析、剪辑或训练筛选更干净的音频输入。')
    async def detect_voice_activity(
        audio_url: Annotated[str | None, WithJsonSchema({'description': 'audio_url 为待处理的音频 URL，是条件必填项；支持公网可访问的 http/https 直链或 mediakit/tos/vod 平台资源链接；audio_url 与 video_url 二选一，必须且只能提供其中一个。支持 mp3、m4a、wav、wma、amr、aac、ogg、flac 等主流音频格式。', 'format': 'media-to-url', 'type': 'string'})] = Field(None),
        callback_args: Annotated[str | None, WithJsonSchema({'description': '自定义回调参数；任务完成时会通过事件回调原样返回，用于关联业务；字段长度最大为 512 字节。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        callback_url: Annotated[str | None, WithJsonSchema({'description': '用于接收该任务结果回调的 URL 地址；提供后优先级高于全局回调地址；地址必须以 http:// 或 https:// 开头。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        client_token: Annotated[str | None, WithJsonSchema({'description': '用户请求凭证，用于幂等控制；大小写敏感，长度不超过 64 个 ASCII 可打印字符。 默认不传。用户明确指定时原样使用；用户明确要求重试时，同一逻辑请求的重试链必须复用同一 token。已有 token 时必须复用原值；此前请求未带 token 时，可从本次重试开始创建一次并持续复用，但该 token 不对此前请求提供追溯幂等。业务参数变化视为新请求，不得复用旧 token。不得为每次尝试生成不同值。调用端运行时不判断重试意图，也不自动生成 token。', 'type': 'string'})] = Field(None),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        video_url: Annotated[str | None, WithJsonSchema({'description': 'video_url 为待处理的视频 URL，是条件必填项；支持公网可访问的 http/https 直链或 mediakit/tos/vod 平台资源链接；video_url 与 audio_url 二选一，必须且只能提供其中一个。支持 mp4、flv、ts、avi、mov、wmv、mkv 等主流视频格式。', 'format': 'media-to-url', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('detect_voice_activity', **{
                key: item for key, item in {'audio_url': audio_url, 'callback_args': callback_args, 'callback_url': callback_url, 'client_token': client_token, 'queue_id': queue_id, 'video_url': video_url}.items()
                if item is not None
            })
            return async_task_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='probe_audio_metadata', description='探测输入音频 URL，输出标准化媒资元信息，用于获取音频元信息。')
    async def probe_audio_metadata(
        audio_url: Annotated[str, WithJsonSchema({'description': '待探测的音频 URL，支持 mp3、m4a、wav、wma、amr、aac、ogg、flac 等音频格式；支持公网 HTTP/HTTPS URL、火山引擎视频点播 vod:// 和火山引擎对象存储 tos:// 三种输入协议。', 'format': 'media-to-vid', 'type': 'string'})] = Field(...),
        callback_args: Annotated[str | None, WithJsonSchema({'description': '自定义回调参数；任务完成时会通过事件回调原样返回，用于关联业务；字段长度最大为 512 字节。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        callback_url: Annotated[str | None, WithJsonSchema({'description': '用于接收该任务结果回调的 URL 地址；提供后优先级高于全局回调地址；地址必须以 http:// 或 https:// 开头。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        client_token: Annotated[str | None, WithJsonSchema({'description': '用户请求凭证，用于幂等控制；大小写敏感，长度不超过 64 个 ASCII 可打印字符。 默认不传。用户明确指定时原样使用；用户明确要求重试时，同一逻辑请求的重试链必须复用同一 token。已有 token 时必须复用原值；此前请求未带 token 时，可从本次重试开始创建一次并持续复用，但该 token 不对此前请求提供追溯幂等。业务参数变化视为新请求，不得复用旧 token。不得为每次尝试生成不同值。调用端运行时不判断重试意图，也不自动生成 token。', 'type': 'string'})] = Field(None),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('probe_audio_metadata', **{
                key: item for key, item in {'audio_url': audio_url, 'callback_args': callback_args, 'callback_url': callback_url, 'client_token': client_token, 'queue_id': queue_id}.items()
                if item is not None
            })
            return async_task_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='separate_voice', description='从音频或视频中分离人声与其他声音：通用或音乐场景输出人声和背景音两轨，短剧或口播场景可进一步输出人声、音乐和音效三轨，便于剪辑、二次创作、人声优化、语音识别或声音复刻。')
    async def separate_voice(
        audio_url: Annotated[str | None, WithJsonSchema({'description': '音频地址，仅支持公网可访问的 HTTP/HTTPS URL；支持 mp3、m4a、wav 等主流音频格式。', 'format': 'media-to-vid', 'type': 'string', 'x-description-en': 'The URL of the audio to be processed. It supports only publicly accessible HTTP or HTTPS URLs, and supports mainstream audio formats such as mp3, m4a, and wav. If both audio_url and video_url are provided, video_url takes priority.'})] = Field(None),
        callback_args: Annotated[str | None, WithJsonSchema({'description': '自定义回调参数；任务完成时会通过事件回调原样返回，用于关联业务；字段长度最大为 512 字节。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        callback_url: Annotated[str | None, WithJsonSchema({'description': '用于接收该任务结果回调的 URL 地址；提供后优先级高于全局回调地址；地址必须以 http:// 或 https:// 开头。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        client_token: Annotated[str | None, WithJsonSchema({'description': '用户请求凭证，用于幂等控制；大小写敏感，长度不超过 64 个 ASCII 可打印字符。 默认不传。用户明确指定时原样使用；用户明确要求重试时，同一逻辑请求的重试链必须复用同一 token。已有 token 时必须复用原值；此前请求未带 token 时，可从本次重试开始创建一次并持续复用，但该 token 不对此前请求提供追溯幂等。业务参数变化视为新请求，不得复用旧 token。不得为每次尝试生成不同值。调用端运行时不判断重试意图，也不自动生成 token。', 'type': 'string'})] = Field(None),
        media_output_destination: Annotated[str | None, WithJsonSchema({'description': '指定处理产物的目标存储位置；支持将处理产物存储至火山引擎视频点播（VOD）空间或对象存储（TOS）桶。存储至 VOD 时设为 `vod://<您的空间名>`，存储至 TOS 时设为 `tos://<您的桶名>`。设置后，任务结果中的 `url` 相关字段返回 `vod://` 或 `tos://` 格式的资源地址，不再返回临时下载地址。首次使用前需按需授权 AI MediaKit 将文件写入您的 VOD 空间或 TOS 桶。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        output_format: Annotated[str | None, WithJsonSchema({'default': 'aac', 'description': 'output_format 可选，用于指定分离后音频（包含 voice_audio_url 与 background_audio_url 文件）的输出格式；默认输出 AAC 格式，即 aac；也可以指定为 mp3、wav、m4a 或 flac。', 'enum': ['aac', 'mp3', 'wav', 'm4a', 'flac'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'aac'}),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        scene: Annotated[str | None, WithJsonSchema({'default': 'Audio', 'description': '分离场景，用于针对不同内容类型选择更合适的分离策略。可选值：Audio：（默认）通用场景。输出人声/背景音 2 轨。Music：音乐场景。输出人声/背景音 2 轨。Drama：短剧场景。输出人声/音乐/音效 3 轨。Narrate：口播场景。输出人声/音乐/音效 3 轨。', 'enum': ['Audio', 'Drama', 'Music', 'Narrate'], 'type': 'string'})] = Field(None, json_schema_extra={'default': 'Audio'}),
        video_url: Annotated[str | None, WithJsonSchema({'description': '视频地址，支持公网 HTTP/HTTPS URL、火山引擎视频点播 (vod://) 和火山引擎对象存储 (tos://) 三种输入协议；支持 mp4、flv、ts、avi、mov、wmv、mkv 等主流视频格式；必须提供 video_url 或 audio_url 其中之一。', 'format': 'media-to-vid', 'type': 'string', 'x-description-en': 'The URL of the video to be processed. Supports mainstream video formats such as mp4, flv, ts, avi, mov, wmv, and mkv. Supports only publicly accessible HTTP or HTTPS URLs. If both video_url and audio_url are present, video_url takes priority.'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('separate_voice', **{
                key: item for key, item in {'audio_url': audio_url, 'callback_args': callback_args, 'callback_url': callback_url, 'client_token': client_token, 'media_output_destination': media_output_destination, 'output_format': output_format, 'queue_id': queue_id, 'scene': scene, 'video_url': video_url}.items()
                if item is not None
            })
            return async_task_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

    @mcp.tool(name='transcode_audio', description='将音频转换为另一种封装与编码配置，并可调整采样率、码率、声道和响度，以及保留、新增或覆盖元信息，用于适配播放终端、网络传输和媒资库响度标准化。')
    async def transcode_audio(
        audio: Annotated[dict[str, Any], WithJsonSchema({'description': 'audio 提供音频参数配置。', 'properties': {'bitrate_kbps': {'default': 128, 'description': 'bitrate_kbps 指定音频码率，单位为 Kbps，范围 10 至 500，默认值为 128。', 'maximum': 500, 'minimum': 10, 'type': 'integer', 'x-description-en': 'The audio bitrate in Kbps. Supported values range from a minimum of 10 to a maximum of 500, and it defaults to 128.'}, 'bitrate_mode': {'default': 'cbr', 'description': 'bitrate_mode 指定音频码率控制模式，支持 cbr 和 cae，默认 cbr。cbr 是恒定码率模式，编码器会尝试让音频流每秒严格保持 bitrate_kbps 设定的码率，使文件大小可以被精确预测，适合带宽稳定性要求高的流式传输。cae 仅在 container_format 为 M4A 时支持，会根据音频内容复杂度动态调整瞬时码率，并确保整个文件平均码率接近 bitrate_kbps 目标值。', 'enum': ['cbr', 'cae'], 'type': 'string', 'x-description-en': 'Controls the audio bitrate mode. Supported values are cbr and cae, and the mode defaults to cbr. In cbr mode, the encoder tries to keep every second of the audio stream strictly at bitrate_kbps, making file size precisely predictable, so cbr is suitable for streaming scenarios with high bandwidth-stability requirements. In cae mode, the encoder dynamically adjusts instantaneous bitrate based on content complexity while ensuring the overall average bitrate approaches bitrate_kbps. cae is supported only when container_format is M4A.'}, 'channels': {'description': 'channels 指定音频声道数，支持 1 和 2；1 表示单声道，2 表示双声道。不传时不在客户端补默认值，由后端按源音频与任务配置处理。', 'enum': [1, 2], 'type': 'integer', 'x-description-en': 'Specifies the number of audio channels. Supported values are 1 for Mono and 2 for Stereo. When omitted, the client does not send a default value and the backend handles it according to the source audio and task configuration.'}, 'sample_rate': {'default': 48000, 'description': 'sample_rate 指定音频采样率，单位为 Hz，默认 48000。建议根据目标编码器填写：MP3 支持 8000、11025、12000、16000、22050、24000、32000、44100、48000；AAC 支持 8000、11025、12000、16000、22050、24000、32000、44100、48000、64000、88200、96000；Opus 支持 48000。', 'enum': [8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000, 64000, 88200, 96000], 'type': 'integer', 'x-description-en': 'Specifies the audio sample rate in Hz, and it defaults to 48000. Filling this field according to the target encoder is recommended. MP3 supports sample rates 8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, and 48000. AAC supports sample rates 8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000, 64000, 88200, and 96000. Opus supports sample rate 48000.'}, 'volume_integrated_loudness': {'default': -12, 'description': 'volume_integrated_loudness 用于设定音频整体感知音量的目标综合响度，单位为 LUFS，范围 -70 至 -5，默认值为 -12。', 'maximum': -5, 'minimum': -70, 'type': 'number', 'x-description-en': 'Sets the overall perceived audio volume in LUFS. The minimum value is -70 and the maximum value is -5, with a default of -12. This field is optional.'}, 'volume_loudness_range': {'default': 7, 'description': 'volume_loudness_range 调节音频最响亮和最安静部分之间的差异，单位为 LU，范围 1 至 20，默认值为 7；volume_method 为 2Pass 时生效。', 'maximum': 20, 'minimum': 1, 'type': 'number', 'x-description-en': 'Adjusts the difference between the loudest and quietest audio parts, measured in LU. The minimum value is 1 and the maximum value is 20, with a default of 7. This field is optional and takes effect when volume_method is set to 2Pass.'}, 'volume_method': {'description': 'volume_method 是音量均衡算法开关；不设置时不处理音量。支持将 volume_method 设置为 2Pass 启用两阶段响度分析与处理，此时 volume_integrated_loudness、volume_true_peak 和 volume_loudness_range 生效。', 'enum': ['2Pass'], 'type': 'string', 'x-description-en': 'Controls loudness normalization for the audio, and is optional. If it is not set, the volume is not processed. Setting it to 2Pass enables two-pass loudness analysis and processing, and the integrated loudness, true peak, and loudness range settings then take effect.'}, 'volume_true_peak': {'default': 0, 'description': 'volume_true_peak 设置音频信号的真实峰值最高上限，以防止削波失真，单位为 dBTP，范围 -9 至 0，默认值为 0。', 'maximum': 0, 'minimum': -9, 'type': 'number', 'x-description-en': 'Sets the maximum audio signal limit to prevent clipping distortion, in dBTP. This field is optional and defaults to 0, which is also the maximum allowed value. The minimum is -9.'}}, 'required': ['sample_rate', 'bitrate_mode', 'bitrate_kbps'], 'type': 'object', 'x-description-en': 'Contains the audio parameter configuration.'})] = Field(...),
        audio_url: Annotated[str, WithJsonSchema({'description': 'audio_url 是待转码音频的 URL，支持公网 HTTP/HTTPS URL、视频点播 vod:// 和对象存储 tos:// 三种输入协议；输入支持 mp3、m4a、wav、wma、amr、aac、ogg、flac 等音频格式。', 'format': 'media-to-vid', 'type': 'string', 'x-description-en': 'The URL of the audio to be transcoded. This field is required, and only publicly accessible HTTP/HTTPS URLs are supported as the file source. Supported input formats include mainstream audio formats such as mp3, m4a, wav, wma, amr, aac, ogg, and flac.'})] = Field(...),
        container_format: Annotated[str, WithJsonSchema({'default': 'MP3', 'description': 'container_format 指定目标封装格式，建议填写，默认 MP3；系统根据封装格式自动选择对应编码器：MP3 封装格式使用 MP3 编码器，M4A 封装格式使用 AAC 编码器，OGG 封装格式使用 Opus 编码器。', 'enum': ['MP3', 'M4A', 'OGG'], 'type': 'string', 'x-description-en': 'Specifies the target container format. Specifying this field is recommended, and it defaults to MP3. Supported container formats are MP3, M4A, and OGG. The system selects the MP3 encoder for MP3, the AAC encoder for M4A, and the Opus encoder for OGG.'})] = Field(...),
        callback_args: Annotated[str | None, WithJsonSchema({'description': '自定义回调参数；任务完成时会通过事件回调原样返回，用于关联业务；字段长度最大为 512 字节。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        callback_url: Annotated[str | None, WithJsonSchema({'description': '用于接收该任务结果回调的 URL 地址；提供后优先级高于全局回调地址；地址必须以 http:// 或 https:// 开头。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        client_token: Annotated[str | None, WithJsonSchema({'description': '用户请求凭证，用于幂等控制；大小写敏感，长度不超过 64 个 ASCII 可打印字符。 默认不传。用户明确指定时原样使用；用户明确要求重试时，同一逻辑请求的重试链必须复用同一 token。已有 token 时必须复用原值；此前请求未带 token 时，可从本次重试开始创建一次并持续复用，但该 token 不对此前请求提供追溯幂等。业务参数变化视为新请求，不得复用旧 token。不得为每次尝试生成不同值。调用端运行时不判断重试意图，也不自动生成 token。', 'type': 'string'})] = Field(None),
        media_output_destination: Annotated[str | None, WithJsonSchema({'description': '指定处理产物的目标存储位置；支持将处理产物存储至火山引擎视频点播（VOD）空间或对象存储（TOS）桶。存储至 VOD 时设为 `vod://<您的空间名>`，存储至 TOS 时设为 `tos://<您的桶名>`。设置后，任务结果中的 `url` 相关字段返回 `vod://` 或 `tos://` 格式的资源地址，不再返回临时下载地址。首次使用前需按需授权 AI MediaKit 将文件写入您的 VOD 空间或 TOS 桶。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
        metadata_add_tags: Annotated[list[Any] | None, WithJsonSchema({'description': 'metadata_add_tags 指定为输出音频新增的元信息标签；新增标签与保留标签同名时，新增标签设置覆盖源文件的值。', 'items': {'properties': {'key': {'description': 'metadata_add_tags 中每个标签由 key 组成。', 'type': 'string', 'x-description-en': 'The key of a metadata tag.'}, 'value': {'description': 'metadata_add_tags 中每个标签由 value 组成。', 'type': 'string', 'x-description-en': 'The value of a metadata tag.'}}, 'type': 'object'}, 'type': 'array', 'x-description-en': 'An optional Array of Objects specifying the metadata tags to add to the output audio.'})] = Field(None),
        metadata_keep_tags: Annotated[list[Any] | None, WithJsonSchema({'description': 'metadata_keep_tags 指定从源音频保留的元信息标签键；默认情况下，转码会丢弃大部分元信息，例如标题和艺术家。', 'items': {'type': 'string'}, 'type': 'array', 'x-description-en': 'An optional list of metadata tag keys to keep from the source audio, given as an Array of Strings. By default, transcoding discards most metadata, such as title and artist.'})] = Field(None),
        queue_id: Annotated[str | None, WithJsonSchema({'description': '任务提交的目标队列 ID；不传时默认使用系统自动创建的队列 ID。可将不同业务或优先级的任务提交到不同队列，以按队列对应的项目进行分账。队列可创建和管理，系统会自动分配队列 ID。 仅在用户明确提供该值时传递；不得由 Agent 生成、推断或补写。', 'type': 'string'})] = Field(None),
    ) -> dict:
        try:
            result = get_client().call('transcode_audio', **{
                key: item for key, item in {'audio': audio, 'audio_url': audio_url, 'container_format': container_format, 'callback_args': callback_args, 'callback_url': callback_url, 'client_token': client_token, 'media_output_destination': media_output_destination, 'metadata_add_tags': metadata_add_tags, 'metadata_keep_tags': metadata_keep_tags, 'queue_id': queue_id}.items()
                if item is not None
            })
            return async_task_response(result)
        except Exception as exc:
            return error_response(_structured_error(exc))

