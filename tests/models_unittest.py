"""
Unit tests for option pricing and implied volatility models

"""

import unittest
from models import Pricer
from sabr import SABRVolatility

class ModelsTestCase(unittest.TestCase):
    """
    Unit tests for option pricing and implied volatility models

    """
    # For each function, test with defaults and with specified parameters

    def test_black_scholes_merton(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().price(option_method='bsm'), float)
        self.assertIsInstance(Pricer().price(option_method='bsm',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, option='put',
            timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='bsm'), 0)
        self.assertGreater(Pricer().price(option_method='bsm',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, option='put',
            timing=True), 0)

        # Print the output from running the function
        print("Default black_scholes_merton: ",
              Pricer().price(option_method='bsm'))
        print("Revalued black_scholes_merton: ",
              Pricer().price(option_method='bsm',
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, option='put',
                  timing=True))


    def test_black_scholes_merton_vega(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().price(option_method='bsm_vega'), float)
        self.assertIsInstance(Pricer().price(option_method='bsm_vega',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, option='put',
            timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='bsm_vega'), 0)
        self.assertGreater(Pricer().price(option_method='bsm_vega',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, option='put',
            timing=True), 0)

        # Print the output from running the function
        print("Default black_scholes_merton_vega: ",
              Pricer().price(option_method='bsm_vega'))
        print("Revalued black_scholes_merton_vega: ",
              Pricer().price(option_method='bsm_vega',
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, option='put',
                  timing=True))


    def test_black_76(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().price(option_method='black76'), float)
        self.assertIsInstance(Pricer().price(option_method='black76',
            F=50, K=55, T=1, r=0.05, sigma=0.3, option='put',
            timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='black76'), 0)
        self.assertGreater(Pricer().price(option_method='black76',
            F=50, K=55, T=1, r=0.05, sigma=0.3, option='put',
            timing=True), 0)

        # Print the output from running the function
        print("Default black_76: ", Pricer().price(option_method='black76'))
        print("Revalued black_76: ", Pricer().price(option_method='black76',
            F=50, K=55, T=1, r=0.05, sigma=0.3, option='put',
            timing=True))


    def test_european_binomial(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().price(option_method='euro_bin'), float)
        self.assertIsInstance(Pricer().price(option_method='euro_bin',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500,
            option='put', timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='euro_bin'), 0)
        self.assertGreater(Pricer().price(option_method='euro_bin',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500,
            option='put', timing=True), 0)

        # Print the output from running the function
        print("Default european_binomial: ",
              Pricer().price(option_method='euro_bin'))
        print("Revalued european_binomial: ",
              Pricer().price(option_method='euro_bin',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500,
            option='put', timing=True))


    def test_cox_ross_rubinstein_binomial(self):

        # Test if the output is a float
        self.assertIsInstance(
            Pricer().price(option_method='crr_bin'), float)
        self.assertIsInstance(Pricer().price(option_method='crr_bin',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500,
            output_flag='all', option='put', american=True,
            timing=True)['Price'], float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='crr_bin'), 0)
        self.assertGreater(Pricer().price(option_method='crr_bin',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500,
            output_flag='all', option='put', american=True,
            timing=True)['Price'], 0)

        # Print the output from running the function
        print("Default cox_ross_rubinstein_binomial: ",
              Pricer().price(option_method='crr_bin'))
        print("Revalued cox_ross_rubinstein_binomial: ",
              Pricer().price(option_method='crr_bin',
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500,
                  output_flag='all', option='put', american=True,
                  timing=True)['Price'])


    def test_leisen_reimer_binomial(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().price(option_method='lr_bin'), float)
        self.assertIsInstance(Pricer().price(option_method='lr_bin',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500,
            output_flag='all', option='put', american=True,
            timing=True)['Price'], float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='lr_bin'), 0)
        self.assertGreater(Pricer().price(option_method='lr_bin',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500,
            output_flag='all', option='put', american=True,
            timing=True)['Price'], 0)

        # Print the output from running the function
        print("Default leisen_reimer_binomial: ",
              Pricer().price(option_method='lr_bin'))
        print("Revalued leisen_reimer_binomial: ",
              Pricer().price(option_method='lr_bin',
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500,
                  output_flag='all', option='put', american=True,
                  timing=True)['Price'])


    def test_trinomial_tree(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().price(option_method='tt'), float)
        self.assertIsInstance(Pricer().price(option_method='tt',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500,
            output_flag='all', option='put', american=True,
            timing=True)['Price'], float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='tt'), 0)
        self.assertGreater(Pricer().price(option_method='tt',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500,
            output_flag='all', option='put', american=True,
            timing=True)['Price'], 0)

        # Print the output from running the function
        print("Default trinomial_tree: ", Pricer().price(option_method='tt'))
        print("Revalued trinomial_tree: ", Pricer().price(option_method='tt',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500,
            output_flag='all', option='put', american=True,
            timing=True)['Price'])


    def test_implied_trinomial_tree(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().price(option_method='itt'), float)
        self.assertIsInstance(Pricer().price(option_method='itt',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps_itt=5, step=4,
            state=4, skew=0.0005, output_flag='price', option='put',
            timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='itt'), 0)
        self.assertGreater(Pricer().price(option_method='itt',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps_itt=5, step=4,
            state=4, skew=0.0005, output_flag='price', option='put',
            timing=True), 0)

        # Print the output from running the function
        print("Default implied_trinomial_tree: ",
              Pricer().price(option_method='itt'))
        print("Revalued implied_trinomial_tree: ",
              Pricer().price(option_method='itt',
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps_itt=5,
                  step=4, state=4, skew=0.0005, output_flag='price',
                  option='put', timing=True))


    def test_explicit_finite_difference(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().price(option_method='efd'), float)
        self.assertIsInstance(Pricer().price(option_method='efd',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, nodes=50,
            option='put', american=True, timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='efd'), 0)
        self.assertGreater(Pricer().price(option_method='efd',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, nodes=50,
            option='put', american=True, timing=True), 0)

        # Print the output from running the function
        print("Default explicit_finite_difference: ",
              Pricer().price(option_method='efd'))
        print("Revalued explicit_finite_difference: ",
              Pricer().price(option_method='efd',
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, nodes=50,
                  option='put', american=True, timing=True))


    def test_implicit_finite_difference(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().price(option_method='ifd'), float)
        self.assertIsInstance(Pricer().price(option_method='ifd',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, nodes=50,
            option='put', american=True, timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='ifd'), 0)
        self.assertGreater(Pricer().price(option_method='ifd',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, nodes=50,
            option='put', american=True, timing=True), 0)

        # Print the output from running the function
        print("Default implicit_finite_difference: ",
              Pricer().price(option_method='ifd'))
        print("Revalued implicit_finite_difference: ",
              Pricer().price(option_method='ifd',
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500,
                  nodes=50, option='put', american=True, timing=True))


    def test_explicit_finite_difference_lns(self):

        # Test if the output is a float
        self.assertIsInstance(
            Pricer().price(option_method='efd_lns'), float)
        self.assertIsInstance(Pricer().price(option_method='efd_lns',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps_itt=20, nodes=50,
            option='put', american=True, timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='efd_lns'), 0)
        self.assertGreater(Pricer().price(option_method='efd_lns',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps_itt=20, nodes=50,
            option='put', american=True, timing=True), 0)

        # Print the output from running the function
        print("Default explicit_finite_difference_lns: ",
              Pricer().price(option_method='efd_lns'))
        print("Revalued explicit_finite_difference_lns: ",
              Pricer().price(option_method='efd_lns',
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps_itt=20,
                  nodes=50, option='put', american=True, timing=True))


    def test_crank_nicolson(self):

        # Test if the output is a float
        self.assertIsInstance(
            Pricer().price(option_method='cn'), float)
        self.assertIsInstance(Pricer().price(option_method='cn',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, nodes=50,
            option='put', american=True, timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='cn'), 0)
        self.assertGreater(Pricer().price(option_method='cn',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, nodes=50,
            option='put', american=True, timing=True), 0)

        # Print the output from running the function
        print("Default crank_nicolson: ", Pricer().price(option_method='cn'))
        print("Revalued crank_nicolson: ", Pricer().price(option_method='cn',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, nodes=50,
            option='put', american=True, timing=True))


    def test_european_monte_carlo(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().price(option_method='emc'), float)
        self.assertIsInstance(Pricer().price(option_method='emc',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, simulations=1000,
            option='put', timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='emc'), 0)
        self.assertGreater(Pricer().price(option_method='emc',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, simulations=1000,
            option='put', timing=True), 0)

        # Print the output from running the function
        print("Default european_monte_carlo: ",
              Pricer().price(option_method='emc'))
        print("Revalued european_monte_carlo: ",
              Pricer().price(option_method='emc',
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, simulations=1000,
                  option='put', timing=True))


    def test_european_monte_carlo_with_greeks(self):

        # Test if the output is a float
        self.assertIsInstance(
            Pricer().price(option_method='emc_greeks'), float)
        self.assertIsInstance(Pricer().price(option_method='emc_greeks',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, simulations=1000,
            option='put', output_flag='all', timing=True)['Price'], float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='emc_greeks'), 0)
        self.assertGreater(Pricer().price(option_method='emc_greeks',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, simulations=1000,
            option='put', output_flag='all', timing=True)['Price'], 0)

        # Print the output from running the function
        print("Default european_monte_carlo_with_greeks: ",
              Pricer().price(option_method='emc_greeks'))
        print("Revalued european_monte_carlo_with_greeks: ",
              Pricer().price(option_method='emc_greeks',
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, simulations=1000,
                  option='put', output_flag='all', timing=True)['Price'])


    def test_hull_white_87(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().price(option_method='hw87'), float)
        self.assertIsInstance(Pricer().price(option_method='hw87',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, vvol=0.3,
            option='put', timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='hw87'), 0)
        self.assertGreater(Pricer().price(option_method='hw87',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, vvol=0.3,
            option='put', timing=True), 0)

        # Print the output from running the function
        print("Default hull_white_87: ", Pricer().price(option_method='hw87'))
        print("Revalued hull_white_87: ", Pricer().price(option_method='hw87',
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, vvol=0.3,
            option='put', timing=True))


    def test_hull_white_88(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().price(option_method='hw88'), float)
        self.assertIsInstance(Pricer().price(option_method='hw88',
            S=50, K=55, T=1, r=0.05, q=0.01, sig0=0.07, sigLR=0.05,
            halflife=0.15, vvol=0.3, rho=0.1, option='put', timing=True),
            float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().price(option_method='hw88'), 0)
        self.assertGreater(Pricer().price(option_method='hw88',
            S=50, K=55, T=1, r=0.05, q=0.01, sig0=0.07, sigLR=0.05,
            halflife=0.15, vvol=0.3, rho=0.1, option='put', timing=True), 0)

        # Print the output from running the function
        print("Default hull_white_88: ", Pricer().price(option_method='hw88'))
        print("Revalued hull_white_88: ", Pricer().price(option_method='hw88',
            S=50, K=55, T=1, r=0.05, q=0.01, sig0=0.07, sigLR=0.05,
            halflife=0.15, vvol=0.3, rho=0.1, option='put', timing=True))


    def test_implied_vol_newton_raphson(self):

        # Test if the output is a float
        self.assertIsInstance(
            Pricer().impliedvol(vol_method='nr'), float)
        self.assertIsInstance(Pricer().impliedvol(vol_method='nr',
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001,
            option='put', timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().impliedvol(vol_method='nr'), 0)
        self.assertGreater(Pricer().impliedvol(vol_method='nr',
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001,
            option='put', timing=True), 0)

        # Print the output from running the function
        print("Default implied_vol_newton_raphson: ",
              Pricer().impliedvol(vol_method='nr'))
        print("Revalued implied_vol_newton_raphson: ",
              Pricer().impliedvol(vol_method='nr',
                  S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001,
                  option='put', timing=True))


    def test_implied_vol_bisection(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().impliedvol(vol_method='bisection'), float)
        self.assertIsInstance(Pricer().impliedvol(vol_method='bisection',
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001,
            option='put', timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().impliedvol(vol_method='bisection'), 0)
        self.assertGreater(Pricer().impliedvol(vol_method='bisection',
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001,
            option='put', timing=True), 0)

        # Print the output from running the function
        print("Default implied_vol_bisection: ",
              Pricer().impliedvol(vol_method='bisection'))
        print("Revalued implied_vol_bisection: ",
              Pricer().impliedvol(vol_method='bisection',
                  S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001,
                  option='put', timing=True))


    def test_implied_vol_naive(self):

        # Test if the output is a float
        self.assertIsInstance(Pricer().impliedvol(vol_method='naive'), float)
        self.assertIsInstance(Pricer().impliedvol(vol_method='naive',
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001,
            option='put', timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().impliedvol(vol_method='naive'), 0)
        self.assertGreater(Pricer().impliedvol(vol_method='naive',
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001,
            option='put', timing=True), 0)

        # Print the output from running the function
        print("Default implied_vol_naive: ",
              Pricer().impliedvol(vol_method='naive'))
        print("Revalued implied_vol_naive: ",
              Pricer().impliedvol(vol_method='naive',
                  S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001,
                  option='put', timing=True))


    def test_implied_vol_naive_verbose(self):

        # Test if the output is a float
        self.assertIsInstance(
            Pricer().impliedvol(vol_method='naive_verbose'), float)
        self.assertIsInstance(Pricer().impliedvol(vol_method='naive_verbose',
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001,
            option='put', timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(Pricer().impliedvol(vol_method='naive_verbose'), 0)
        self.assertGreater(Pricer().impliedvol(vol_method='naive_verbose',
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001,
            option='put', timing=True), 0)

        # Print the output from running the function
        print("Default implied_vol_naive_verbose: ",
              Pricer().impliedvol(vol_method='naive_verbose'))
        print("Revalued implied_vol_naive_verbose: ",
              Pricer().impliedvol(vol_method='naive_verbose',
                  S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001,
                  option='put', timing=True))


    def test_sabr_volatility_calibrate(self):

        # Test if the output is a float
        self.assertIsInstance(SABRVolatility().calibrate(), float)
        self.assertIsInstance(SABRVolatility().calibrate(
            F=90, K=75, T=1, r=0.03, atmvol=0.25, beta=0.9, volvol=0.3,
            rho=-0.2, option='call', timing=True,
            output_flag='all')['Price'], float)

        # Test if the value of the output is greater than zero
        self.assertGreater(SABRVolatility().calibrate(), 0)
        self.assertGreater(SABRVolatility().calibrate(
            F=90, K=75, T=1, r=0.03, atmvol=0.25, beta=0.9, volvol=0.3,
            rho=-0.2, option='call', timing=True,
            output_flag='all')['Price'], 0)

        # Print the output from running the function
        print("Default sabr_volatility_calibrate: ",
              SABRVolatility().calibrate())
        print("Revalued sabr_volatility_calibrate: ",
              SABRVolatility().calibrate(
                  F=90, K=75, T=1, r=0.03, atmvol=0.25, beta=0.9, volvol=0.3,
                  rho=-0.2, option='call', timing=True,
                  output_flag='all')['Price'])


if __name__ == '__main__':
    unittest.main()
