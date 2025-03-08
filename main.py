# main.py
from advisor import advisory_workflow
from schemas import FinancialAdvice

from advisor import advisory_workflow

def display_advice(advice: FinancialAdvice):
    print("\n" + "="*50)
    print(f"Analysis for {advice.symbol}")
    print("="*50)
    print(advice.analysis)
    print("="*50)

def main():
    while True:
        symbol = input("\nEnter stock symbol (q to quit): ").strip().upper()
        if symbol == 'Q': break
        
        try:
            result = advisory_workflow.invoke({"symbol": symbol})
            display_advice(result["recommendation"])
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()