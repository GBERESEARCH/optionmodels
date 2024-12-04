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

Install in a new environment using Python venv:

Create base environment of Python 3.13
```
$ py -3.13 -m venv .venv
```
Activate new environment
```
$ .venv\scripts\activate
```
Ensure pip is up to date
``` 
$ (.venv) python -m pip install --upgrade pip
```
Install Spyder
```
$ (.venv) python -m pip install spyder
```
Install package
```
$ (.venv) python -m pip install optionmodels
```

&nbsp;

Or to install in new environment using anaconda:
```
$ conda create --name optmods
```
Activate new environment
```
$ activate optmods
```
Install Python
```
(optmods) $ conda install python==3.13
```
Install Spyder
```
(optmods) $ conda install spyder
```
Install package
```
(optmods) $ pip install optionmodels
```

&nbsp;

### Option pricing models:
  - Black-Scholes-Merton (1973)
  - Black (1976)
  - Cox-Ross-Rubinstein Binomial (1979) 
  - Leisen-Reimer Binomial (1996)
  - Trinomial tree
  - Explicit Finite Difference
  - Implicit Finite Difference
  - Crank-Nicolson Finite Difference
  - European Monte Carlo
  - Hull-White (1987) - Uncorrelated Stochastic Vol
  - Hull White (1988) - Correlated Stochastic Vol

&nbsp;

### Setup
Import models

```
from optionmodels.models import Pricer
```

&nbsp;

Initialise a Pricer object
```
opt = Pricer()
```
Calculate option price
```
opt.price(option_method='bsm')
```
```
opt.price(option_method='crr_bin', timing=True, steps=1000)
```
```
opt.price(option_method='emc', simulations=10000)
```

&nbsp;

### Implied Volatility models:
  - Newton-Raphson
  - Bisection
  - Simple iterative reduction

&nbsp;

Initialise a Pricer object
```
imp = Pricer()
```
Extract implied volatility
```
imp.impliedvol(timing=True)
```
```
imp.impliedvol(vol_method='bisection')
```

&nbsp;

### SABR Calibration

&nbsp;

Initialise a SABRVolatility object
```
sabr = SABRVolatility()
```
Calibrate the model and return price and / or volatility
```
sabr.calibrate()
```

&nbsp;

### Tools
  - Cholesky decomposition  
&nbsp;  

The following volume served as a reference for the formulas:
* [The Complete Guide to Option Pricing Formulas, 2nd Ed, E. G. Haug]

[The Complete Guide to Option Pricing Formulas, 2nd Ed, E. G. Haug]:<https://www.amazon.co.uk/Complete-Guide-Option-Pricing-Formulas/dp/0071389970/>