# Portfolio Value at Risk & Stress Testing

## Overview

This project evaluates the market risk of a **$1,000,000 multi-asset portfolio** using:

- Historical Value at Risk (VaR)
- Parametric VaR
- Monte Carlo VaR
- Expected Shortfall (CVaR)
- Historical stress testing
- Hypothetical stress testing
- VaR backtesting
- Kupiec model validation

The analysis extends a previously optimized portfolio consisting of **AAPL, GLD, JNJ, JPM, and XOM**.

Historical market data from **January 2020 through December 2025** was obtained using `yfinance`.

The objective is to measure potential portfolio losses under normal market conditions, extreme historical events, and hypothetical stress scenarios.

---

## Portfolio

| Asset | Weight |
|---|---:|
| AAPL | 19.75% |
| GLD | 64.47% |
| JNJ | 0.00% |
| JPM | 13.05% |
| XOM | 2.72% |

**Portfolio Value: $1,000,000**

---

## 1. Daily Portfolio Returns

Daily asset returns were calculated as:

`Daily Return = Current Price / Previous Price - 1`

Portfolio returns were calculated as the weighted sum of individual asset returns:

`Portfolio Return = Sum of (Asset Weight × Asset Return)`

Daily portfolio profit and loss was calculated as:

`Daily P&L = Portfolio Return × Portfolio Value`

---

## 2. Historical Value at Risk

Historical VaR uses the actual historical distribution of portfolio returns.

The **95% VaR** is based on the 5th percentile of historical returns, while the **99% VaR** is based on the 1st percentile.

### 1-Day Historical VaR

| Confidence Level | VaR Return | VaR |
|---|---:|---:|
| 95% | -1.2775% | $12,775 |
| 99% | -2.5032% | $25,032 |

Historical VaR makes no normal-distribution assumption. It measures risk directly from observed portfolio returns.

---

## 3. Expected Shortfall

Expected Shortfall, also known as Conditional Value at Risk (CVaR), measures the **average loss when returns are already worse than the VaR threshold**.

Conceptually:

`Expected Shortfall = Average loss beyond VaR`

| Confidence Level | ES Return | Expected Shortfall |
|---|---:|---:|
| 95% | -2.0488% | $20,488 |
| 99% | -3.4533% | $34,533 |

Expected Shortfall is substantially larger than VaR, showing that losses can become much more severe after entering the extreme tail of the return distribution.

---

## 4. Parametric Value at Risk

Parametric VaR assumes portfolio returns can be approximated by a normal distribution.

The lower-tail return threshold is calculated using:

`VaR Return Threshold = Mean Return + Z-Score × Volatility`

The portfolio's historical daily statistics were:

| Metric | Value |
|---|---:|
| Mean Daily Return | 0.0812% |
| Daily Volatility | 0.9165% |

### 1-Day Parametric VaR

| Confidence Level | VaR Return | VaR |
|---|---:|---:|
| 95% | -1.4263% | $14,263 |
| 99% | -2.0509% | $20,509 |

---

## 5. Monte Carlo Value at Risk

A Monte Carlo simulation generated **100,000 hypothetical daily portfolio returns** using the portfolio's historical mean return and volatility.

A fixed random seed was used to make the simulation reproducible.

| Confidence Level | VaR Return | VaR |
|---|---:|---:|
| 95% | -1.4250% | $14,250 |
| 99% | -2.0585% | $20,585 |

Parametric and Monte Carlo VaR estimates were very similar because both approaches used a normal-return assumption.

![VaR Method Comparison](charts/var_method_comparison.png)

---

## 6. Comparison of VaR Methods

| Method | 95% VaR | 99% VaR |
|---|---:|---:|
| Historical | $12,775 | $25,032 |
| Parametric | $14,263 | $20,509 |
| Monte Carlo | $14,250 | $20,585 |

At the 95% confidence level, all three methods produced relatively similar estimates.

At the 99% confidence level, Historical VaR was noticeably higher than the normal-based Parametric and Monte Carlo estimates.

This suggests that the historical portfolio experienced more severe extreme losses than implied by the normal distribution assumption.

---

## 7. 10-Day Value at Risk

Risk was also measured over a **10-trading-day holding period**.

Historical 10-day returns were calculated by compounding daily portfolio returns.

Conceptually:

`10-Day Return = Product of (1 + Daily Return) - 1`

For the parametric model:

`10-Day Mean = Daily Mean × 10`

`10-Day Volatility = Daily Volatility × sqrt(10)`

### 10-Day VaR

| Method | 95% VaR | 99% VaR |
|---|---:|---:|
| Historical | $34,757 | $55,100 |
| Parametric | $39,550 | $59,302 |
| Monte Carlo | $39,499 | $58,346 |

![1-Day vs 10-Day VaR](charts/var_horizon_comparison.png)

The longer holding period substantially increased potential portfolio losses.

For example, Monte Carlo 95% VaR increased from approximately **$14,250 over one day** to **$39,499 over ten trading days**.

---

## 8. Historical Stress Testing

Historical stress testing identifies the most severe losses that actually occurred in the dataset.

### Worst Single Trading Day

The worst daily portfolio return occurred on **12 March 2020**.

| Metric | Result |
|---|---:|
| Portfolio Return | -5.91% |
| Portfolio Loss | $59,087 |

The loss was substantially larger than the 1-day 99% Historical VaR of approximately **$25,032**.

This demonstrates that VaR represents a loss threshold rather than a maximum possible loss.

### Worst Rolling 10-Day Period

The most severe rolling 10-day period ended on **19 March 2020**.

| Metric | Result |
|---|---:|
| 10-Day Return | -14.72% |
| Portfolio Loss | $147,234 |

The worst realized 10-day loss was approximately **2.7 times** the 10-day 99% Historical VaR of about $55,100.

Several of the worst 10-day periods occurred around March 2020, showing that large portfolio losses can cluster during periods of severe market stress.

---

## 9. Hypothetical Stress Testing

Three illustrative hypothetical stress scenarios were constructed.

These scenarios are used for risk analysis and are **not forecasts**.

### Stress Scenarios

| Scenario | AAPL | GLD | JNJ | JPM | XOM |
|---|---:|---:|---:|---:|---:|
| Equity Sell-Off | -15% | +5% | -5% | -12% | -10% |
| Gold Correction | -5% | -12% | -3% | -5% | -6% |
| Broad Market Shock | -20% | -8% | -8% | -18% | -15% |

### Portfolio Impact

| Scenario | Portfolio Return | Portfolio P&L |
|---|---:|---:|
| Equity Sell-Off | -1.58% | -$15,770 |
| Gold Correction | -9.54% | -$95,396 |
| Broad Market Shock | -11.86% | -$118,646 |

![Hypothetical Stress Testing](charts/hypothetical_stress_test.png)

The **Equity Sell-Off** caused a relatively small portfolio loss because the assumed 5% increase in GLD offset part of the equity decline.

The **Gold Correction** produced a much larger loss because GLD represents the largest portfolio allocation.

The **Broad Market Shock** generated the largest hypothetical loss because several portfolio assets declined simultaneously, weakening the benefits of diversification.

---

## 10. Stress Contribution Analysis

Each asset's contribution to the stressed portfolio return was calculated as:

`Stress Contribution = Portfolio Weight × Asset Shock`

### Contribution to Portfolio Return

| Scenario | AAPL | GLD | JNJ | JPM | XOM |
|---|---:|---:|---:|---:|---:|
| Equity Sell-Off | -2.9625% | +3.2235% | 0.0000% | -1.5660% | -0.2720% |
| Gold Correction | -0.9875% | -7.7364% | 0.0000% | -0.6525% | -0.1632% |
| Broad Market Shock | -3.9500% | -5.1576% | 0.0000% | -2.3490% | -0.4080% |

In the Gold Correction scenario, GLD alone contributed approximately **-$77,364** of the total **-$95,396** portfolio loss.

This highlights concentration risk.

Although the portfolio contains several assets, its large allocation to GLD means that a severe decline in gold can still have a major effect on total portfolio value.

---

## 11. VaR Backtesting

A rolling **252-trading-day Parametric VaR model** was backtested.

For each day, the model estimated VaR using only the previous 252 trading days.

The rolling statistics were shifted by one day to prevent look-ahead bias.

A VaR breach occurs when:

`Actual Portfolio Return < VaR Threshold`

The backtest contained **1,255 observations**.

### Backtesting Results

| Confidence Level | Expected Breach Rate | Actual Breach Rate | Expected Breaches | Actual Breaches |
|---|---:|---:|---:|---:|
| 95% | 5.00% | 4.46% | 62.8 | 56 |
| 99% | 1.00% | 2.07% | 12.6 | 26 |

The 95% VaR model produced approximately the expected number of exceptions.

However, the 99% VaR model recorded **26 breaches compared with only 12.6 expected breaches**.

![99% VaR Backtest](charts/var_99_backtest.png)

The chart also shows periods where breaches occurred close together, indicating that extreme losses can cluster during periods of elevated market volatility.

---

## 12. Kupiec Proportion of Failures Test

The **Kupiec Proportion of Failures Test** evaluates whether the number of observed VaR breaches is statistically consistent with the number expected by the model.

The null hypothesis is:

`H0: Observed breach probability = Expected breach probability`

A significance level of **5%** was used.

### Results

| Confidence Level | LR Statistic | P-Value |
|---|---:|---:|
| 95% | 0.7918 | 0.3736 |
| 99% | 11.1217 | 0.0009 |

### 95% VaR

The p-value was:

`0.3736 > 0.05`

Therefore, the null hypothesis was **not rejected**.

The observed 95% VaR breach frequency was reasonably consistent with the model's expected 5% breach rate.

### 99% VaR

The p-value was:

`0.0009 < 0.05`

Therefore, the null hypothesis was **rejected**.

The observed 99% VaR breach frequency was statistically inconsistent with the expected 1% breach rate.

This indicates that the rolling normal-parametric VaR model underestimated the frequency of extreme portfolio losses.

---

## Key Findings

- Historical, Parametric, and Monte Carlo VaR produced similar results at the 95% confidence level.
- Historical 99% VaR was substantially higher than the normal-based VaR estimates.
- 95% Expected Shortfall was approximately **$20,488**.
- 99% Expected Shortfall was approximately **$34,533**.
- The worst historical single-day loss was approximately **$59,087**.
- The worst historical rolling 10-day loss was approximately **$147,234**.
- The worst 10-day historical loss was about **2.7 times** the 10-day 99% Historical VaR.
- Stress testing revealed meaningful concentration risk from the large GLD allocation.
- GLD provided significant downside protection in the Equity Sell-Off scenario.
- The diversification benefit weakened when multiple asset classes declined simultaneously.
- The Broad Market Shock produced the largest hypothetical loss at approximately **$118,646**.
- The rolling 95% Parametric VaR model produced a breach rate close to expectations.
- The rolling 99% VaR model recorded a **2.07% breach rate compared with 1% expected**.
- The Kupiec test rejected the 99% VaR model's expected exception frequency.
- Normal-distribution VaR performed reasonably for moderate tail risk but understated extreme tail risk in this dataset.

---

## Tools Used

- Python
- pandas
- NumPy
- SciPy
- Matplotlib
- yfinance

---

## Project Structure

```text
portfolio-var-stress-testing/
│
├── var_analysis.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── charts/
    ├── var_method_comparison.png
    ├── var_horizon_comparison.png
    ├── hypothetical_stress_test.png
    └── var_99_backtest.png
```

---

## Limitations

- Historical estimates depend on the selected 2020-2025 sample period.
- Historical relationships between assets may not continue in the future.
- Parametric VaR assumes normally distributed portfolio returns.
- The Monte Carlo model assumes constant historical mean and volatility.
- The simulation does not model changing volatility regimes or fat-tailed distributions.
- Hypothetical stress scenarios are illustrative rather than forecasts.
- Portfolio weights are assumed to remain constant.
- Transaction costs, taxes, liquidity risk, and portfolio rebalancing are not modeled.
- The Kupiec test evaluates the number of breaches but does not test whether breaches occur independently over time.

---

## Conclusion

This project demonstrates that no single measure provides a complete view of portfolio market risk.

Value at Risk provides a useful estimate of potential loss thresholds, but it does not describe how severe losses may become after the threshold is exceeded.

Expected Shortfall addresses this limitation by measuring average losses within the extreme tail.

Historical and hypothetical stress testing provide additional insight into how the portfolio behaves during severe market conditions, while backtesting evaluates whether the VaR model performs as expected.

The rolling 95% Parametric VaR model produced an exception frequency broadly consistent with expectations.

However, the 99% model recorded substantially more breaches than expected, and the Kupiec test rejected the model's expected 1% exception rate.

Overall, combining **VaR, Expected Shortfall, Monte Carlo simulation, stress testing, and statistical backtesting** provides a more comprehensive view of portfolio risk than relying on VaR alone.