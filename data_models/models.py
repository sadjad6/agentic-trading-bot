from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict
class RagToolSchema(BaseModel):
    """Input for the RAG tool."""

    question: str = Field(
        ...,
        description="The question to ask the RAG tool.",
    )

class StockAnalysisSchema(BaseModel):
    """Input for the stock analysis tool."""

    symbol: str = Field(
        ...,
        description="The stock symbol to analyze.",
    )

class TechnicalAnalysisSchema(BaseModel):
    """Input for the technical analysis tool."""

    symbol: str = Field(
        ...,
        description="The stock symbol for technical analysis.",
    )
class QuestionRequest(BaseModel):
    question: str