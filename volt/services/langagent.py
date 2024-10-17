from pydantic import BaseModel
from typing import Literal
from typing import Sequence
from typing_extensions import TypedDict
import functools
import operator
from typing import Annotated
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import create_react_agent
from langtools import DFSRetrieverResults,AlationSearchResults,SharepointSearchResults,GeneralAnswerResults
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from config import Config

dfs_retriever_tool = DFSRetrieverResults()
alation_search_tool = AlationSearchResults()
sharepoint_search_tool = SharepointSearchResults()
general_answer_tool = GeneralAnswerResults()

members = ["DFS_Retriever", "Alation_Search", "Sharepoint_Search", "General_Answer"]
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers: {members}. Given the following user request,"
    " respond with the worker to act next only. Each worker will perform a"
    " task and respond with their results and status. If not relevant, default BYPASS with a general answer."
)
class routeResponse(BaseModel):
    next: Literal["DFS_Retriever", "Alation_Search", "Sharepoint_Search", "General_Answer"]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ]
).partial(options=str(members), members=", ".join(members))

llm = ChatOpenAI(model="gpt-4o",api_key=Config.OPENAI_API_KEY)

def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["messages"][-1].content, name=name)]
    }

def supervisor_agent(state):
    supervisor_chain = prompt | llm.with_structured_output(routeResponse)
    return supervisor_chain.invoke(state)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

dfs_retriever_agent = create_react_agent(llm, tools=[dfs_retriever_tool])
dfs_retriever_node = functools.partial(agent_node, agent=dfs_retriever_agent, name="DFS_Retriever")

alation_search_agent = create_react_agent(llm, tools=[alation_search_tool])
alation_search_node = functools.partial(agent_node, agent=alation_search_agent, name="Alation_Search")

sharepoint_search_agent = create_react_agent(llm, tools=[sharepoint_search_tool])
sharepoint_search_node = functools.partial(agent_node, agent=sharepoint_search_agent, name="Sharepoint_Search")

general_answer_agent = create_react_agent(llm, tools=[general_answer_tool])
general_answer_node = functools.partial(agent_node, agent=general_answer_agent, name="General_Answer")

workflow = StateGraph(AgentState)
workflow.add_node("DFS_Retriever", dfs_retriever_node)
workflow.add_node("Alation_Search", alation_search_node)
workflow.add_node("Sharepoint_Search", sharepoint_search_node)
workflow.add_node("General_Answer", general_answer_node)
workflow.add_node("supervisor", supervisor_agent)

conditional_map = {k: k for k in members}

workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
for member in members:
    workflow.add_edge(member, END)
workflow.add_edge(START, "supervisor")

volt_graph = workflow.compile()
try:
    image_data = volt_graph.get_graph().draw_mermaid_png()
    with open("assets/graph_image.png", "wb") as f:
        f.write(image_data)
except Exception:
    pass

# print("=========================================")
# for s in graph.stream({"messages": [HumanMessage(content="Provide list of alation fields.")]}):
#     print(s)
#     print("----")
# print("=========================================")
# for s in graph.stream({"messages": [HumanMessage(content="Retrieve the crtical items.")]},{"recursion_limit": 10}):
#     if "__end__" not in s:
#         print(s)
#         print("----")
# print("=========================================")
# for s in graph.stream({"messages": [HumanMessage(content="Retrieve sharepoint links.")]},{"recursion_limit": 10}):
#     if "__end__" not in s:
#         print(s)
#         print("----")
# print("=========================================")
# for s in graph.stream({"messages": [HumanMessage(content="How is the weather today.")]}):
#     print(s)
#     print("----")
