# optionmodels
## Pricing and calibration models

&nbsp;

A collection of option pricing and volatility calibration tools. Each pricer has a timing flag and default parameters for ease of speed comparison.

&nbsp;

### Installation
Install from PyPI:
```
$ pip install optionmodels
```

&nbsp;

### Setup
Import models module

```
import models as mod
```

&nbsp;

### Option pricing models:
  - Black-Scholes-Merton (1973)
  - Black (1976)
  - Cox-Ross-Rubinstein Binomial (1979) 
  - Leisen-Reimer Binomial(1996)
  - Trinomial tree
  - Explicit Finite Difference
  - Implicit Finite Difference
  - Crank-Nicolson Finite Difference
  - European Monte Carlo
  - Hull-White (1987) - Uncorrelated Stochastic Vol
  - Hull White (1988) - Correlated Stochastic Vol

&nbsp;

Initialise a Pricer object
```
opt = mod.Pricer()
```
Calculate option price
```
opt.black_scholes_merton(**kwargs)
```
```
opt.cox_ross_rubinstein_binomial(timing=True, steps=1000, **kwargs)
```
```
opt.european_monte_carlo(simulations=10000, **kwargs)
```

&nbsp;

### Implied Volatility models:
  - Newton-Raphson
  - Bisection
  - Simple iterative reduction

&nbsp;

Initialise an ImpliedVol object
```
imp = mod.ImpliedVol()
```
Extract implied volatility
```
vol.implied_vol_newton_raphson(timing=True, **kwargs)
```
```
vol.implied_vol_bisection(**kwargs)
```

&nbsp;

### SABR Calibration

&nbsp;

Initialise a SABRVolatility object
```
sabr = mod.SABRVolatility()
```
Calibrate the model
```
sabr.calibrate(**kwargs)
```
Price after calibration
```
sabr.price(option='put') 
```

&nbsp;

### Tools
  - Cholesky decomposition  
&nbsp;  

The following volume served as a reference for the formulas:
* [The Complete Guide to Option Pricing Formulas, 2nd Ed, E. G. Haug]

[The Complete Guide to Option Pricing Formulas, 2nd Ed, E. G. Haug]:<https://www.amazon.co.uk/Complete-Guide-Option-Pricing-Formulas/dp/0071389970/>