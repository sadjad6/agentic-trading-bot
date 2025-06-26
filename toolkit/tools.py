import os
from datetime import datetime, timedelta
from langchain.tools import tool
from langchain_community.tools import TavilySearchResults
from langchain_community.tools.polygon.financials import PolygonFinancials
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults 
from data_models.models import RagToolSchema, StockAnalysisSchema, TechnicalAnalysisSchema
from langchain_pinecone import PineconeVectorStore
from utils.model_loaders import ModelLoader
from utils.config_loader import load_config
from dotenv import load_dotenv
from pinecone import Pinecone
import yfinance as yf
import pandas as pd
import ta

load_dotenv()
api_wrapper = PolygonAPIWrapper()
model_loader = ModelLoader()
config = load_config()

@tool(args_schema=RagToolSchema)
def retriever_tool(question):
    """Use this tool to retrieve information from the knowledge base about stock market concepts and company information."""
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=pinecone_api_key)
    vector_store = PineconeVectorStore(
        index=pc.Index(config["vector_db"]["index_name"]), 
        embedding=model_loader.load_embeddings()
    )
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": config["retriever"]["top_k"], "score_threshold": config["retriever"]["score_threshold"]},
    )
    return retriever.invoke(question)

@tool(args_schema=StockAnalysisSchema)
def stock_analysis_tool(symbol: str):
    """Use this tool to get comprehensive stock analysis including price, volume, and basic financial metrics."""
    stock = yf.Ticker(symbol)
    info = stock.info
    
    analysis = {
        "company_name": info.get("longName"),
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "dividend_yield": info.get("dividendYield"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
        "analyst_rating": info.get("recommendationKey"),
        "target_price": info.get("targetMeanPrice")
    }
    return analysis

@tool(args_schema=TechnicalAnalysisSchema)
def technical_analysis_tool(symbol: str):
    """Use this tool to perform technical analysis on a stock using various indicators."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    df = yf.download(symbol, start=start_date, end=end_date)
    
    # Calculate technical indicators
    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['MACD'] = ta.trend.MACD(df['Close']).macd()
    df['BB_upper'] = ta.volatility.BollingerBands(df['Close']).bollinger_hband()
    df['BB_lower'] = ta.volatility.BollingerBands(df['Close']).bollinger_lband()
    
    latest = df.iloc[-1]
    analysis = {
        "current_price": latest['Close'],
        "rsi": latest['RSI'],
        "macd": latest['MACD'],
        "bollinger_upper": latest['BB_upper'],
        "bollinger_lower": latest['BB_lower'],
        "volume": latest['Volume'],
        "50_day_ma": df['Close'].rolling(window=50).mean().iloc[-1],
        "200_day_ma": df['Close'].rolling(window=200).mean().iloc[-1]
    }
    return analysis

tavilytool = TavilySearchResults(
    max_results=config["tools"]["tavily"]["max_results"],
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
)

financials_tool = PolygonFinancials(api_wrapper=api_wrapper)