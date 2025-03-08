from langchain_community.tools.tavily_search import TavilySearchResults
import yfinance as yf

def get_stock_analysis(symbol: str) -> dict:
    """Get raw stock data with native Python types"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d").iloc[-1]
        return {
            "symbol": symbol,
            "price": float(hist['Close']),
            "pe_ratio": ticker.info.get('trailingPE', 'N/A'),
            "market_cap": ticker.info.get('marketCap', 'N/A'),
            "volume": int(hist['Volume'])
        }
    except Exception as e:
        return {"error": str(e)}

def web_researcher(symbol: str) -> list:
    """Return raw search results"""
    try:
        search = TavilySearchResults(max_results=3)
        return search.invoke(f"{symbol} stock news")
    except Exception as e:
        print(f"Search Error: {str(e)}")
        return []
