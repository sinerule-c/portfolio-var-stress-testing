# Portfolio Value at Risk & Stress Testing

## Overview

This project evaluates the market risk of a **$1,000,000 multi-asset portfolio** using Value at Risk (VaR), Expected Shortfall, Monte Carlo simulation, stress testing, and VaR backtesting.

The analysis extends a previously optimized portfolio consisting of:

- AAPL
- GLD
- JNJ
- JPM
- XOM

Historical market data from **January 2020 through December 2025** was obtained using `yfinance`.

The project focuses on measuring potential portfolio losses under normal market conditions, extreme historical events, and hypothetical stress scenarios.

---

## Portfolio

Approximate portfolio weights:

| Asset | Weight |
|---|---:|
| AAPL | 19.75% |
| GLD | 64.47% |
| JNJ | 0.00% |
| JPM | 13.05% |
| XOM | 2.72% |

Portfolio value:

**$1,000,000**

---

## Methodology

### 1. Daily Portfolio Returns

Daily asset returns were calculated using:

$$
R_t = \frac{P_t}{P_{t-1}} - 1
$$

Portfolio returns were calculated as the weighted sum of individual asset returns:

$$
R_p = \sum_{i=1}^{n} w_iR_i
$$

Daily portfolio profit and loss was then calculated as:

$$
P\&L_t = R_{p,t} \times \text{Portfolio Value}
$$

---

## 2. Historical Value at Risk

Historical VaR uses the empirical distribution of observed portfolio returns.

The **95% VaR** corresponds to the 5th percentile of historical returns, while the **99% VaR** corresponds to the 1st percentile.

### 1-Day Historical VaR

| Confidence Level | VaR Return | VaR |
|---|---:|---:|
| 95% | -1.2775% | $12,775 |
| 99% | -2.5032% | $25,032 |

Historical VaR does not assume that returns follow a normal distribution. Instead, it uses the actual observed distribution of portfolio returns.

---

## 3. Expected Shortfall

Expected Shortfall, also known as Conditional Value at Risk (CVaR), measures the average loss conditional on losses exceeding the VaR threshold.

$$
ES_{\alpha}
=
-E[R_p \mid R_p \le q_{\alpha}]
$$

where \(q_{\alpha}\) represents the relevant lower-tail return threshold.

| Confidence Level | ES Return | Expected Shortfall |
|---|---:|---:|
| 95% | -2.0488% | $20,488 |
| 99% | -3.4533% | $34,533 |

Expected Shortfall is substantially larger than VaR, demonstrating that losses can increase significantly once the portfolio enters the extreme tail of the return distribution.

---

## 4. Parametric Value at Risk

Parametric VaR assumes portfolio returns can be approximated using a normal distribution.

The lower-tail return threshold is calculated as:

$$
q_{\alpha}
=
\mu + z_{\alpha}\sigma
$$

where:

- \(\mu\) = mean daily portfolio return
- \(\sigma\) = daily portfolio volatility
- \(z_{\alpha}\) = standard normal critical value

Dollar VaR is then calculated as:

$$
VaR_{\$}
=
-q_{\alpha} \times \text{Portfolio Value}
$$

The portfolio's historical daily statistics were:

- **Mean daily return:** 0.0812%
- **Daily volatility:** 0.9165%

### Parametric VaR

| Confidence Level | VaR Return | VaR |
|---|---:|---:|
| 95% | -1.4263% | $14,263 |
| 99% | -2.0509% | $20,509 |

---

## 5. Monte Carlo Value at Risk

A Monte Carlo simulation was used to generate **100,000 hypothetical daily portfolio returns** using the historical portfolio mean and volatility.

A fixed random seed was used to ensure reproducibility.

| Confidence Level | VaR Return | VaR |
|---|---:|---:|
| 95% | -1.4250% | $14,250 |
| 99% | -2.0585% | $20,585 |

Parametric and Monte Carlo VaR estimates were very similar because both methods used a normal-return assumption.

![VaR Method Comparison](charts/var_method_comparison.png)

---

## 6. Comparison of VaR Methods

| Method | 95% VaR | 99% VaR |
|---|---:|---:|
| Historical | $12,775 | $25,032 |
| Parametric | $14,263 | $20,509 |
| Monte Carlo | $14,250 | $20,585 |

Historical VaR was lower than the normal-based methods at the 95% confidence level but substantially higher at the 99% confidence level.

This suggests that extreme historical portfolio losses were more severe than implied by the normal distribution assumption.

The result highlights an important limitation of normal-based VaR models: they may fail to fully capture extreme tail events.

---

## 7. 10-Day Value at Risk

Risk was also evaluated over a **10-trading-day holding period**.

Historical 10-day returns were calculated by compounding rolling daily returns:

$$
R_{10}
=
\prod_{t=1}^{10}(1+R_t)-1
$$

For the parametric model:

$$
\mu_{10}=10\mu
$$

and:

$$
\sigma_{10}=\sqrt{10}\sigma
$$

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

Historical stress testing was used to identify the portfolio's most severe realized losses.

### Worst Single Trading Day

The worst daily portfolio return occurred on **12 March 2020**:

- **Portfolio return:** -5.91%
- **Portfolio loss:** $59,087

This loss was substantially larger than the 1-day 99% Historical VaR of approximately **$25,032**.

This demonstrates that VaR should not be interpreted as the maximum possible portfolio loss.

### Worst Rolling 10-Day Period

The most severe rolling 10-day period ended on **19 March 2020**:

- **10-day return:** -14.72%
- **Portfolio loss:** $147,234

The worst realized 10-day loss was approximately **2.7 times** the 10-day 99% Historical VaR of approximately $55,100.

Several of the worst rolling 10-day periods occurred around March 2020, showing how extreme portfolio losses can cluster during periods of severe market stress.

---

## 9. Hypothetical Stress Testing

Three illustrative hypothetical stress scenarios were constructed.

These scenarios are designed for risk analysis and are **not forecasts**.

### Stress Scenarios

| Scenario | AAPL | GLD | JNJ | JPM | XOM |
|---|---:|---:|---:|---:|---:|
| Equity Sell-Off | -15% | +5% | -5% | -12% | -10% |
| Gold Correction | -5% | -12% | -3% | -5% | -6% |
| Broad Market Shock | -20% | -8% | -8% | -18% | -15% |

### Portfolio Results

| Scenario | Portfolio Return | Portfolio P&L |
|---|---:|---:|
| Equity Sell-Off | -1.58% | -$15,770 |
| Gold Correction | -9.54% | -$95,396 |
| Broad Market Shock | -11.86% | -$118,646 |

![Hypothetical Stress Testing](charts/hypothetical_stress_test.png)

The **Equity Sell-Off** produced a relatively limited portfolio loss because the assumed increase in GLD partially offset losses in equities.

The **Gold Correction** produced a much larger loss because GLD represented the largest portfolio allocation.

The **Broad Market Shock** generated the largest hypothetical loss because multiple portfolio assets declined simultaneously, reducing the benefits of diversification.

---

## 10. Stress Contribution Analysis

Asset-level contributions were calculated as:

$$
Contribution_i
=
w_i \times Shock_i
$$

### Contribution by Asset

| Scenario | AAPL | GLD | JNJ | JPM | XOM |
|---|---:|---:|---:|---:|---:|
| Equity Sell-Off | -2.9625% | +3.2235% | 0.0000% | -1.5660% | -0.2720% |
| Gold Correction | -0.9875% | -7.7364% | 0.0000% | -0.6525% | -0.1632% |
| Broad Market Shock | -3.9500% | -5.1576% | 0.0000% | -2.3490% | -0.4080% |

In the Gold Correction scenario, GLD alone contributed approximately:

**-$77,364**

of the total:

**-$95,396**

portfolio loss.

This highlights an important distinction between diversification and concentration risk.

Although the portfolio contains multiple assets, its large GLD allocation means that a severe decline in gold can still have a substantial effect on total portfolio value.

---

## 11. VaR Backtesting

A rolling **252-trading-day parametric VaR model** was backtested.

For each trading day, the VaR estimate was calculated using only information available during the previous 252 trading days.

The rolling mean and volatility estimates were shifted by one day to avoid look-ahead bias.

A VaR breach occurred when:

$$
R_t < VaR_t
$$

meaning that the realized portfolio return was worse than the VaR threshold predicted by the model.

### Backtesting Results

The backtest contained **1,255 observations**.

| Confidence | Expected Breach Rate | Actual Breach Rate | Expected Breaches | Actual Breaches |
|---|---:|---:|---:|---:|
| 95% | 5.00% | 4.46% | 62.8 | 56 |
| 99% | 1.00% | 2.07% | 12.6 | 26 |

The 95% model produced approximately the expected number of exceptions.

However, the 99% model experienced **more than twice the expected number of breaches**.

![99% VaR Backtest](charts/var_99_backtest.png)

The backtest also showed periods where VaR breaches occurred close together, indicating that extreme losses can cluster during periods of elevated market volatility.

---

## 12. Kupiec Proportion of Failures Test

The **Kupiec Proportion of Failures test** was used to determine whether the observed VaR exception frequency was statistically consistent with the model's expected exception probability.

The null hypothesis is:

$$
H_0:
p_{\text{observed}}
=
p_{\text{expected}}
$$

A significance level of:

$$
\alpha = 0.05
$$

was used.

### Results

| Confidence | LR Statistic | P-Value |
|---|---:|---:|
| 95% | 0.7918 | 0.3736 |
| 99% | 11.1217 | 0.0009 |

### 95% VaR

The p-value was:

$$
0.3736 > 0.05
$$

Therefore, the null hypothesis was **not rejected**.

The observed 95% VaR breach frequency was reasonably consistent with the model's expected 5% breach rate.

### 99% VaR

The p-value was:

$$
0.0009 < 0.05
$$

Therefore, the null hypothesis was **rejected**.

The observed frequency of 99% VaR breaches was statistically inconsistent with the model's expected 1% breach rate.

This indicates that the rolling normal-parametric VaR model underestimated the frequency of extreme portfolio losses.

---

## Key Findings

- Historical, Parametric, and Monte Carlo VaR produced relatively similar estimates at the 95% confidence level.
- Historical 99% VaR was substantially higher than normal-based VaR estimates, indicating more severe empirical tail losses.
- Expected Shortfall showed that average losses beyond the VaR threshold were significantly larger than VaR itself.
- 95% Expected Shortfall reached approximately **$20,488**, while 99% Expected Shortfall reached approximately **$34,533**.
- The worst historical single-day portfolio loss was approximately **$59,087**.
- The worst historical rolling 10-day portfolio loss reached approximately **$147,234**.
- The worst historical 10-day loss was approximately 2.7 times the corresponding 99% Historical VaR.
- Stress testing revealed substantial exposure to GLD because of its large portfolio weight.
- Diversification provided meaningful protection during the Equity Sell-Off scenario when GLD moved positively.
- Diversification benefits weakened substantially when several portfolio assets declined simultaneously.
- The Broad Market Shock produced the largest hypothetical loss of approximately **$118,646**.
- The rolling 95% parametric VaR model produced an exception rate close to expectations.
- The rolling 99% VaR model recorded a **2.07% breach rate compared with the expected 1%**.
- The Kupiec test rejected the 99% VaR model's expected breach frequency.
- The results suggest that a normal-return VaR model can provide reasonable estimates under moderate conditions while understating extreme tail risk.

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
- Historical relationships between assets may not persist in future market conditions.
- Parametric VaR assumes normally distributed portfolio returns.
- The Monte Carlo model assumes constant historical mean and volatility.
- The Monte Carlo simulation does not model changing volatility regimes or fat-tailed return distributions.
- Hypothetical stress scenarios are illustrative rather than forecasts.
- Portfolio weights are held constant throughout the analysis.
- Transaction costs, taxes, liquidity risk, and portfolio rebalancing are not modeled.
- The Kupiec test evaluates whether the overall number of VaR exceptions is consistent with expectations but does not test whether breaches occur independently over time.

---

## Conclusion

This project demonstrates that no single risk measure provides a complete view of portfolio market risk.

Value at Risk provides a useful estimate of potential loss thresholds, but it does not measure the severity of losses once those thresholds are exceeded.

Expected Shortfall addresses this limitation by examining average losses in the extreme tail, while historical and hypothetical stress testing evaluate how the portfolio may behave during severe market conditions.

Backtesting provides an additional layer of model validation by comparing predicted VaR thresholds against realized portfolio returns.

The rolling 95% parametric VaR model produced an exception frequency broadly consistent with expectations. However, the 99% model recorded substantially more breaches than expected, and the Kupiec test rejected the model's expected 1% exception rate.

Overall, the results show that combining **VaR, Expected Shortfall, stress testing, Monte Carlo simulation, and statistical backtesting** provides a more comprehensive view of portfolio risk than relying on VaR alone.