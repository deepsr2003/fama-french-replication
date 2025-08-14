import pandas as pd
import yfinance as yf
import config


def load_data(tickers, start_date, end_date):
    """
    Downloads and preprocesses stock price and fundamental data.

    NOTE: yfinance provides current fundamentals, not historical point-in-time data.
    This is a major simplification for this project. A rigorous academic replication
    would use a source like CRSP/Compustat for historical fundamentals.

    Args:
        tickers (list): List of stock tickers.
        start_date (str): Start date for price data.
        end_date (str): End date for price data.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: Monthly price data.
            - pd.DataFrame: Fundamental data (Market Cap, Book-to-Market).
    """
    print("Downloading monthly price data...")
    # price_data = yf.download(tickers, start=start_date,
    #                         end=end_date, interval='1mo')['Adj Close']
    # NEW CODE
    price_data = yf.download(tickers, start=start_date,
                             end=end_date, interval='1mo')['Close']
    # Drop columns that are all NaN
    price_data.dropna(axis=1, how='all', inplace=True)

    print("Downloading fundamental data...")
    fundamentals = {}
    valid_tickers = []
    for ticker in price_data.columns:
        try:
            info = yf.Ticker(ticker).info
            market_cap = info.get('marketCap')
            book_value_per_share = info.get('bookValue')
            shares_outstanding = info.get('sharesOutstanding')

            if all([market_cap, book_value_per_share, shares_outstanding, book_value_per_share > 0]):
                book_value = book_value_per_share * shares_outstanding
                fundamentals[ticker] = {
                    'MarketCap': market_cap,
                    'BookToMarket': book_value / market_cap
                }
                valid_tickers.append(ticker)
            else:
                print(f"Skipping {ticker}: Missing fundamental data.")
        except Exception as e:
            print(f"Could not get fundamentals for {ticker}: {e}")

    # Filter price data to only include stocks with valid fundamentals
    price_data = price_data[valid_tickers]

    df_fundamentals = pd.DataFrame.from_dict(fundamentals, orient='index')

    if df_fundamentals.empty:
        raise ValueError(
            "No valid fundamental data could be retrieved. The project cannot proceed.")

    print(f"\nSuccessfully loaded data for {len(df_fundamentals)} stocks.")
    return price_data, df_fundamentals
