# advisor.py
from langgraph.graph import StateGraph, END
from typing import TypedDict
from schemas import FinancialAdvice
from tools import get_stock_analysis, web_researcher
from groq import Groq
import os
import json


# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class AgentState(TypedDict):
    symbol: str
    stock_data: dict
    web_data: list
    recommendation: FinancialAdvice

# Create workflow graph
workflow = StateGraph(AgentState)

# Define nodes
def fetch_stock_data(state: AgentState):
    """Fetch raw stock data without formatting"""
    stock_data = get_stock_analysis(state["symbol"])
    print("\nRaw Stock Data:")
    print(json.dumps(stock_data, indent=2))
    return {"stock_data": stock_data}

def fetch_web_data(state: AgentState):
    """Fetch raw web data without formatting"""
    web_data = web_researcher(state["symbol"])
    print("\nRaw Web Data:")
    print(json.dumps(web_data, indent=2))
    return {"web_data": web_data}

def analyze_data(state: AgentState):
    """Pass raw data directly to LLM"""
    try:
        recommendation = generate_recommendation(
            state["symbol"],
            state["stock_data"], 
            state["web_data"]
        )
        return {"recommendation": recommendation}
    except Exception as e:
        print(f"Analysis Error: {str(e)}")
        raise

# Add nodes to workflow
workflow.add_node("get_stock", fetch_stock_data)
workflow.add_node("get_web", fetch_web_data)
workflow.add_node("analyze", analyze_data)

# Set up edges
workflow.set_entry_point("get_stock")
workflow.add_edge("get_stock", "get_web")
workflow.add_edge("get_web", "analyze")
workflow.add_edge("analyze", END)

# Compile the workflow
advisory_workflow = workflow.compile()

def generate_recommendation(symbol: str, stock_data: dict, web_data: list) -> FinancialAdvice:
    """Generate recommendation using raw data"""
    prompt = f"""
    As a certified financial analyst,
    Analyze {symbol} stock as a financial expert using this raw data:
    
    Stock Data: {stock_data}
    
    Web Results: {web_data}
    
    Provide detailed analysis with recommendation.
    1. Buy/Hold/Sell recommendation
    2. Clear rationale with numerical references
    4. Risk Factors: [List top 3 risks]

    Instructions: Your analysis should be data-driven and consider both the fundamental stock data and the latest news.
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="deepseek-r1-distill-qwen-32b",
        temperature=0.4,
        max_tokens=1000
    )

    return FinancialAdvice(
        symbol=symbol,
        analysis=response.choices[0].message.content
    )
