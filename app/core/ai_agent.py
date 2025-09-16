from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from app.config.settings import settings


def get_response_from_agent(llm_id,query, allow_search, system_prompt):
    llm = ChatGroq(model_name=llm_id, api_key=settings.GROQ_API_KEY)
    tools = [TavilySearchResults(api_key=settings.TAVILY_API_KEY)] if allow_search else []
    
    agent = create_react_agent(llm,
                                tools=tools)
    response = agent.invoke({"messages": query})
    messages = response.get("messages")
    
    ai_message = [msg for msg in messages if isinstance(msg, AIMessage)]
    return ai_message[-1]