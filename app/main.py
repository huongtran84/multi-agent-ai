import subprocess
import threading
import time
import os
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
load_dotenv()

def run_backend():
    try:
        logger.info("Starting backend server...")
        subprocess.run(["uvicorn", "app.backend.api:app", "--host",
                        os.getenv("BACKEND_HOST"), "--port", 
                                os.getenv("BACKEND_PORT", "9999")], check=True)
    except CustomException as e:
        logger.error(f"Backend server error: {str(e)}")
        raise CustomException(error_message="Backend server failed to start", error_detail=e)
def run_frontend():
    try:
        logger.info("Starting frontend server...")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py"], check=True)
    except CustomException as e:
        logger.error(f"Frontend server error: {str(e)}")
        raise CustomException(error_message="Frontend server failed to start", error_detail=e)

if __name__ == "__main__":
    try:
        backend_thread = threading.Thread(target=run_backend)
        

        backend_thread.start()
        time.sleep(5)  # Ensure backend starts before frontend
        run_frontend()
    except CustomException as e:
        logger.critical(f"Application failed to start: {str(e)}")