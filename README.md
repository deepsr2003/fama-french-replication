# Fama-French Factor Replication in Python

![Python](https://img.shields.io/badge/python-3.11-blue.svg)

An end-to-end quantitative finance project that replicates the seminal Fama-French 'Size' (SMB) and 'Value' (HML) factors. The model downloads real market data, constructs factor portfolios based on academic methodology, and performs statistical analysis to validate the factors' performance in the modern market (2015-2023).

### Key Findings & Results

The most interesting result was that for the 2015-2023 period, both the Size and Value factors produced a **statistically significant negative alpha**. This demonstrates that the historical premiums did not hold during this specific window, which was heavily dominated by large-cap growth stocks.

This project doesn't just replicate a model; it provides a real-world insight into how factor performance is cyclical and not guaranteed.

![Cumulative Factor Performance](https://github.com/deepsr2003/fama-french-replication/blob/main/outputs/plots/cumulative_factors_performance.png?raw=true)
*(This image will show up once you push your project to a repo with this exact name)*

### Core Concepts Demonstrated
*   **Quantitative Research:** Translating academic papers into a functional Python model.
*   **Data Wrangling:** Processing and cleaning time-series financial data using **Pandas**.
*   **Financial APIs:** Sourcing stock price and fundamental data programmatically using **yfinance**.
*   **Portfolio Construction:** Implementing a rules-based 2x3 sorting methodology to create factor-mimicking portfolios.
*   **Statistical Analysis:** Using **Statsmodels** to perform time-series regression, calculate alpha and beta, and interpret statistical significance (p-values, R-squared).
*   **Software Engineering:** Structuring a project with a clean, modular architecture (config, data loading, analysis separated).

### How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/deepsr2003/fama-french-replication.git
    cd fama-french-replication
    ```

2.  **Set up a virtual environment:**
    ```bash
    # For Unix/macOS
    python3 -m venv .venv
    source .venv/bin/activate

    # For Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the pipeline:**
    ```bash
    python -m src.main
    ```
    The script will create `data/` and `outputs/` directories, download the latest data, run the analysis, and save the results.

### Project Structure
```
fama_french_replication/
├── .gitignore
├── README.md
├── requirements.txt
├── config.py           # Central configuration for paths & parameters
│
├── outputs/            # Final plots and regression reports
│
└── src/                # Main source code
    ├── data_loader.py
    ├── portfolio_constructor.py
    ├── factor_analyzer.py
    └── main.py
```

### Limitations & Simplifications
This project is a demonstration of the methodology. For an academic-grade replication, the following improvements would be necessary:
*   **Data Source:** Use a point-in-time database like CRSP/Compustat instead of `yfinance` to avoid lookahead bias in fundamentals.
*   **Rebalancing:** Implement annual or monthly rebalancing instead of a single sort at the beginning of the period.
*   **Portfolio Weighting:** Use value-weighting (based on market cap) for portfolios instead of equal-weighting.
