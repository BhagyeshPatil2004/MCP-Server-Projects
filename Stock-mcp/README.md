# 📈 Stock Analyst MCP Server

> **Note:** This tool is designed exclusively for **Stock Market Data**. It connects your AI assistant to real-time financial information, allowing it to "see" current prices and company details that are otherwise outside its training data.

A Model Context Protocol (MCP) server that provides real-time stock prices, historical data, and company information using `yfinance`.

## 🚀 Features

- **Get Stock Price**: Fetch real-time prices for any stock (e.g., AAPL, TSLA, BTC-USD).
- **Company Info**: detailed summaries, sectors, and industry information.
- **Historical Data**: Retrieve past performance data (Open, High, Low, Close, Volume).
- **Smart Caching**: Built-in 5-minute cache to prevent API throttling and ensure fast responses.
- **Async Support**: Non-blocking data fetching for high performance.

## 🛠️ Installation

1.  **Install dependencies** (if running locally):
    ```bash
    pip install mcp yfinance
    ```
    *Note: If using `uv` (recommended), these are handled automatically via the configuration.*

2.  **Configure Claude Desktop**:
    Add the following to your `claude_desktop_config.json`:

    ```json
    "stock-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--quiet",
        "--with",
        "mcp",
        "--with",
        "yfinance",
        "C:\\Agent MCP\\Stock-mcp\\server.py"
      ]
    }
    ```
    *(Make sure to update the path if your folder location is different!)*

## 💡 How to Use

Once connected, you can ask Claude questions like:

*   "What is the current price of **NVIDIA**?"
*   "Show me the stock history of **Apple** for the last month."
*   "What sector is **Palantir** in and what do they do?"
*   "Compare the performance of **Google** vs **Microsoft** this week."

## 🔧 Technical Details

*   **tools**:
    *   `get_stock_price(symbol)`
    *   `get_company_info(symbol)`
    *   `get_stock_history(symbol, period)`
*   **Infrastructure**: Python, FastMCP, asyncio.
*   **Data Source**: Yahoo Finance (free).
