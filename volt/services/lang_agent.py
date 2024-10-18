import os
import sys
import operator
import functools
from pydantic import BaseModel
from typing import Literal, Sequence, Annotated
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import create_react_agent
from volt.services.lang_tools import DFSRetrieverResults, AlationSearchResults, SharepointSearchResults, GeneralAnswerResults
from volt.config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class routeResponse(BaseModel):
    next: Literal["DFS_Retriever", "Alation_Search", "Sharepoint_Search", "General_Answer"]

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

class LangAgent:
    def __init__(self):
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        sys.path.insert(0, parent_dir)
        
        self.dfs_retriever_tool = DFSRetrieverResults()
        self.alation_search_tool = AlationSearchResults()
        self.sharepoint_search_tool = SharepointSearchResults()
        self.general_answer_tool = GeneralAnswerResults()

        self.members = ["DFS_Retriever", "Alation_Search", "Sharepoint_Search", "General_Answer"]
        self.system_prompt = (
            "You are Volt a helpful DFS assistant that provides access to internal data and insights."
            "DFS is Discover Financial Services, a financial services company."
            "You are a supervisor tasked with managing a conversation between the following workers: {members}."
            "Answer any question related to DFS using DFS_Retriever."
            "Answer any question related to Database or Tables using Alation_Search."
            "Answer any question related to internal documents using Sharepoint_Search."
            "Given the following user request, respond with the worker to act next." 
            "Each worker will perform a task and respond with their results and status."
            "If not relevant default to BYPASS."
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder(variable_name="messages"),
            ]
        ).partial(options=str(self.members), members=", ".join(self.members))

        self.llm = ChatOpenAI(model="gpt-4o", api_key=Config.OPENAI_API_KEY)

        self.dfs_retriever_agent = create_react_agent(self.llm, tools=[self.dfs_retriever_tool])
        self.dfs_retriever_node = functools.partial(self.agent_node, agent=self.dfs_retriever_agent, name="DFS_Retriever")

        self.alation_search_agent = create_react_agent(self.llm, tools=[self.alation_search_tool])
        self.alation_search_node = functools.partial(self.agent_node, agent=self.alation_search_agent, name="Alation_Search")

        self.sharepoint_search_agent = create_react_agent(self.llm, tools=[self.sharepoint_search_tool])
        self.sharepoint_search_node = functools.partial(self.agent_node, agent=self.sharepoint_search_agent, name="Sharepoint_Search")

        self.general_answer_agent = create_react_agent(self.llm, tools=[self.general_answer_tool])
        self.general_answer_node = functools.partial(self.agent_node, agent=self.general_answer_agent, name="General_Answer")

        self.workflow = StateGraph(AgentState)
        self.workflow.add_node("DFS_Retriever", self.dfs_retriever_node)
        self.workflow.add_node("Alation_Search", self.alation_search_node)
        self.workflow.add_node("Sharepoint_Search", self.sharepoint_search_node)
        self.workflow.add_node("General_Answer", self.general_answer_node)
        self.workflow.add_node("supervisor", self.supervisor_agent)

        self.conditional_map = {k: k for k in self.members}

        self.workflow.add_conditional_edges("supervisor", lambda x: x["next"], self.conditional_map)
        for member in self.members:
            self.workflow.add_edge(member, END)
        self.workflow.add_edge(START, "supervisor")

        self.volt_graph = self.workflow.compile()
        try:
            image_data = self.volt_graph.get_graph().draw_mermaid_png()
            with open("assets/graph_image.png", "wb") as f:
                f.write(image_data)
        except Exception:
            pass

    def agent_node(self, state, agent, name):
        result = agent.invoke(state)
        logger.info(f"Agent Called: {name}")
        return {
            "messages": [result["messages"][-1].content]
        }

    def supervisor_agent(self, state):
        supervisor_chain = self.prompt | self.llm.with_structured_output(routeResponse)
        return supervisor_chain.invoke(state)

if __name__ == "__main__":
    lang_agent = LangAgent()
    for s in lang_agent.volt_graph.stream({"messages": [HumanMessage(content="Provide list of alation fields.")]}):
        if "supervisor" not in s:
            agent_response=[y for x,y in s.items()][0]
            logger.info(agent_response['messages'][0])