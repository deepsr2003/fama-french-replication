import os
import config
from src.data_loader import load_data
from src.portfolio_constructor import construct_factors
from src.factor_analyzer import analyze_factors


def create_output_dirs():
    """Creates the necessary output directories if they don't exist."""
    os.makedirs(config.PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(config.PLOTS_DIR, exist_ok=True)
    os.makedirs(config.REPORTS_DIR, exist_ok=True)


def run_pipeline():
    """
    Executes the full Fama-French factor replication pipeline.
    """
    print("--- Starting Fama-French Factor Replication Pipeline ---")

    # 0. Setup
    create_output_dirs()

    # 1. Load Data
    price_data, fundamentals_data = load_data(
        tickers=config.TICKERS,
        start_date=config.START_DATE,
        end_date=config.END_DATE
    )

    # 2. Construct Portfolios and Factors
    factors = construct_factors(price_data, fundamentals_data)

    # 3. Analyze Factors and Generate Outputs
    analyze_factors(factors)

    print("\n--- Pipeline finished successfully. Check the /outputs folder. ---")


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        print(f"\nAn error occurred during the pipeline execution: {e}")
