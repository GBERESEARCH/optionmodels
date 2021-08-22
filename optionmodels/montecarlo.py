"""
MonteCarlo option methods

"""

import random
import numpy as np
from scipy.stats import norm
from optionmodels.utils import Utils
# pylint: disable=invalid-name

class MonteCarlo():
    """
    MonteCarlo option methods

    """
    @staticmethod
    def european_monte_carlo(**kwargs):
        """
        Standard Monte Carlo

        Parameters
        ----------
        S : Float
            Stock Price. The default is 100.
        K : Float
            Strike Price. The default is 100.
        T : Float
            Time to Maturity.  The default is 0.25 (3 Months).
        r : Float
            Interest Rate. The default is 0.005 (50bps)
        q : Float
            Dividend Yield.  The default is 0.
        sigma : Float
            Implied Volatility.  The default is 0.2 (20%).
        simulations : Int
            Number of Monte Carlo runs. The default is 10000.
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.
        default : Bool
            Whether the function is being called directly (in which
            case values that are not supplied are set to default
            values) or called from another function where they have
            already been updated.

        Returns
        -------
        result : Float
            Option Price.

        """

        # Update pricing input parameters to default if not supplied
        if 'refresh' in kwargs and kwargs['refresh']:
            params = Utils.init_params(kwargs)
            S = params['S']
            K = params['K']
            T = params['T']
            r = params['r']
            q = params['q']
            sigma = params['sigma']
            simulations = params['simulations']
            option = params['option']

        if option == 'call':
            z = 1
        else:
            z = -1

        b = r - q
        Drift = (b - (sigma ** 2) / 2) * T
        sigmarT = sigma * np.sqrt(T)
        val = 0

        counter = 1
        while counter < simulations + 1:
            St = S * np.exp(
                Drift + sigmarT * norm.ppf(random.random(), loc=0, scale=1))
            val = val + max(z * (St - K), 0)
            counter += 1

        result = np.exp(-r * T) * val / simulations

        return result


    @staticmethod
    def european_monte_carlo_with_greeks(**kwargs):
        """
        Standard Monte Carlo with Greeks

        Parameters
        ----------
        S : Float
            Stock Price. The default is 100.
        K : Float
            Strike Price. The default is 100.
        T : Float
            Time to Maturity.  The default is 0.25 (3 Months).
        r : Float
            Interest Rate. The default is 0.005 (50bps)
        q : Float
            Dividend Yield.  The default is 0.
        sigma : Float
            Implied Volatility.  The default is 0.2 (20%).
        simulations : Int
            Number of Monte Carlo runs. The default is 10000.
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.
        output_flag : Str
            Whether to return 'price', 'delta', 'gamma', 'theta',
            'vega' or 'all'. The default is 'price'.
        default : Bool
            Whether the function is being called directly (in which
            case values that are not supplied are set to default
            values) or called from another function where they have
            already been updated.

        Returns
        -------
        result : Various
            Depending on output flag:
                'price' : Float; Option Price
                'delta' : Float; Option Delta
                'gamma' : Float; Option Gamma
                'theta' : Float; Option Theta
                'vega' : Float; Option Vega
                'all' : Dict; Option Price, Option Delta, Option
                               Gamma, Option Theta, Option Vega

        """

        # Update pricing input parameters to default if not supplied
        if 'refresh' in kwargs and kwargs['refresh']:
            params = Utils.init_params(kwargs)
            S = params['S']
            K = params['K']
            T = params['T']
            r = params['r']
            q = params['q']
            sigma = params['sigma']
            simulations = params['simulations']
            option = params['option']
            output_flag = params['output_flag']

        if option == 'call':
            z = 1
        else:
            z = -1

        b = r - q
        Drift = (b - (sigma ** 2) / 2) * T
        sigmarT = sigma * np.sqrt(T)
        val = 0
        deltasum = 0
        gammasum = 0
        output = np.zeros((5))

        counter = 1
        while counter < simulations + 1:
            St = S * np.exp(
                Drift + sigmarT * norm.ppf(random.random(), loc=0, scale=1))
            val = val + max(z * (St - K), 0)
            if z == 1 and St > K:
                deltasum = deltasum + St
            if z == -1 and St < K:
                deltasum = deltasum + St
            if abs(St - K) < 2:
                gammasum = gammasum + 1
            counter += 1

        # Option Value
        output[0] = np.exp(-r * T) * val / simulations

        # Delta
        output[1] = np.exp(-r * T) * deltasum / (simulations * S)

        # Gamma
        output[2] = (np.exp(-r * T) * ((K / S) ** 2)
                     * gammasum / (4 * simulations))

        # Theta
        output[3] = ((r * output[0]
                      - b * S * output[1]
                      - (0.5 * (sigma ** 2) * (S ** 2) * output[2]))
                     / 365)

        # Vega
        output[4] = output[2] * sigma * (S ** 2) * T / 100

        output_dict = {
            'price':output[0],
            'delta':output[1],
            'gamma':output[2],
            'theta':output[3],
            'vega':output[4],
            'all':{
                'Price':output[0],
                'Delta':output[1],
                'Gamma':output[2],
                'Theta':output[3],
                'Vega':output[4]
                }
            }

        result = output_dict.get(
            output_flag, 'Please enter a valid output flag')

#        if output_flag == 'price':
#            result = output[0]
#        if output_flag == 'delta':
#            result = output[1]
#        if output_flag == 'gamma':
#            result = output[2]
#        if output_flag == 'theta':
#            result = output[3]
#        if output_flag == 'vega':
#            result = output[4]
#        if output_flag == 'all':
#            result = {'Price':output[0],
#                      'Delta':output[1],
#                      'Gamma':output[2],
#                      'Theta':output[3],
#                      'Vega':output[4]}

        return result
