from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.common.logger import get_logger
from app.core.ai_agent import get_response_from_agent
from app.common.custom_exception import CustomException
from app.config.settings import settings


logger = get_logger(__name__)

app = FastAPI(title="Multi-Agent API", version="0.1")

class RequestState(BaseModel):
    model_name: str
    messages: List[str]
    allow_search: bool
    system_prompt: List[str]
    
@app.post("/chat")
def chat_endpoint(request: RequestState):
    logger.info(f"Received request for model : {request.model_name}")
    
    if request.model_name not in settings.ALLOWED_MODELS_NAMES:
        logger.warning(f"Model {request.model_name} is not allowed.")
        raise HTTPException(status_code=400, detail=f"Model {request.model_name} is not allowed.")
    try:
        response = get_response_from_agent(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )
        logger.info(f"Response generated successfully for model {request.model_name}")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise CustomException(error_message="Failed to process the request", error_detail=e)