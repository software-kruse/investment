import streamlit as st

mpt_text = """
# Modern Portfolio Theory (MPT)

Modern Portfolio Theory (MPT) is a foundational framework in finance that explains how investors can build investment portfolios that **maximize expected return for a given level of risk** or **minimize risk for a desired level of return**. It was introduced by **Harry Markowitz in 1952**, earning him a Nobel Prize.

---

# What Is Modern Portfolio Theory?
MPT is based on the idea that an investor should not evaluate investments individually but as part of a **portfolio**, where combining assets can reduce overall risk thanks to **diversification**.

### Key Goals:
1. **Maximize returns** for a chosen risk level.
2. **Minimize risk** for a chosen return level.
3. Achieve an **optimal** mix of assets.

---

# Core Concepts in Modern Portfolio Theory

## 1. Expected Return (ER)
The weighted average of the expected returns of all assets in a portfolio.

Formula:
E(Rₚ) = Σ wᵢ * E(Rᵢ)

Where:
- wᵢ = weight (proportion) of asset i
- E(Rᵢ) = expected return of asset i

---

## 2. Risk (Variance and Standard Deviation)
MPT defines risk as the **variability** of returns (measured by variance or standard deviation).

But here's the key idea:

### The risk of a portfolio is not just the weighted average of individual risks.
It also depends on how assets **move relative to each other**.

---

## 3. Correlation (or Covariance)
This measures how two asset returns move together:

- +1 → perfect positive correlation  
- 0 → no relationship  
- –1 → perfect negative correlation

### Why it matters:
Low or negative correlations **reduce portfolio risk** — this is the engine of diversification.

---

## 4. Diversification
The idea that combining assets that don’t move together reduces total risk.

Example:
If you hold tech stocks *and* utility stocks, they usually respond differently to economic events. This smooths out volatility.

---

# The Efficient Frontier

MPT shows all possible portfolios on a graph:

- x-axis: risk (standard deviation)
- y-axis: expected return

Among all possible combinations, some portfolios will be *better* — offering higher returns for the same risk level.

The **efficient frontier** is the curved line that represents these optimal portfolios.

### Efficient Frontier Features:
- Portfolios *below* the curve are suboptimal.
- Portfolios *on* the curve are efficient.
- The curve typically bows outward due to diversification benefits.

---

# The Risk-Free Asset and the Capital Market Line (CML)

When you introduce a **risk-free asset** (e.g., government T-bills), the picture changes:

- Investors can combine the risk-free asset with the market portfolio.
- This produces a straight line called the **Capital Market Line**.

The point where the CML touches the efficient frontier is the **market portfolio**.

### Key implication:
Every rational investor should combine:
- some proportion of the market portfolio  
- some proportion of the risk-free asset

Depending on risk tolerance:
- Conservative → more risk-free asset  
- Aggressive → borrow at the risk-free rate and leverage the market portfolio

---

# Optimal Portfolio Selection
MPT says:

> Your optimal portfolio = the portfolio on the efficient frontier that aligns with your risk tolerance.

Behaviorally:
- Risk-averse → lower-risk points  
- Risk-seeking → upper points  

---

# Criticisms and Limitations of MPT

Although powerful, MPT has limitations:

### 1. Relies on historical data
Future returns, volatilities, and correlations may differ sharply from the past.

### 2. Assumes normally distributed returns
Real markets show fat tails, crashes, and skew.

### 3. Assumes rational investors
Behavioral finance shows we are not always rational.

### 4. Single-period model
Investment decisions usually span multiple periods.

Despite these issues, MPT remains a cornerstone of portfolio construction.

---

# Why MPT Still Matters Today
It provides:
- A clear framework for assessing risk vs. return.
- The basis for index investing.
- Foundations for CAPM, Black-Litterman, factor models, and more.
- The logic behind modern robo-advisors and target-date funds.

"""

st.markdown(mpt_text)
