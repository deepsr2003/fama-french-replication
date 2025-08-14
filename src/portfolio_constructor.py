import pandas as pd
import numpy as np
import config
import os  # <-- THIS IS THE FIX


def construct_factors(price_data, fundamentals_data):
    """
    Constructs the SMB and HML factors based on the Fama-French 2x3 sort.

    NOTE: This implementation performs one sort at the beginning. A true replication
    would rebalance annually (typically at the end of June). This is a simplification.

    Args:
        price_data (pd.DataFrame): DataFrame of monthly stock prices.
        fundamentals_data (pd.DataFrame): DataFrame of market cap and B/M ratios.

    Returns:
        pd.DataFrame: A DataFrame with the time-series of SMB and HML factor returns.
    """
    print("\nConstructing Fama-French 2x3 portfolios...")

    # --- 1. Calculate Monthly Returns ---
    monthly_returns = price_data.pct_change().iloc[1:]

    # --- 2. Assign Stocks to Portfolios ---
    size_breakpoint = fundamentals_data['MarketCap'].quantile(
        config.SIZE_QUANTILE)
    value_breakpoints = fundamentals_data['BookToMarket'].quantile(
        [config.VALUE_QUANTILE, config.GROWTH_QUANTILE])

    # Assign Size portfolio (Small or Big)
    fundamentals_data['Size'] = np.where(
        fundamentals_data['MarketCap'] <= size_breakpoint, 'Small', 'Big')

    # Assign Value portfolio (Low, Medium, or High)
    fundamentals_data['Value'] = pd.cut(
        fundamentals_data['BookToMarket'],
        bins=[-np.inf, value_breakpoints.iloc[0],
              value_breakpoints.iloc[1], np.inf],
        labels=['Low', 'Medium', 'High']
    )

    fundamentals_data['Portfolio'] = fundamentals_data['Size'] + \
        '/' + fundamentals_data['Value'].astype(str)
    print("Portfolio Assignments:\n",
          fundamentals_data['Portfolio'].value_counts())

    # --- 3. Calculate Returns for the Six Portfolios ---
    # NOTE: Using equal-weighting for simplicity. Fama-French use value-weighting.
    portfolio_returns = pd.DataFrame()
    for name, group in fundamentals_data.groupby('Portfolio'):
        tickers_in_portfolio = group.index
        # Ensure we only use tickers present in the monthly_returns columns
        valid_tickers = [
            t for t in tickers_in_portfolio if t in monthly_returns.columns]
        if valid_tickers:
            portfolio_returns[name] = monthly_returns[valid_tickers].mean(
                axis=1)

    # --- 4. Calculate SMB and HML Factor Returns ---
    small_caps_return = portfolio_returns[[
        'Small/Low', 'Small/Medium', 'Small/High']].mean(axis=1)
    big_caps_return = portfolio_returns[[
        'Big/Low', 'Big/Medium', 'Big/High']].mean(axis=1)

    smb_factor = small_caps_return - big_caps_return

    high_bm_return = portfolio_returns[['Small/High', 'Big/High']].mean(axis=1)
    low_bm_return = portfolio_returns[['Small/Low', 'Big/Low']].mean(axis=1)

    hml_factor = high_bm_return - low_bm_return

    factors = pd.DataFrame({'SMB': smb_factor, 'HML': hml_factor}).dropna()

    # Save intermediate data
    factors.to_csv(os.path.join(
        config.PROCESSED_DATA_DIR, 'final_factors.csv'))
    fundamentals_data.to_csv(os.path.join(
        config.PROCESSED_DATA_DIR, 'portfolio_assignments.csv'))

    return factors
