# NameError

**Group members:**
- Cecilie Ring Westergaard (PJT321)
- Tobias Rhod Søndergaard (JCZ104)
- Simon Magaard Skødeberg (HKB674)

**This repository contains:**

**1. Data project**
Our project is titled Inequality in Denmark and examines income inequality in Denmark using DST register data, alongside a simulated life-cycle income model.

We first analyze the development of the Gini coefficient and top-10% income share in Denmark and its municipalities (1987–2024), predict future inequality using trend extrapolation, and compare the most and least equal municipalities. We then build and validate a life-cycle simulation of income (covering education, human capital, and unemployment) and decompose which mechanisms drive inequality most.

Extensions: (1) We correlate municipal Gini coefficients with equalization grants, fertility, and crime rates. (2) We add education-scaled unemployment risk to the simulation and examine its effect on inequality.

Distribution of responsibility:
HKB674: 1.1, 1.4, 2.5
PJT321: 1.2, 2.4
JCZ104: 1.3, 2.1, 2.2, 2.3

**2. Model project**
Our project is titled A Consumer with Two Nests: Transport Demand and Taxation and models a consumer choosing between food, bus, and train under a nested CES utility function, together with government tax revenue from these goods.

We calibrate the model under two scenarios (bus/train as complements vs. substitutes), solve it via grid search and L-BFGS-B, and analyze comparative statics and government revenue (Laffer curves) across different tax instruments.

Extension: We add a Pigouvian tax on bus trips to account for a CO2 externality, comparing revenue-maximizing and welfare-maximizing tax rates under both calibrations.

Distribution of responsibility:
HKB674: problem 4 and 5
PJT321: problem 1 and 2
JCZ104: problem 3

**3. Exam project**
description

Distribution of responsibility:
HKB674:
PJT321:
JCZ104:

*All code can be run with a standard Anaconda Distribution for Python 3.14 and requires the dstapi package: pip install git+https://github.com/alemartinello/dstapi.*