def Error(message: str):
    return "API Error: " + message


def HandlerVolcResponse(response: dict):
    if (
        response    
        and response.get("ResponseMetadata")
        and response["ResponseMetadata"]
        and response["ResponseMetadata"].get("Error")
        and response["ResponseMetadata"]["Error"]
    ):
        return Error(response["ResponseMetadata"]["Error"]["Message"])
    return str(response)
