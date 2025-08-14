import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os
import config


def run_regression(factor_returns, market_returns):
    """Performs a time-series regression of factor returns against market returns."""
    data = pd.concat([factor_returns, market_returns], axis=1).dropna()
    Y = data.iloc[:, 0]  # Factor return
    X = data.iloc[:, 1]  # Market return
    X = sm.add_constant(X)  # Add a constant (intercept) for alpha

    model = sm.OLS(Y, X).fit()
    return model


def analyze_factors(factors):
    """
    Analyzes the constructed factors by plotting their performance and running regressions.

    Args:
        factors (pd.DataFrame): DataFrame with SMB and HML factor returns.
    """
    print("\nAnalyzing factors and generating outputs...")

    # --- 1. Load Market Data ---
    # market_data = yf.download(config.MARKET_INDEX_TICKER, start=config.START_DATE,
    #                          end=config.END_DATE, interval='1mo')['Adj Close']
    # new code
    market_data = yf.download(config.MARKET_INDEX_TICKER, start=config.START_DATE,
                              end=config.END_DATE, interval='1mo')['Close']
    market_returns = market_data.pct_change().dropna()
    market_returns.name = 'Mkt'

    # --- 2. Generate Cumulative Performance Plot ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))
    (factors + 1).cumprod().plot(ax=ax)
    ax.set_title(
        'Cumulative Performance of Replicated SMB and HML Factors', fontsize=16)
    ax.set_ylabel('Cumulative Return')
    ax.set_xlabel('Date')
    ax.legend(['Size (SMB)', 'Value (HML)'])

    plot_path = os.path.join(
        config.PLOTS_DIR, 'cumulative_factors_performance.png')
    plt.savefig(plot_path)
    print(f"Performance plot saved to: {plot_path}")
    plt.close()

    # --- 3. Run Regressions and Save Reports ---
    # SMB Regression
    smb_model = run_regression(factors['SMB'], market_returns)
    smb_report_path = os.path.join(
        config.REPORTS_DIR, 'smb_regression_summary.txt')
    with open(smb_report_path, 'w') as f:
        f.write(str(smb_model.summary()))
    print(f"SMB regression summary saved to: {smb_report_path}")

    # HML Regression
    hml_model = run_regression(factors['HML'], market_returns)
    hml_report_path = os.path.join(
        config.REPORTS_DIR, 'hml_regression_summary.txt')
    with open(hml_report_path, 'w') as f:
        f.write(str(hml_model.summary()))
    print(f"HML regression summary saved to: {hml_report_path}")

    # Print a summary of the alphas
    smb_alpha = smb_model.params['const'] * 12
    hml_alpha = hml_model.params['const'] * 12
    print("\n--- Regression Results ---")
    print(f"Annualized SMB Alpha (Intercept): {smb_alpha:.4%}")
    print(f"Annualized HML Alpha (Intercept): {hml_alpha:.4%}")
