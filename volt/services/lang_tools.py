from typing import  Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel,Field

class DFSRetriever(BaseModel):
    """Input for the DFS Retriever."""

    query: str = Field(description="Search Text")
    
class DFSRetrieverResults(BaseTool):
    """Tool that searches the DFS vector database and returns matching documents."""

    name: str = "dfs_retriever"
    description: str = "Tool that searchies the DFS vector database and returns matching documents."
    args_schema: Type[BaseModel] = DFSRetriever

    def _run(self, query: str) -> str:
        """Use the tool."""
        
        results = "Confidential fields are bank account numbers, social security numbers, and credit card numbers."
        return results
    
    async def _arun(self, query: str) -> str:
    
        """Use the tool asynchronously."""
        raise NotImplementedError("Currently we do not support async call")

class AlationSearch(BaseModel):
    """Input for the Alation Search."""

    query: str = Field(description="Search Text")

class AlationSearchResults(BaseTool):
    """Tool that searches Alation for data models."""

    name: str = "alation_search"
    description: str = "Tool that searches alation for data models."
    args_schema: Type[BaseModel] = AlationSearch

    def _run(self, query: str) -> str:
        """Use the tool."""
        
        # Simulate a search result
        results = "Employee table has three fields - employee_id, employee_name, and employee_salary."
        return results
    
    async def _arun(self, query: str) -> str:
    
        """Use the tool asynchronously."""
        raise NotImplementedError("Currently we do not support async call")
    
class SharepointSearch(BaseModel):
    """Input for the Sharepoint Search."""

    query: str = Field(description="Search Text")

class SharepointSearchResults(BaseTool):
    """Tool that searches Sharepoint for data models."""

    name: str = "sharepoint_search"
    description: str = "Tool that searches Sharepoint for miscelenious discover assets."
    args_schema: Type[BaseModel] = SharepointSearch

    def _run(self, query: str) -> str:
        """Use the tool."""
        
        results = "Link to relevent docs from Sharepoint search. \noffice.com/docs/1234\noffice.com/docs/2345"
        return results
    
    async def _arun(self, query: str) -> str:
    
        """Use the tool asynchronously."""
        raise NotImplementedError("Currently we do not support async call")

class GeneralAnswer(BaseModel):
    """Default Conversation."""

    query: str = Field(description="Provide general respnse if a specific tool is not called.")

class GeneralAnswerResults(BaseTool):
    """Provide general response if a specific tool is not called."""

    name: str = "general_pass"
    description: str =  "You are Volt a helpful DFS assistant that provides access to internal data and insights.Provide general response if a specific tool is not called.DFS is Discover Financial Services.Do not provide information that you do not have access to"
    args_schema: Type[BaseModel] = GeneralAnswer

    def _run(self, query: str) -> str:
        """Use the tool."""
        
        results = query
        return results
    
    async def _arun(self, query: str) -> str:
    
        """Use the tool asynchronously."""
        raise NotImplementedError("Currently we do not support async call")    