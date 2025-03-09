# main.py
import streamlit as st
from advisor import advisory_workflow
from tools import get_stock_analysis, web_researcher
import os
from dotenv import load_dotenv
import yfinance as yf
import datetime

# Load environment variables
load_dotenv()

# Streamlit UI Configuration
st.set_page_config(
    page_title="AI Stock Advisor",
    page_icon="📈",
    layout="wide"
)

def main():
    st.title("📈 AI Stock Advisor")
    st.markdown("Get real-time stock analysis powered by GROQ and our AI workflow.")

    # Input for stock symbol
    symbol = st.text_input("Enter stock symbol (e.g. AAPL, NVDA):").upper().strip()

    if st.button("Analyze", type="primary"):
        if not symbol or len(symbol) < 1:
            st.error("Please enter a valid stock symbol")
            return

        with st.spinner(f"Analyzing {symbol}..."):
            try:
                # Run the analysis workflow from advisor.py
                result = advisory_workflow.invoke({"symbol": symbol})
                advice = result["recommendation"]

                # Display raw data for verification
                with st.expander("Raw Stock Data", expanded=False):
                    raw_stock = get_stock_analysis(symbol)
                    st.json(raw_stock)
                with st.expander("Raw Web Data", expanded=False):
                    raw_web = web_researcher(symbol)
                    st.json(raw_web)

                # Display the AI analysis report
                st.subheader(f"Analysis Report for {symbol}")
                st.markdown(advice.analysis)

                # New: Display a graph of the stock's performance over the past year using Altair
                st.subheader("Stock Price Trend (Last 1 Year)")
                ticker = yf.Ticker(symbol)
                # Retrieve historical data for the last year
                df = ticker.history(period='1y')
                if not df.empty:
                    df = df.reset_index()  # reset index so Date becomes a column
                    chart = alt.Chart(df).mark_line(point=True).encode(
                        x=alt.X('Date:T', title='Date'),
                        y=alt.Y('Close:Q', title='Closing Price'),
                        tooltip=['Date:T', 'Close:Q']
                    ).properties(
                        title=f"{symbol} Stock Price - Last 1 Year",
                        width=700,
                        height=400
                    )
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info("Unable to fetch historical price data for the past year.")

            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                st.stop()

if __name__ == "__main__":
    main()
