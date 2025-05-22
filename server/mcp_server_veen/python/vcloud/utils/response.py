import json


def Error(message: str):
    return "API Error: " + message


def HandlerVolcResponse(response: dict):
    if not response:
        return Error("Empty response")
        
    json_response = response if not isinstance(response, str) else json.loads(response)
    error = json_response.get("ResponseMetadata", {}).get("Error")
    
    if error and isinstance(error, dict):
        message = error.get("Message", "Unknown error")
        return Error(message)
        
    return str(response)