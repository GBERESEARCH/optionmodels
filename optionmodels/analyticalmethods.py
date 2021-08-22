"""
Analytical option pricing models

"""

import numpy as np
import scipy.stats as si
from optionmodels.utils import Utils
# pylint: disable=invalid-name

class AnalyticalMethods():
    """
    Analytical option pricing models

    """
    @staticmethod
    def black_scholes_merton(**kwargs):
        """
        Black-Scholes-Merton Option price

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
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.

        Returns
        -------
        opt_price : Float
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
            option = params['option']

        b = r - q
        carry = np.exp((b - r) * T)
        d1 = ((np.log(S / K) + (b + (0.5 * sigma ** 2)) * T)
              / (sigma * np.sqrt(T)))
        d2 = ((np.log(S / K) + (b - (0.5 * sigma ** 2)) * T)
              / (sigma * np.sqrt(T)))

        # Cumulative normal distribution function
        Nd1 = si.norm.cdf(d1, 0.0, 1.0)
        minusNd1 = si.norm.cdf(-d1, 0.0, 1.0)
        Nd2 = si.norm.cdf(d2, 0.0, 1.0)
        minusNd2 = si.norm.cdf(-d2, 0.0, 1.0)

        if option == "call":
            opt_price = ((S * carry * Nd1) - (K * np.exp(-r * T) * Nd2))
        if option == 'put':
            opt_price = ((K * np.exp(-r * T) * minusNd2) -
                         (S * carry * minusNd1))

        return opt_price


    @staticmethod
    def black_scholes_merton_vega(**kwargs):
        """
        Black-Scholes-Merton Option Vega

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
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.

        Returns
        -------
        opt_vega : Float
            Option Vega.

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

        b = r - q
        carry = np.exp((b - r) * T)
        d1 = ((np.log(S / K) + (b + (0.5 * sigma ** 2)) * T)
              / (sigma * np.sqrt(T)))
        nd1 = (1 / np.sqrt(2 * np.pi)) * (np.exp(-d1 ** 2 * 0.5))

        opt_vega = S * carry * nd1 * np.sqrt(T)

        return opt_vega


    @staticmethod
    def black_76(**kwargs):
        """
        Black 76 Futures Option price

        Parameters
        ----------
        F : Float
            Discounted Futures Price.
        K : Float
            Strike Price. The default is 100.
        T : Float
            Time to Maturity.  The default is 0.25 (3 Months).
        r : Float
            Interest Rate. The default is 0.005 (50bps)
        sigma : Float
            Implied Volatility.  The default is 0.2 (20%).
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.

        Returns
        -------
        opt_price : Float
            Option Price.

        """

        # Update pricing input parameters to default if not supplied
        if 'refresh' in kwargs and kwargs['refresh']:
            params = Utils.init_params(kwargs)
            F = params['F']
            K = params['K']
            T = params['T']
            r = params['r']
            sigma = params['sigma']
            option = params['option']

        carry = np.exp(-r * T)
        d1 = (np.log(F / K) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(F / K) + (-0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

        # Cumulative normal distribution function
        Nd1 = si.norm.cdf(d1, 0.0, 1.0)
        minusNd1 = si.norm.cdf(-d1, 0.0, 1.0)
        Nd2 = si.norm.cdf(d2, 0.0, 1.0)
        minusNd2 = si.norm.cdf(-d2, 0.0, 1.0)

        if option == "call":
            opt_price = ((F * carry * Nd1) - (K * np.exp(-r * T) * Nd2))
        if option == 'put':
            opt_price = ((K * np.exp(-r * T) * minusNd2)
                         - (F * carry * minusNd1))

        return opt_price
