# Agentic Trading Bot

This project is an advanced trading assistant that combines large language models (LLM) with real-time financial analysis tools. It provides comprehensive stock market insights through a FastAPI backend and an intuitive Streamlit UI.

## Features

- **Advanced Financial Analysis**:
  - Real-time stock data analysis with fundamental metrics
  - Technical analysis with indicators (RSI, MACD, Bollinger Bands)
  - Market sentiment and analyst recommendations

- **Intelligent Routing System**:
  - Context-aware query processing
  - Automatic tool selection based on query type
  - Seamless integration of multiple data sources

- **Enhanced UI/UX**:
  - Two-column layout with dedicated analysis panel
  - Quick stock analysis feature
  - Context-aware conversations
  - Real-time market data visualization

- **Core Infrastructure**:
  - **FastAPI Backend**: RESTful API for document processing and market analysis
  - **Streamlit UI**: Modern, responsive interface for market interaction
  - **RAG Pipeline**: Document ingestion and retrieval system
  - **LangGraph Agent**: Advanced routing and tool coordination

## Project Structure

```
├── agent/               # LangGraph agent with routing system
├── config/              # Configuration files
├── data_ingestion/      # Enhanced data ingestion pipeline
├── data_models/         # Extended Pydantic models
├── exception/           # Custom exceptions
├── main.py              # FastAPI application
├── prompt_library/      # Prompt templates and routing logic
├── requirements.txt     # Project dependencies
├── setup.py             # Setup script
├── streamlit_ui.py      # Advanced Streamlit UI
├── toolkit/             # Financial analysis tools
└── utils/               # Utility functions
```

## Getting Started

### Prerequisites

- Python 3.10
- Conda
- API Keys for financial data and AI services

### Installation

1. **Create a Conda environment:**

   ```bash
   conda create -p env python=3.10 -y
   ```

2. **Activate the environment:**

   - **CMD:**
     ```bash
     conda activate ./env
     ```
   - **Git Bash:**
     ```bash
     source activate ./env
     ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory (use `.env.example` as a template) and add the following keys:

   ```
   POLYGON_API_KEY      # For financial data access
   GOOGLE_API_KEY       # For embeddings and LLM
   TAVILY_API_KEY       # For web search
   GROQ_API_KEY         # For fast LLM inference
   PINECONE_API_KEY     # For vector storage
   ```

### Key Dependencies

- **Data Analysis**: yfinance, pandas, ta
- **AI/ML**: langchain, langgraph, pinecone-client
- **API**: fastapi, uvicorn
- **UI**: streamlit

### Running the Application

1. **Start the FastAPI backend:**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start the Streamlit UI:**

   ```bash
   streamlit run streamlit_ui.py
   ```

## Usage

1. **Quick Stock Analysis:**
   - Enter a stock symbol in the analysis panel to get instant insights.
   - Select from basic, technical, or combined analysis types.

2. **Document Upload:**
   - Upload relevant financial documents (PDF, DOCX) to enhance the bot's knowledge base.

3. **Interactive Chat:**
   - Ask questions about specific stocks, market trends, or trading strategies.
   - The bot will use its tools and knowledge base to provide comprehensive answers.

## Development Roadmap

### Completed

- **Advanced Financial Tools**: Integrated real-time stock analysis and technical indicators.
- **Intelligent Routing**: Implemented a context-aware routing system.
- **Enhanced UI**: Redesigned the Streamlit interface for a better user experience.

### Next Steps

- **Real-time Data Visualization**: Add interactive charts and graphs to the UI.
- **Backtesting Engine**: Develop a backtesting module to evaluate trading strategies.
- **Portfolio Management**: Implement features for tracking and managing a virtual portfolio.
- **Enhanced Security**: Strengthen API security and data protection measures.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.