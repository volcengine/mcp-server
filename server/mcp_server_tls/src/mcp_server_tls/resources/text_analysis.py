import json
import logging
import httpx

from typing import Optional
from volcengine.tls.tls_exception import TLSException
from mcp_server_tls.consts import *
from mcp_server_tls.request import custom_api_call

logger = logging.getLogger(__name__)

async def create_app_instance_resource(
        auth_info: dict,
        instance_name: str,
        instance_type: str,
        description: Optional[str] = None,
) -> dict:
    try:
        body = {
            "InstanceName": instance_name,
            "InstanceType": instance_type,
        }

        if description is not None:
            body["Description"] = description

        return await custom_api_call(
            auth_info=auth_info,
            api=API_CREATE_APP_INSTANCE,
            body=body,
        )

    except TLSException as e:
        logger.error("create_app_instance_resource")
        raise e

async def describe_app_instances_resource(
        auth_info: dict,
        instance_id: Optional[str]=None,
        instance_type: Optional[str]=None,
        instance_name: Optional[str]=None,
        description: Optional[str] = None,
        page_number: int = 1,
        page_size: int = 10,
) -> dict:
    try:
        params = {
            "PageNumber": page_number,
            "PageSize": page_size,
        }

        if instance_id is not None:
            params["InstanceId"] = instance_id

        if instance_type is not None:
            params["InstanceType"] = instance_type

        if instance_name is not None:
            params["InstanceName"] = instance_name

        if description is not None:
            params["Description"] = description

        return await custom_api_call(
            auth_info=auth_info,
            api=API_DESCRIBE_APP_INSTANCES,
            params=params
        )

    except TLSException as e:
        logger.error("describe_app_instances_resource error")
        raise e

async def create_app_scene_meta_resource(
        auth_info: dict,
        instance_id: str,
        app_meta_type: str,
        topic_id: Optional[str] = None,
        record: Optional[dict] = None,
) -> dict:
    try:
        body = {
            "InstanceId": instance_id,
            "CreateAPPMetaType": app_meta_type,
        }

        if topic_id is not None:
            body["Id"] = topic_id

        if record is not None:
            body["Record"] = record

        return await custom_api_call(
            auth_info=auth_info,
            api=API_CREATE_APP_SCENE_META,
            body=body
        )

    except TLSException as e:
        logger.error("create_app_scene_meta_resource error")
        raise e

async def describe_session_answer_resource(
        auth_info: dict,
        instance_id: str,
        topic_id: str,
        session_id: str,
        question: str,
        parent_message_id: Optional[str] = None,
        question_id: Optional[str] = None,
        intent: Optional[int] = None,
) -> str:

    answers = []
    suggestions = []
    data_prefix = "data:"

    try:

        body = {
            "InstanceId": instance_id,
            "Question": question,
            "SessionId": session_id,
            "TopicId": topic_id,
        }

        if parent_message_id is not None:
            body["ParentMessageId"] = parent_message_id

        if question_id is not None:
            body["QuestionId"] = question_id

        if intent is not None:
            body["Intent"] = intent

        response_stream: httpx.Response = await custom_api_call(
            auth_info=auth_info,
            api=API_DESCRIBE_SESSION_ANSWER,
            body=body,
            is_stream=True,
        )

        for line in response_stream.iter_lines():
            if not line.startswith(data_prefix):
                continue
            try:
                data = json.loads(line.removeprefix(data_prefix).strip())
                answer = data.get("Message", {}).get("Answer", "")

                rsp_msg_type = data.get("RspMsgType", None)
                match rsp_msg_type:
                    # inference
                    case 2:
                        answers.append(answer)
                    # suggestion
                    case 3:
                        suggestions = data.get("Suggestions", [])
                    case _:
                        continue
            except json.JSONDecodeError as e:
                logger.error(f"Describe seesion answer error, response json decode failed: {e}")

        return json.dumps({"answer": "".join(answers), "Suggestions": suggestions, "session_id": session_id}, ensure_ascii=False)

    except TLSException as e:
        logger.error("describe_session_answer_resource error")
        raise e
