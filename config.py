import os

# --- Project Root ---
# This finds the directory where config.py is located, which is our project root.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# --- Data & Ticker Settings ---
TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'JPM', 'JNJ', 'V', 'PG',
    'XOM', 'CVX', 'BAC', 'PFE', 'KO', 'PEP', 'HD', 'MCD', 'WMT', 'DIS'
]
START_DATE = '2015-01-01'
END_DATE = '2023-12-31'
MARKET_INDEX_TICKER = '^GSPC'

# --- Portfolio Construction Parameters ---
VALUE_QUANTILE = 0.3
GROWTH_QUANTILE = 0.7
SIZE_QUANTILE = 0.5

# --- File Paths (Outputs) ---
# Use os.path.join to build paths from the project root.
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')
PLOTS_DIR = os.path.join(PROJECT_ROOT, 'outputs', 'plots')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'outputs', 'reports')
