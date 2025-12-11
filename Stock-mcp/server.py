from mcp.server.fastmcp import FastMCP
import yfinance as yf
import time
import asyncio
from functools import partial

# Initialize FastMCP server
mcp = FastMCP("Stock Analyst")

# --- Caching System ---
# Simple in-memory cache: {key: (data, timestamp)}
CACHE = {}
DEFAULT_TTL = 300  # 5 minutes (300 seconds)

def get_from_cache(key: str, ttl: int = DEFAULT_TTL):
    """Retrieve value from cache if it exists and hasn't expired."""
    if key in CACHE:
        data, timestamp = CACHE[key]
        if time.time() - timestamp < ttl:
            return data
        else:
            del CACHE[key]  # Remove expired item
    return None

def set_to_cache(key: str, data):
    """Save value to cache with current timestamp."""
    CACHE[key] = (data, time.time())

async def run_blocking(func, *args, **kwargs):
    """
    Run a blocking (synchronous) function in a separate thread.
    This prevents 'yfinance' from freezing the entire MCP server while waiting for data.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))

# --- Sync Helper Functions (The actual work) ---

def _fetch_stock_price(symbol: str) -> str:
    try:
        ticker = yf.Ticker(symbol)
        # fast_info is often faster than .info for current price
        price = ticker.fast_info.last_price
        currency = ticker.fast_info.currency
        
        if price is None:
            # Fallback to regular info
            info = ticker.info
            price = info.get('currentPrice') or info.get('regularMarketPrice')
            currency = info.get('currency', 'USD')

        if price is None:
             return f"Could not fetch price for {symbol}. Please check the symbol."

        return f"The current price of {symbol.upper()} is {price:.2f} {currency}."
    except Exception as e:
        return f"Error fetching stock price for {symbol}: {str(e)}"

def _fetch_company_info(symbol: str) -> str:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        name = info.get('longName', symbol)
        sector = info.get('sector', 'Unknown')
        industry = info.get('industry', 'Unknown')
        summary = info.get('longBusinessSummary', 'No summary available.')
        
        return f"**{name}**\nSector: {sector}\nIndustry: {industry}\n\nSummary: {summary[:500]}..."
    except Exception as e:
        return f"Error fetching company info for {symbol}: {str(e)}"

def _fetch_stock_history(symbol: str, period: str) -> str:
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=period)
        
        if history.empty:
            return f"No historical data found for {symbol} with period {period}."
        
        # Format the history as a readable string
        result = f"Historical data for {symbol.upper()} ({period}):\n\n"
        result += "| Date | Open | High | Low | Close | Volume |\n"
        result += "|---|---|---|---|---|---|\n"
        
        for date, row in history.iterrows():
            date_str = date.strftime('%Y-%m-%d')
            result += f"| {date_str} | {row['Open']:.2f} | {row['High']:.2f} | {row['Low']:.2f} | {row['Close']:.2f} | {row['Volume']} |\n"
            
        return result
    except Exception as e:
        return f"Error fetching history for {symbol}: {str(e)}"

# --- MCP Tool Definitions (Async Wrappers) ---

@mcp.tool()
async def get_stock_price(symbol: str) -> str:
    """
    Get the current stock price for a given symbol (Cached for 5 mins).
    Args:
        symbol: The stock ticker symbol (e.g., 'AAPL', 'GOOGL').
    """
    cache_key = f"price_{symbol.upper()}"
    cached_result = get_from_cache(cache_key)
    if cached_result:
        return cached_result + " (Cached)"

    # Run the blocking fetch in a thread
    result = await run_blocking(_fetch_stock_price, symbol)
    
    if "Error" not in result and "Could not" not in result:
        set_to_cache(cache_key, result)
        
    return result

@mcp.tool()
async def get_company_info(symbol: str) -> str:
    """
    Get company information including sector, industry, and summary (Cached).
    Args:
        symbol: The stock ticker symbol.
    """
    cache_key = f"info_{symbol.upper()}"
    cached_result = get_from_cache(cache_key)
    if cached_result:
        return cached_result + " (Cached)"

    result = await run_blocking(_fetch_company_info, symbol)
    
    if "Error" not in result:
        set_to_cache(cache_key, result)
        
    return result

@mcp.tool()
async def get_stock_history(symbol: str, period: str = "1mo") -> str:
    """
    Get historical stock data for a given period (Cached).
    Args:
        symbol: The stock ticker symbol.
        period: The data period (e.g., '1d', '5d', '1mo', '1y').
    """
    cache_key = f"history_{symbol.upper()}_{period}"
    cached_result = get_from_cache(cache_key)
    if cached_result:
        return cached_result + " (Cached)"

    result = await run_blocking(_fetch_stock_history, symbol, period)
    
    if "Error" not in result:
        set_to_cache(cache_key, result)
        
    return result

if __name__ == "__main__":
    mcp.run()
