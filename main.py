from fastapi import FastAPI
from pydantic import BaseModel
from agent import create_agent
from dotenv import load_dotenv
load_dotenv(".env")
from langfuse.langchain import CallbackHandler
langfuse_handler = CallbackHandler()
config = {
                    "configurable": {"thread_id": "st_session_v1"},
                    "callbacks": [langfuse_handler],
                    "run_name": "Financial_Query_Execution"
}
load_dotenv(".env")
bot = create_agent()
app = FastAPI()
class request_schema(BaseModel):
    question : str
@app.post("/ask")
def request(request:request_schema):
    inputs = {"messages": [("user", request.question)]}
    result = bot.invoke(inputs, config)
    final_messages = result['messages'][-1].content
    return  {"messages":final_messages}
