from typing import  Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel,Field
from volt.mock_data import mock_alation_data ,mock_sharepoint_data ,mock_retriever_data

class DFSRetriever(BaseModel):
    """Input for the DFS Retriever."""

    query: str = Field(description="Search Text")
    
class DFSRetrieverResults(BaseTool):
    """Tool that searches the DFS vector database and returns matching documents.Answer about discover financial services."""

    name: str = "dfs_retriever"
    description: str = "Tool that searches the DFS vector database and returns matching documents."
    args_schema: Type[BaseModel] = DFSRetriever

    def _run(self, query: str) -> str:
        """Use the tool."""
        
        results = mock_retriever_data +"\nAI should not add external information to response"
        return results
    
    async def _arun(self, query: str) -> str:
    
        """Use the tool asynchronously."""
        raise NotImplementedError("Currently we do not support async call")

class AlationSearch(BaseModel):
    """Input for the Alation to search table and view definitons."""

    table_name: str = Field(description="Table Name")

class AlationSearchResults(BaseTool):
    """Tool that searches Alation for data models."""

    name: str = "alation_search"
    description: str = "Tool that searches alation for data models."
    args_schema: Type[BaseModel] = AlationSearch

    def _run(self, table_name: str) -> str:
        """Use the tool."""
        
        # Simulate a search result
        results = mock_alation_data
        return results
    
    async def _arun(self, table_name: str) -> str:
    
        """Use the tool asynchronously."""
        raise NotImplementedError("Currently we do not support async call")
    
class SharepointSearch(BaseModel):
    """Input for the Sharepoint Search."""

    document_search: str = Field(description="Document Search Text")

class SharepointSearchResults(BaseTool):
    """Tool that searches Microsoft Document or Web pages on Sharepoint."""

    name: str = "sharepoint_search"
    description: str = "Tool that searches Sharepoint for miscellaneous discover assets.Do not add title on own"
    args_schema: Type[BaseModel] = SharepointSearch

    def _run(self, document_search: str) -> str:
        """Use the tool."""
        
        results = mock_sharepoint_data
        return results
    
    async def _arun(self, query: str) -> str:
    
        """Use the tool asynchronously."""
        raise NotImplementedError("Currently we do not support async call")

class GeneralAnswer(BaseModel):
    """Default Conversation."""

    usr_msg: str = Field(description="Provide general respnose if a specific tool is not called.")

class GeneralAnswerResults(BaseTool):
    """Provide general response if a specific tool is not called."""

    name: str = "general_pass"
    description: str =  "You are Volt a helpful DFS assistant that provides access to internal data and insights.Provide general response if a specific tool is not called.DFS is Discover Financial Services.Do not provide information that you do not have access to"
    args_schema: Type[BaseModel] = GeneralAnswer

    def _run(self, usr_msg: str) -> str:
        """Use the tool."""
        
        results = usr_msg
        return results
    
    async def _arun(self, usr_msg: str) -> str:
    
        """Use the tool asynchronously."""
        raise NotImplementedError("Currently we do not support async call")    