import json
from volt.services.lang_agent import LangAgent
class LangService:        
    async def model_response(request_data):
        messages = request_data.get("messages", "")
        messages_all = [ (message["role"], message["content"]) for message in messages]
        data = json.loads('{"choices":[{"index":0,"delta":{"content":"placeholder"}}]}')
        lang_agent = LangAgent()
        for s in lang_agent.volt_graph.stream({"messages": messages_all}):
            if "supervisor" not in s:
                agent_response=[y for x,y in s.items()][0]
                content= agent_response['messages'][0]
                data["choices"][0]["delta"]["content"] = content
                yield f"data: {json.dumps(data)}\n"    
        data["choices"][0]["delta"]["content"] = None
        data["choices"][0]["finish_reason"] = "stop"
        yield f"data: {json.dumps(data,separators=(',', ':'))}\n\n"
        yield  f"data: [DONE]"
