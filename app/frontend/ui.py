import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
API_URL = f"http://{settings.BACKEND_HOST}:{settings.BACKEND_PORT}/chat"
st.set_page_config(page_title="Multi-Agent Chat", page_icon="🤖")
st.title("Multi-Agent Chat Application with TAvily 🤖")
st.markdown("Interact with various AI models and leverage web search capabilities.")

system_prompt = st.text_area("Define your AI agent", value="You are a helpful assistant.", height=70)
selected_model = st.selectbox("Select AI Model", settings.ALLOWED_MODELS_NAMES)
allow_search = st.checkbox("Enable Web Search", value=False)
user_query = st.text_area("Enter your query", height=150)

if st.button("Ask Agent") and user_query.strip():
    try:
        payload = {
            "model_name": selected_model,
            "messages": [user_query],
            "allow_search": allow_search,
            "system_prompt": [system_prompt]
        }
        with st.spinner("Generating response..."):
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            ai_response = data.get("response", {}).get("content", "No response content.")
        st.subheader("Agent Response")
        st.markdown(ai_response.replace("\n", "<br>"), unsafe_allow_html=True)
        logger.info(f"Response successfully generated for model {selected_model}")
    except requests.exceptions.RequestException as req_err:
        error_message = f"Request error: {str(req_err)}"
        st.error(error_message)
        logger.error(error_message)
    except Exception as e:
        custom_error = CustomException(error_message=str(e), error_detail=e)
        st.error(f"An unexpected error occurred: {str(custom_error)}")
        logger.error(f"Unexpected error: {str(custom_error)}")  