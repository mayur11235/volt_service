import json
from volt.config import Config
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

model = ChatOpenAI(model="gpt-4",api_key=Config.OPENAI_API_KEY)

class LangService:        
    async def model_response(request_data):
        messages = request_data.get("messages", "")
        messages_all = [ (message["role"], message["content"]) for message in messages]
        system_message=("system", "You are Volt a helpful DFS buddy that provides access to internal data and insights")
        messages_all.insert(0,system_message)
        prompt = ChatPromptTemplate.from_messages(messages_all)
        data = json.loads('{"choices":[{"index":0,"delta":{"content":"placeholder"}}]}')
        chain = prompt | model
        for s in chain.stream({}):
            data["choices"][0]["delta"]["content"] = s.content
            yield f"data: {json.dumps(data)}\n"
        data["choices"][0]["delta"]["content"] = None
        data["choices"][0]["finish_reason"] = "stop"
        yield f"data: {json.dumps(data,separators=(',', ':'))}\n\n"
        yield  f"data: [DONE]"