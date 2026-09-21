import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import norm
from scipy.stats import chi2

# ----------------------------------
# Portfolio settings
# ----------------------------------

tickers = ["AAPL", "GLD", "JNJ", "JPM", "XOM"]

weights = np.array([
    0.1975,   # AAPL
    0.6447,   # GLD
    0.0000,   # JNJ
    0.1305,   # JPM
    0.0272    # XOM
])

portfolio_value = 1_000_000

start_date = "2020-01-01"
end_date = "2026-01-01"


# ----------------------------------
# Download historical prices
# ----------------------------------

prices = yf.download(
    tickers,
    start=start_date,
    end=end_date,
    auto_adjust=False
)["Adj Close"]

print("First five rows:")
print(prices.head())

# ----------------------------------
# Calculate daily asset returns
# ----------------------------------

daily_returns = prices.pct_change().dropna()

print("\nFirst five daily returns:")
print(daily_returns.head())

# ----------------------------------
# Calculate portfolio daily returns
# ----------------------------------

portfolio_returns = daily_returns @ weights

print("\nFirst five portfolio daily returns:")
print(portfolio_returns.head())

# ----------------------------------
# Calculate daily portfolio P&L
# ----------------------------------

portfolio_pnl = portfolio_returns * portfolio_value

print("\nFirst five daily portfolio P&L:")
print(portfolio_pnl.head())

# ----------------------------------
# Historical Value at Risk
# ----------------------------------

var_95_return = np.percentile(portfolio_returns, 5)
var_99_return = np.percentile(portfolio_returns, 1)

var_95_dollar = -var_95_return * portfolio_value
var_99_dollar = -var_99_return * portfolio_value

print("\nHistorical VaR:")
print(f"95% VaR Return: {var_95_return:.4%}")
print(f"95% VaR ($): ${var_95_dollar:,.2f}")

print(f"\n99% VaR Return: {var_99_return:.4%}")
print(f"99% VaR ($): ${var_99_dollar:,.2f}")

# ----------------------------------
# Expected Shortfall (CVaR)
# ----------------------------------

es_95_return = portfolio_returns[
    portfolio_returns <= var_95_return
].mean()

es_99_return = portfolio_returns[
    portfolio_returns <= var_99_return
].mean()

es_95_dollar = -es_95_return * portfolio_value
es_99_dollar = -es_99_return * portfolio_value

print("\nExpected Shortfall (CVaR):")

print(f"95% ES Return: {es_95_return:.4%}")
print(f"95% ES ($): ${es_95_dollar:,.2f}")

print(f"\n99% ES Return: {es_99_return:.4%}")
print(f"99% ES ($): ${es_99_dollar:,.2f}")

# ----------------------------------
# Parametric Value at Risk
# ----------------------------------

mean_return = portfolio_returns.mean()
std_return = portfolio_returns.std()

z_95 = norm.ppf(0.05)
z_99 = norm.ppf(0.01)

parametric_var_95_return = mean_return + z_95 * std_return
parametric_var_99_return = mean_return + z_99 * std_return

parametric_var_95_dollar = -parametric_var_95_return * portfolio_value
parametric_var_99_dollar = -parametric_var_99_return * portfolio_value

print("\nPortfolio daily statistics:")
print(f"Mean daily return: {mean_return:.4%}")
print(f"Daily volatility: {std_return:.4%}")

print("\nParametric VaR:")
print(f"95% VaR Return: {parametric_var_95_return:.4%}")
print(f"95% VaR ($): ${parametric_var_95_dollar:,.2f}")

print(f"\n99% VaR Return: {parametric_var_99_return:.4%}")
print(f"99% VaR ($): ${parametric_var_99_dollar:,.2f}")

# ----------------------------------
# Monte Carlo Value at Risk
# ----------------------------------

np.random.seed(42)

num_simulations = 100_000

simulated_returns = np.random.normal(
    loc=mean_return,
    scale=std_return,
    size=num_simulations
)

monte_carlo_var_95_return = np.percentile(simulated_returns, 5)
monte_carlo_var_99_return = np.percentile(simulated_returns, 1)

monte_carlo_var_95_dollar = (
    -monte_carlo_var_95_return * portfolio_value
)

monte_carlo_var_99_dollar = (
    -monte_carlo_var_99_return * portfolio_value
)

print("\nMonte Carlo VaR:")

print(
    f"95% VaR Return: "
    f"{monte_carlo_var_95_return:.4%}"
)
print(
    f"95% VaR ($): "
    f"${monte_carlo_var_95_dollar:,.2f}"
)

print(
    f"\n99% VaR Return: "
    f"{monte_carlo_var_99_return:.4%}"
)
print(
    f"99% VaR ($): "
    f"${monte_carlo_var_99_dollar:,.2f}"
)

# ----------------------------------
# Compare VaR methods
# ----------------------------------

var_comparison = pd.DataFrame({
    "Method": [
        "Historical",
        "Parametric",
        "Monte Carlo"
    ],
    "95% VaR ($)": [
        var_95_dollar,
        parametric_var_95_dollar,
        monte_carlo_var_95_dollar
    ],
    "99% VaR ($)": [
        var_99_dollar,
        parametric_var_99_dollar,
        monte_carlo_var_99_dollar
    ]
})

print("\nVaR Method Comparison:")
print(var_comparison)

# ----------------------------------
# Plot VaR comparison
# ----------------------------------

var_chart = var_comparison.set_index("Method")

ax = var_chart.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("1-Day Value at Risk by Method")
plt.ylabel("VaR ($)")
plt.xlabel("Method")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "charts/var_method_comparison.png",
    dpi=300
)

plt.show()

# ----------------------------------
# Historical 10-Day VaR
# ----------------------------------

rolling_10d_returns = (
    (1 + portfolio_returns)
    .rolling(window=10)
    .apply(np.prod, raw=True)
    - 1
)

rolling_10d_returns = rolling_10d_returns.dropna()

historical_10d_var_95_return = np.percentile(
    rolling_10d_returns, 5
)

historical_10d_var_99_return = np.percentile(
    rolling_10d_returns, 1
)

historical_10d_var_95_dollar = (
    -historical_10d_var_95_return * portfolio_value
)

historical_10d_var_99_dollar = (
    -historical_10d_var_99_return * portfolio_value
)

print("\nHistorical 10-Day VaR:")

print(
    f"95% VaR Return: "
    f"{historical_10d_var_95_return:.4%}"
)

print(
    f"95% VaR ($): "
    f"${historical_10d_var_95_dollar:,.2f}"
)

print(
    f"\n99% VaR Return: "
    f"{historical_10d_var_99_return:.4%}"
)

print(
    f"99% VaR ($): "
    f"${historical_10d_var_99_dollar:,.2f}"
)

# ----------------------------------
# Parametric 10-Day VaR
# ----------------------------------

days = 10

mean_return_10d = mean_return * days

std_return_10d = std_return * np.sqrt(days)

parametric_10d_var_95_return = (
    mean_return_10d
    + z_95 * std_return_10d
)

parametric_10d_var_99_return = (
    mean_return_10d
    + z_99 * std_return_10d
)

parametric_10d_var_95_dollar = (
    -parametric_10d_var_95_return
    * portfolio_value
)

parametric_10d_var_99_dollar = (
    -parametric_10d_var_99_return
    * portfolio_value
)

print("\nParametric 10-Day VaR:")

print(
    f"95% VaR Return: "
    f"{parametric_10d_var_95_return:.4%}"
)

print(
    f"95% VaR ($): "
    f"${parametric_10d_var_95_dollar:,.2f}"
)

print(
    f"\n99% VaR Return: "
    f"{parametric_10d_var_99_return:.4%}"
)

print(
    f"99% VaR ($): "
    f"${parametric_10d_var_99_dollar:,.2f}"
)

# ----------------------------------
# Monte Carlo 10-Day VaR
# ----------------------------------

np.random.seed(42)

num_simulations = 100_000
days = 10

simulated_daily_returns = np.random.normal(
    loc=mean_return,
    scale=std_return,
    size=(num_simulations, days)
)

simulated_10d_returns = (
    np.prod(
        1 + simulated_daily_returns,
        axis=1
    )
    - 1
)

monte_carlo_10d_var_95_return = np.percentile(
    simulated_10d_returns,
    5
)

monte_carlo_10d_var_99_return = np.percentile(
    simulated_10d_returns,
    1
)

monte_carlo_10d_var_95_dollar = (
    -monte_carlo_10d_var_95_return
    * portfolio_value
)

monte_carlo_10d_var_99_dollar = (
    -monte_carlo_10d_var_99_return
    * portfolio_value
)

print("\nMonte Carlo 10-Day VaR:")

print(
    f"95% VaR Return: "
    f"{monte_carlo_10d_var_95_return:.4%}"
)

print(
    f"95% VaR ($): "
    f"${monte_carlo_10d_var_95_dollar:,.2f}"
)

print(
    f"\n99% VaR Return: "
    f"{monte_carlo_10d_var_99_return:.4%}"
)

print(
    f"99% VaR ($): "
    f"${monte_carlo_10d_var_99_dollar:,.2f}"
)

# ----------------------------------
# Compare 1-Day and 10-Day VaR
# ----------------------------------

horizon_comparison = pd.DataFrame({
    "Method": [
        "Historical",
        "Parametric",
        "Monte Carlo"
    ],

    "1-Day 95% VaR ($)": [
        var_95_dollar,
        parametric_var_95_dollar,
        monte_carlo_var_95_dollar
    ],

    "10-Day 95% VaR ($)": [
        historical_10d_var_95_dollar,
        parametric_10d_var_95_dollar,
        monte_carlo_10d_var_95_dollar
    ],

    "1-Day 99% VaR ($)": [
        var_99_dollar,
        parametric_var_99_dollar,
        monte_carlo_var_99_dollar
    ],

    "10-Day 99% VaR ($)": [
        historical_10d_var_99_dollar,
        parametric_10d_var_99_dollar,
        monte_carlo_10d_var_99_dollar
    ]
})

print("\n1-Day vs 10-Day VaR:")
print(horizon_comparison)

# ----------------------------------
# Plot 1-Day vs 10-Day VaR
# ----------------------------------

horizon_chart = horizon_comparison.set_index("Method")

ax = horizon_chart.plot(
    kind="bar",
    figsize=(12, 7)
)

plt.title("1-Day vs 10-Day Value at Risk")
plt.ylabel("VaR ($)")
plt.xlabel("Method")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "charts/var_horizon_comparison.png",
    dpi=300
)

plt.show()

# ----------------------------------
# Historical Stress Testing
# ----------------------------------

worst_days = portfolio_returns.nsmallest(10)

worst_days_df = pd.DataFrame({
    "Portfolio Return": worst_days,
    "Loss ($)": -worst_days * portfolio_value
})

worst_days_df["Portfolio Return (%)"] = (
    worst_days_df["Portfolio Return"] * 100
)

worst_days_df = worst_days_df[
    [
        "Portfolio Return (%)",
        "Loss ($)"
    ]
]

print("\n10 Worst Portfolio Trading Days:")
print(worst_days_df)

# ----------------------------------
# Worst Historical 10-Day Periods
# ----------------------------------

worst_10d_periods = rolling_10d_returns.nsmallest(10)

worst_10d_df = pd.DataFrame({
    "10-Day Return": worst_10d_periods,
    "Loss ($)": -worst_10d_periods * portfolio_value
})

worst_10d_df["10-Day Return (%)"] = (
    worst_10d_df["10-Day Return"] * 100
)

worst_10d_df = worst_10d_df[
    [
        "10-Day Return (%)",
        "Loss ($)"
    ]
]

print("\n10 Worst Rolling 10-Day Periods:")
print(worst_10d_df)

# ----------------------------------
# Hypothetical Stress Testing
# ----------------------------------

stress_scenarios = pd.DataFrame(
    {
        "AAPL": [-0.15, -0.05, -0.20],
        "GLD":  [0.05, -0.12, -0.08],
        "JNJ":  [-0.05, -0.03, -0.08],
        "JPM":  [-0.12, -0.05, -0.18],
        "XOM":  [-0.10, -0.06, -0.15]
    },
    index=[
        "Equity Sell-Off",
        "Gold Correction",
        "Broad Market Shock"
    ]
)

print("\nHypothetical Stress Scenarios:")
print(stress_scenarios)

# ----------------------------------
# Calculate stress scenario impact
# ----------------------------------

stress_portfolio_returns = stress_scenarios @ weights

stress_results = pd.DataFrame({
    "Portfolio Return (%)":
        stress_portfolio_returns * 100,

    "Portfolio P&L ($)":
        stress_portfolio_returns * portfolio_value
})

print("\nHypothetical Stress Test Results:")
print(stress_results)

# ----------------------------------
# Plot hypothetical stress tests
# ----------------------------------

stress_results["Portfolio P&L ($)"].plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Portfolio Impact Under Hypothetical Stress Scenarios")
plt.ylabel("Portfolio P&L ($)")
plt.xlabel("Scenario")
plt.xticks(rotation=0)

plt.axhline(
    y=0,
    linewidth=1
)

plt.tight_layout()

plt.savefig(
    "charts/hypothetical_stress_test.png",
    dpi=300
)

plt.show()

# ----------------------------------
# Stress Contribution by Asset
# ----------------------------------

stress_contributions = stress_scenarios.mul(
    weights,
    axis=1
)

stress_contributions_pct = (
    stress_contributions * 100
)

print("\nStress Contribution by Asset (% points):")
print(stress_contributions_pct)

stress_contributions_dollar = (
    stress_contributions
    * portfolio_value
)

print("\nStress Contribution by Asset ($):")
print(stress_contributions_dollar)

# ----------------------------------
# VaR Backtesting
# ----------------------------------

window = 252

rolling_mean = (
    portfolio_returns
    .rolling(window=window)
    .mean()
    .shift(1)
)

rolling_std = (
    portfolio_returns
    .rolling(window=window)
    .std()
    .shift(1)
)

var_95_threshold = (
    rolling_mean
    + z_95 * rolling_std
)

var_99_threshold = (
    rolling_mean
    + z_99 * rolling_std
)

backtest = pd.DataFrame({
    "Portfolio Return": portfolio_returns,
    "95% VaR Threshold": var_95_threshold,
    "99% VaR Threshold": var_99_threshold
})

backtest = backtest.dropna()

backtest["95% Breach"] = (
    backtest["Portfolio Return"]
    < backtest["95% VaR Threshold"]
)

backtest["99% Breach"] = (
    backtest["Portfolio Return"]
    < backtest["99% VaR Threshold"]
)

breaches_95 = backtest["95% Breach"].sum()
breaches_99 = backtest["99% Breach"].sum()

total_days = len(backtest)

breach_rate_95 = breaches_95 / total_days
breach_rate_99 = breaches_99 / total_days

expected_breaches_95 = total_days * 0.05
expected_breaches_99 = total_days * 0.01

print("\nVaR Backtesting Results:")

print(f"Backtest observations: {total_days}")

print("\n95% VaR:")
print(f"Expected breaches: {expected_breaches_95:.1f}")
print(f"Actual breaches: {breaches_95}")
print(f"Breach rate: {breach_rate_95:.2%}")

print("\n99% VaR:")
print(f"Expected breaches: {expected_breaches_99:.1f}")
print(f"Actual breaches: {breaches_99}")
print(f"Breach rate: {breach_rate_99:.2%}")

breaches_99_df = backtest[
    backtest["99% Breach"]
]

print("\n99% VaR Breach Dates:")
print(
    breaches_99_df[
        [
            "Portfolio Return",
            "99% VaR Threshold"
        ]
    ]
)

# ----------------------------------
# Kupiec VaR Backtest
# ----------------------------------

def kupiec_test(total_observations, breaches, expected_probability):

    observed_probability = (
        breaches / total_observations
    )

    log_likelihood_expected = (
        (total_observations - breaches)
        * np.log(1 - expected_probability)
        +
        breaches
        * np.log(expected_probability)
    )

    log_likelihood_observed = (
        (total_observations - breaches)
        * np.log(1 - observed_probability)
        +
        breaches
        * np.log(observed_probability)
    )

    lr_stat = -2 * (
        log_likelihood_expected
        - log_likelihood_observed
    )

    p_value = 1 - chi2.cdf(
        lr_stat,
        df=1
    )

    return lr_stat, p_value

kupiec_95_stat, kupiec_95_p = kupiec_test(
    total_days,
    breaches_95,
    0.05
)

kupiec_99_stat, kupiec_99_p = kupiec_test(
    total_days,
    breaches_99,
    0.01
)

print("\nKupiec VaR Backtest:")

print("\n95% VaR:")
print(
    f"LR Statistic: "
    f"{kupiec_95_stat:.4f}"
)
print(
    f"P-value: "
    f"{kupiec_95_p:.4f}"
)

print("\n99% VaR:")
print(
    f"LR Statistic: "
    f"{kupiec_99_stat:.4f}"
)
print(
    f"P-value: "
    f"{kupiec_99_p:.4f}"
)

# ----------------------------------
# Plot 99% VaR Backtest
# ----------------------------------

plt.figure(figsize=(14, 7))

plt.plot(
    backtest.index,
    backtest["Portfolio Return"] * 100,
    label="Portfolio Return",
    linewidth=0.8
)

plt.plot(
    backtest.index,
    backtest["99% VaR Threshold"] * 100,
    label="99% VaR Threshold",
    linewidth=1.5
)

breach_points = backtest[
    backtest["99% Breach"]
]

plt.scatter(
    breach_points.index,
    breach_points["Portfolio Return"] * 100,
    label="99% VaR Breach",
    s=35,
    zorder=3
)

plt.axhline(
    y=0,
    linewidth=0.8
)

plt.title("99% Parametric VaR Backtest")
plt.ylabel("Daily Return (%)")
plt.xlabel("Date")
plt.legend()

plt.tight_layout()

plt.savefig(
    "charts/var_99_backtest.png",
    dpi=300
)

plt.show()

# ----------------------------------
# VaR Backtest Summary
# ----------------------------------

backtest_summary = pd.DataFrame({
    "Confidence Level": [
        "95%",
        "99%"
    ],

    "Expected Breach Rate": [
        0.05,
        0.01
    ],

    "Actual Breach Rate": [
        breach_rate_95,
        breach_rate_99
    ],

    "Expected Breaches": [
        expected_breaches_95,
        expected_breaches_99
    ],

    "Actual Breaches": [
        breaches_95,
        breaches_99
    ],

    "Kupiec LR Statistic": [
        kupiec_95_stat,
        kupiec_99_stat
    ],

    "Kupiec P-Value": [
        kupiec_95_p,
        kupiec_99_p
    ]
})

print("\nVaR Backtest Summary:")
print(backtest_summary)