# NameError

**Group members:**
- Cecilie Ring Westergaard (PJT321)
- Tobias Rhod Søndergaard (JCZ104)
- Simon Magaard Skødeberg (HKB674)

## This repository contains:

**1. Data project**

Our project is titled Inequality in Denmark and examines income inequality in Denmark using DST register data, alongside a simulated life-cycle income model.

We first analyze the development of the Gini coefficient and top-10% income share in Denmark and its municipalities (1987–2024), predict future inequality using trend extrapolation, and compare the most and least equal municipalities. We then build and validate a life-cycle simulation of income (covering education, human capital, and unemployment) and decompose which mechanisms drive inequality most.

Extensions: (1) We correlate municipal Gini coefficients with equalization grants, fertility, and crime rates. (2) We add education-scaled unemployment risk to the simulation and examine its effect on inequality.

Distribution of responsibility:
- PJT321: 1.2, 2.4
- JCZ104: 1.3, 2.1, 2.2, 2.3
- HKB674: 1.1, 1.4, 2.5

**2. Model project**

Our project is titled A Consumer with Two Nests: Transport Demand and Taxation and models a consumer choosing between food, bus, and train under a nested CES utility function, together with government tax revenue from these goods.

We calibrate the model under two scenarios (bus/train as complements vs. substitutes), solve it via grid search and L-BFGS-B, and analyze comparative statics and government revenue (Laffer curves) across different tax instruments.

Extension: We add a Pigouvian tax on bus trips to account for a CO2 externality, comparing revenue-maximizing and welfare-maximizing tax rates under both calibrations.

Distribution of responsibility:
- PJT321: Problem 1 & 2
- JCZ104: Problem 3
- HKB674: Problem 4 & 5

**3. Exam project**

The exam project covers three independent problems: real GDP convergence across US states, a Solow growth model with a time-varying savings rate, and an optimal portfolio choice between a risky and a safe asset.

Question 1 downloads real GDP and population data for all 50 US states from the FRED API, computes real GDP per person, and examines convergence and dispersion across states and regions over 1997–2025. Question 2 simulates the Solow model under a savings rate that decays from an initial level toward a long-run target, evaluates welfare under different rules, and finds the welfare-maximizing rule by grid search and numerical optimization. Question 3 simulates a portfolio-rebalancing rule with a no-trade band and trading costs, and evaluates it by expected utility across 50,000 simulated wealth paths.

Extension: In Question 2.6 we propose an alternative savings-rate rule based on power-law decay, and compare the welfare it achieves to the other rules considered.

Distribution of responsibility:
- PJT321: Problem 2
- JCZ104: Problem 3
- HKB674: Problem 1

*All code can be run with a standard Anaconda Distribution for Python 3.14. Furthermore, the following packages are required:*
- The dstapi package:* `%pip install git+https://github.com/alemartinello/dstapi`
- The fredapi package:* `%pip install fredapi`
*The exam project's Question 1 additionally requires a free FRED API key (see 03_examproject/Examproject.ipynb for instructions on obtaining one).*