import unittest
import optionmodels.models as mod

class ModelsTestCase(unittest.TestCase):
    
    # For each function, test with defaults and with specified parameters 
    
    def test_black_scholes_merton(self):

        # Test if the output is a float        
        self.assertIsInstance(mod.Pricer().black_scholes_merton(), float)
        self.assertIsInstance(mod.Pricer().black_scholes_merton(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, option='put', 
            timing=True), float)
        
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().black_scholes_merton(), 0)
        self.assertGreater(mod.Pricer().black_scholes_merton(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, option='put', 
            timing=True), 0)
        
        # Print the output from running the function
        print("Default black_scholes_merton: ", 
              mod.Pricer().black_scholes_merton())
        print("Revalued black_scholes_merton: ", 
              mod.Pricer().black_scholes_merton(
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, option='put', 
                  timing=True))
 
        
    def test_black_scholes_merton_vega(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.Pricer().black_scholes_merton_vega(), float)
        self.assertIsInstance(mod.Pricer().black_scholes_merton_vega(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, option='put', 
            timing=True), float)
      
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().black_scholes_merton_vega(), 0)
        self.assertGreater(mod.Pricer().black_scholes_merton_vega(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, option='put', 
            timing=True), 0)
        
        # Print the output from running the function
        print("Default black_scholes_merton_vega: ", 
              mod.Pricer().black_scholes_merton_vega()) 
        print("Revalued black_scholes_merton_vega: ", 
              mod.Pricer().black_scholes_merton_vega(
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, option='put', 
                  timing=True))


    def test_black_76(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.Pricer().black_76(), float)
        self.assertIsInstance(mod.Pricer().black_76(
            F=50, K=55, T=1, r=0.05, sigma=0.3, option='put', 
            timing=True), float)
     
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().black_76(), 0)
        self.assertGreater(mod.Pricer().black_76(
            F=50, K=55, T=1, r=0.05, sigma=0.3, option='put', 
            timing=True), 0)
        
        # Print the output from running the function
        print("Default black_76: ", mod.Pricer().black_76()) 
        print("Revalued black_76: ", mod.Pricer().black_76(
            F=50, K=55, T=1, r=0.05, sigma=0.3, option='put', 
            timing=True))


    def test_european_binomial(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.Pricer().european_binomial(), float)
        self.assertIsInstance(mod.Pricer().european_binomial(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, 
            option='put', timing=True), float)
    
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().european_binomial(), 0)
        self.assertGreater(mod.Pricer().european_binomial(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, 
            option='put', timing=True), 0)
        
        # Print the output from running the function
        print("Default european_binomial: ", mod.Pricer().european_binomial())        
        print("Revalued european_binomial: ", mod.Pricer().european_binomial(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, 
            option='put', timing=True))


    def test_cox_ross_rubinstein_binomial(self):
        
        # Test if the output is a float
        self.assertIsInstance(
            mod.Pricer().cox_ross_rubinstein_binomial(), float)
        self.assertIsInstance(mod.Pricer().cox_ross_rubinstein_binomial(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, 
            output_flag='all', option='put', american=True, 
            timing=True)['Price'], float)
    
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().cox_ross_rubinstein_binomial(), 0)
        self.assertGreater(mod.Pricer().cox_ross_rubinstein_binomial(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, 
            output_flag='all', option='put', american=True, 
            timing=True)['Price'], 0)
        
        # Print the output from running the function
        print("Default cox_ross_rubinstein_binomial: ", 
              mod.Pricer().cox_ross_rubinstein_binomial())
        print("Revalued cox_ross_rubinstein_binomial: ", 
              mod.Pricer().cox_ross_rubinstein_binomial(
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, 
                  output_flag='all', option='put', american=True, 
                  timing=True)['Price'])
                

    def test_leisen_reimer_binomial(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.Pricer().leisen_reimer_binomial(), float)
        self.assertIsInstance(mod.Pricer().leisen_reimer_binomial(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, 
            output_flag='all', option='put', american=True, 
            timing=True)['Price'], float)
      
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().leisen_reimer_binomial(), 0)
        self.assertGreater(mod.Pricer().leisen_reimer_binomial(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, 
            output_flag='all', option='put', american=True, 
            timing=True)['Price'], 0)
        
        # Print the output from running the function
        print("Default leisen_reimer_binomial: ", 
              mod.Pricer().leisen_reimer_binomial())
        print("Revalued leisen_reimer_binomial: ", 
              mod.Pricer().leisen_reimer_binomial(
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, 
                  output_flag='all', option='put', american=True, 
                  timing=True)['Price'])


    def test_trinomial_tree(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.Pricer().trinomial_tree(), float)
        self.assertIsInstance(mod.Pricer().trinomial_tree(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, 
            output_flag='all', option='put', american=True, 
            timing=True)['Price'], float)
        
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().trinomial_tree(), 0)
        self.assertGreater(mod.Pricer().trinomial_tree(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, 
            output_flag='all', option='put', american=True, 
            timing=True)['Price'], 0)
        
        # Print the output from running the function 
        print("Default trinomial_tree: ", mod.Pricer().trinomial_tree())
        print("Revalued trinomial_tree: ", mod.Pricer().trinomial_tree(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, 
            output_flag='all', option='put', american=True, 
            timing=True)['Price'])


    def test_implied_trinomial_tree(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.Pricer().implied_trinomial_tree(), float)
        self.assertIsInstance(mod.Pricer().implied_trinomial_tree(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps_itt=5, step=4, 
            state=4, skew=0.0005, output_flag='price', option='put', 
            timing=True), float) 
        
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().implied_trinomial_tree(), 0)
        self.assertGreater(mod.Pricer().implied_trinomial_tree(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps_itt=5, step=4, 
            state=4, skew=0.0005, output_flag='price', option='put', 
            timing=True), 0)
        
        # Print the output from running the function
        print("Default implied_trinomial_tree: ", 
              mod.Pricer().implied_trinomial_tree())
        print("Revalued implied_trinomial_tree: ", 
              mod.Pricer().implied_trinomial_tree(
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps_itt=5, 
                  step=4, state=4, skew=0.0005, output_flag='price', 
                  option='put', timing=True))
        
        
    def test_explicit_finite_difference(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.Pricer().explicit_finite_difference(), float)
        self.assertIsInstance(mod.Pricer().explicit_finite_difference(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, nodes=50, 
            option='put', american=True, timing=True), float)
        
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().explicit_finite_difference(), 0)
        self.assertGreater(mod.Pricer().explicit_finite_difference(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, nodes=50, 
            option='put', american=True, timing=True), 0)
        
        # Print the output from running the function
        print("Default explicit_finite_difference: ", 
              mod.Pricer().explicit_finite_difference())
        print("Revalued explicit_finite_difference: ", 
              mod.Pricer().explicit_finite_difference(
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, nodes=50, 
                  option='put', american=True, timing=True))


    def test_implicit_finite_difference(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.Pricer().implicit_finite_difference(), float)
        self.assertIsInstance(mod.Pricer().implicit_finite_difference(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, nodes=50, 
            option='put', american=True, timing=True), float)
        
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().implicit_finite_difference(), 0)
        self.assertGreater(mod.Pricer().implicit_finite_difference(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, nodes=50, 
            option='put', american=True, timing=True), 0)
        
        # Print the output from running the function
        print("Default implicit_finite_difference: ", 
              mod.Pricer().implicit_finite_difference())
        print("Revalued implicit_finite_difference: ", 
              mod.Pricer().implicit_finite_difference(
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, 
                  nodes=50, option='put', american=True, timing=True))


    def test_explicit_finite_difference_lns(self):
        
        # Test if the output is a float
        self.assertIsInstance(
            mod.Pricer().explicit_finite_difference_lns(), float)
        self.assertIsInstance(mod.Pricer().explicit_finite_difference_lns(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps_itt=20, nodes=50, 
            option='put', american=True, timing=True), float)
        
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().explicit_finite_difference_lns(), 0)
        self.assertGreater(mod.Pricer().explicit_finite_difference_lns(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps_itt=20, nodes=50, 
            option='put', american=True, timing=True), 0)
        
        # Print the output from running the function
        print("Default explicit_finite_difference_lns: ", 
              mod.Pricer().explicit_finite_difference_lns())
        print("Revalued explicit_finite_difference_lns: ", 
              mod.Pricer().explicit_finite_difference_lns(
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps_itt=20, 
                  nodes=50, option='put', american=True, timing=True))
        
        
    def test_crank_nicolson(self):
        
        # Test if the output is a float
        self.assertIsInstance(
            mod.Pricer().crank_nicolson(), float)
        self.assertIsInstance(mod.Pricer().crank_nicolson(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, nodes=50, 
            option='put', american=True, timing=True), float)
        
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().crank_nicolson(), 0)
        self.assertGreater(mod.Pricer().crank_nicolson(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, nodes=50, 
            option='put', american=True, timing=True), 0)
        
        # Print the output from running the function
        print("Default crank_nicolson: ", mod.Pricer().crank_nicolson())
        print("Revalued crank_nicolson: ", mod.Pricer().crank_nicolson(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, steps=500, nodes=50, 
            option='put', american=True, timing=True))
        

    def test_european_monte_carlo(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.Pricer().european_monte_carlo(), float)
        self.assertIsInstance(mod.Pricer().european_monte_carlo(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, simulations=1000, 
            option='put', timing=True), float)        
        
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().european_monte_carlo(), 0)
        self.assertGreater(mod.Pricer().european_monte_carlo(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, simulations=1000, 
            option='put', timing=True), 0)
        
        # Print the output from running the function
        print("Default european_monte_carlo: ", 
              mod.Pricer().european_monte_carlo())
        print("Revalued european_monte_carlo: ", 
              mod.Pricer().european_monte_carlo(
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, simulations=1000, 
                  option='put', timing=True))
        

    def test_european_monte_carlo_with_greeks(self):
        
        # Test if the output is a float
        self.assertIsInstance(
            mod.Pricer().european_monte_carlo_with_greeks(), float)
        self.assertIsInstance(mod.Pricer().european_monte_carlo_with_greeks(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, simulations=1000, 
            option='put', output_flag='all', timing=True)['Price'], float) 
        
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().european_monte_carlo_with_greeks(), 0)
        self.assertGreater(mod.Pricer().european_monte_carlo_with_greeks(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, simulations=1000, 
            option='put', output_flag='all', timing=True)['Price'], 0)
        
        # Print the output from running the function
        print("Default european_monte_carlo_with_greeks: ", 
              mod.Pricer().european_monte_carlo_with_greeks())
        print("Revalued european_monte_carlo_with_greeks: ", 
              mod.Pricer().european_monte_carlo_with_greeks(
                  S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, simulations=1000, 
                  option='put', output_flag='all', timing=True)['Price'])


    def test_hull_white_87(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.Pricer().hull_white_87(), float)
        self.assertIsInstance(mod.Pricer().hull_white_87(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, vvol=0.3, 
            option='put', timing=True), float)        

        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().hull_white_87(), 0)
        self.assertGreater(mod.Pricer().hull_white_87(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, vvol=0.3, 
            option='put', timing=True), 0)
        
        # Print the output from running the function
        print("Default hull_white_87: ", mod.Pricer().hull_white_87())
        print("Revalued hull_white_87: ", mod.Pricer().hull_white_87(
            S=50, K=55, T=1, r=0.05, q=0.01, sigma=0.3, vvol=0.3, 
            option='put', timing=True))
        
        
    def test_hull_white_88(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.Pricer().hull_white_88(), float)
        self.assertIsInstance(mod.Pricer().hull_white_88(
            S=50, K=55, T=1, r=0.05, q=0.01, sig0=0.07, sigLR=0.05, 
            halflife=0.15, vvol=0.3, rho=0.1, option='put', timing=True), 
            float)        
        
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.Pricer().hull_white_88(), 0)
        self.assertGreater(mod.Pricer().hull_white_88(
            S=50, K=55, T=1, r=0.05, q=0.01, sig0=0.07, sigLR=0.05, 
            halflife=0.15, vvol=0.3, rho=0.1, option='put', timing=True), 0)
        
        # Print the output from running the function
        print("Default hull_white_88: ", mod.Pricer().hull_white_88())
        print("Revalued hull_white_88: ", mod.Pricer().hull_white_88(
            S=50, K=55, T=1, r=0.05, q=0.01, sig0=0.07, sigLR=0.05, 
            halflife=0.15, vvol=0.3, rho=0.1, option='put', timing=True))
        

    def test_implied_vol_newton_raphson(self):
        
        # Test if the output is a float
        self.assertIsInstance(
            mod.ImpliedVol().implied_vol_newton_raphson(), float)
        self.assertIsInstance(mod.ImpliedVol().implied_vol_newton_raphson(
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001, 
            option='put', timing=True), float)
      
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.ImpliedVol().implied_vol_newton_raphson(), 0)
        self.assertGreater(mod.ImpliedVol().implied_vol_newton_raphson(
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001, 
            option='put', timing=True), 0)

        # Print the output from running the function
        print("Default implied_vol_newton_raphson: ", 
              mod.ImpliedVol().implied_vol_newton_raphson())
        print("Revalued implied_vol_newton_raphson: ", 
              mod.ImpliedVol().implied_vol_newton_raphson(
                  S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001, 
                  option='put', timing=True))        


    def test_implied_vol_bisection(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.ImpliedVol().implied_vol_bisection(), float)
        self.assertIsInstance(mod.ImpliedVol().implied_vol_bisection(
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001, 
            option='put', timing=True), float)
        
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.ImpliedVol().implied_vol_bisection(), 0)
        self.assertGreater(mod.ImpliedVol().implied_vol_bisection(
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001, 
            option='put', timing=True), 0)
        
        # Print the output from running the function
        print("Default implied_vol_bisection: ", 
              mod.ImpliedVol().implied_vol_bisection())
        print("Revalued implied_vol_bisection: ", 
              mod.ImpliedVol().implied_vol_bisection(
                  S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001, 
                  option='put', timing=True))
        

    def test_implied_vol_naive(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.ImpliedVol().implied_vol_naive(), float)
        self.assertIsInstance(mod.ImpliedVol().implied_vol_naive(
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001, 
            option='put', timing=True), float)
        
        # Test if the value of the output is greater than zero
        self.assertGreater(mod.ImpliedVol().implied_vol_naive(), 0)
        self.assertGreater(mod.ImpliedVol().implied_vol_naive(
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001, 
            option='put', timing=True), 0)
        
        # Print the output from running the function
        print("Default implied_vol_naive: ", 
              mod.ImpliedVol().implied_vol_naive())
        print("Revalued implied_vol_naive: ", 
              mod.ImpliedVol().implied_vol_naive(
                  S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001, 
                  option='put', timing=True))
        
        
    def test_implied_vol_naive_verbose(self):
        
        # Test if the output is a float
        self.assertIsInstance(
            mod.ImpliedVol().implied_vol_naive_verbose(), float)
        self.assertIsInstance(mod.ImpliedVol().implied_vol_naive_verbose(
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001, 
            option='put', timing=True), float)

        # Test if the value of the output is greater than zero
        self.assertGreater(mod.ImpliedVol().implied_vol_naive_verbose(), 0)
        self.assertGreater(mod.ImpliedVol().implied_vol_naive_verbose(
            S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001, 
            option='put', timing=True), 0)
        
        # Print the output from running the function
        print("Default implied_vol_naive_verbose: ", 
              mod.ImpliedVol().implied_vol_naive_verbose())
        print("Revalued implied_vol_naive_verbose: ", 
              mod.ImpliedVol().implied_vol_naive_verbose(
                  S=50, K=55, T=1, r=0.05, q=0.01, cm=7.57, epsilon=0.001, 
                  option='put', timing=True))
        

    def test_sabr_volatility_calibrate(self):
        
        # Test if the output is a float
        self.assertIsInstance(mod.SABRVolatility().calibrate(), float)
        self.assertIsInstance(mod.SABRVolatility().calibrate(
            F=90, K=75, T=1, r=0.03, atmvol=0.25, beta=0.9, volvol=0.3, 
            rho=-0.2, option='call', timing=True, 
            output_flag='all')['Price'], float)        

        # Test if the value of the output is greater than zero
        self.assertGreater(mod.SABRVolatility().calibrate(), 0)
        self.assertGreater(mod.SABRVolatility().calibrate(
            F=90, K=75, T=1, r=0.03, atmvol=0.25, beta=0.9, volvol=0.3, 
            rho=-0.2, option='call', timing=True, 
            output_flag='all')['Price'], 0)
        
        # Print the output from running the function
        print("Default sabr_volatility_calibrate: ", 
              mod.SABRVolatility().calibrate())
        print("Revalued sabr_volatility_calibrate: ", 
              mod.SABRVolatility().calibrate(
                  F=90, K=75, T=1, r=0.03, atmvol=0.25, beta=0.9, volvol=0.3, 
                  rho=-0.2, option='call', timing=True, 
                  output_flag='all')['Price'])
        
        
if __name__ == '__main__':
    unittest.main()
        

