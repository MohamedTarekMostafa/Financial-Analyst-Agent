# 📈 AI Financial Analyst Agent

An intelligent autonomous agent that provides real-time stock market analysis and global financial news summaries. Built using **LangGraph** for orchestration and **Gemini 2.5- Flash** as the brain.

## 🚀 Features
- **Real-time Market Data**: Fetches live stock prices and daily changes using `yfinance`.
- **Global News Retrieval**: Searches the latest financial news using **Tavily AI**.
- **Stateful Conversation**: Remembers previous context for follow-up questions (Chat History).
- **Observability**: Full tracing, latency monitoring, and cost tracking via **Langfuse**.
- **Modern UI**: Clean and interactive chat interface built with **Streamlit**.

## 🧠 Architecture
The agent is designed as a **Stateful Graph**:
1. **LLM Node**: Decides whether to answer the user or call a tool.
2. **Tools Node**: Executes `get_market_data` or `web_search` based on the agent's decision.
3. **Conditional Edges**: Logic-based routing to manage the flow between thinking and acting.

## 🛠️ Tech Stack
- **Framework**: LangChain & LangGraph
- **LLM**: Google Gemini 1.5 Flash
- **Search API**: Tavily AI
- **Data Source**: Yahoo Finance (yfinance)
- **Monitoring**: Langfuse
- **Frontend**: Streamlit

## 📸 Screenshots
### User Interface
![Streamlit UI](path/to/your/ui-screenshot.png)

### Agent Logic (LangGraph)
![Agent Graph](path/to/your/graph-screenshot.png)
