"""
Hull-White option pricing methods

"""

import numpy as np
import scipy.stats as si
from optionmodels.analyticalmethods import AnalyticalMethods
from optionmodels.utils import Utils
# pylint: disable=invalid-name

class HullWhite():
    """
    Hull-White option pricing methods

    """
    @staticmethod
    def hull_white_87(**kwargs):
        """
        Hull White 1987 - Uncorrelated Stochastic Volatility.

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
        vvol : Float
            Vol of vol. The default is 0.5.
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
            Option price.

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
            vvol = params['vvol']
            option = params['option']

        k = vvol ** 2 * T
        ek = np.exp(k)
        b = r - q
        d1 = ((np.log(S / K) + (b + (sigma ** 2) / 2) * T)
              / (sigma * np.sqrt(T)))
        d2 = d1 - sigma * np.sqrt(T)
        Nd1 = si.norm.cdf(d1, 0.0, 1.0)

        cgbs = AnalyticalMethods.black_scholes_merton(
            S=S, K=K, T=T, r=r, q=q, sigma=sigma, option='call', refresh=True)

        # Partial Derivatives
        cVV = (S
               * np.exp((b - r) * T)
               * np.sqrt(T)
               * Nd1
               * (d1 * d2 - 1)
               / (4 * (sigma ** 3)))

        cVVV = (S
                * np.exp((b - r) * T)
                * np.sqrt(T)
                * Nd1
                * ((d1 * d2 - 1) * (d1 * d2 - 3) - ((d1 ** 2) + (d2 ** 2)))
                / (8 * (sigma ** 5)))

        callvalue = (cgbs
                     + 1 / 2
                     * cVV
                     * (2 * sigma ** 4 * (ek - k - 1) / k ** 2 - sigma  ** 4)
                     + (1 / 6 * cVVV * sigma ** 6
                        * (ek ** 3
                           - (9 + 18 * k) * ek
                           + 8
                           + 24 * k
                           + 18 * k ** 2
                           + (6 * k ** 3))
                        / (3 * k ** 3)))

        if option == 'call':
            result = callvalue

        if option == 'put': # use put-call parity
            result = callvalue - S * np.exp((b - r) * T) + K * np.exp(-r * T)

        return result


    @staticmethod
    def hull_white_88(**kwargs):
        """
        Hull White 1988 - Correlated Stochastic Volatility.

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
        sig0 : Float
            Initial Volatility. The default is 0.09 (9%).
        sigLR : Float
            Long run mean reversion level of volatility. The default
            is 0.0625 (6.25%).
        halflife : Float
            Half-life of volatility deviation. The default is 0.1.
        vvol : Float
            Vol of vol. The default is 0.5.
        rho : Float
            Correlation between asset price and volatility. The
            default is 0.
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
            Option price.

        """

        # Update pricing input parameters to default if not supplied
        if 'refresh' in kwargs and kwargs['refresh']:
            params = Utils.init_params(kwargs)
            S = params['S']
            K = params['K']
            T = params['T']
            r = params['r']
            q = params['q']
            sig0 = params['sig0']
            sigLR = params['sigLR']
            halflife = params['halflife']
            vvol = params['vvol']
            rho = params['rho']
            option = params['option']

        b = r - q
        # Find constant, beta, from Half-life
        beta = -np.log(2) / halflife

        # Find constant, a, from long run volatility
        a = -beta * (sigLR ** 2)
        delta = beta * T
        ed = np.exp(delta)
        v = sig0 ** 2

        # Average expected variance
        if abs(beta) < 0.0001:
            vbar = v + 0.5 * a * T
        else:
            vbar = (v + (a / beta)) * ((ed - 1) / delta) - (a / beta)

        d1 = (np.log(S / K) + (b + (vbar / 2)) * T) / np.sqrt(vbar * T)
        d2 = d1 - np.sqrt(vbar * T)

        # standardised normal density function
        nd1 = (1 / np.sqrt(2 * np.pi)) * (np.exp(-d1 ** 2 * 0.5))

        # Cumulative normal distribution function
        Nd1 = si.norm.cdf(d1, 0.0, 1.0)
        Nd2 = si.norm.cdf(d2, 0.0, 1.0)

        # Partial derivatives
        cSV = (-S * np.exp((b - r) * T) * nd1 * (d2 / (2 * vbar)))
        cVV = (
            (S * np.exp((b - r) * T) * nd1 * np.sqrt(T) / (4 * vbar ** 1.5))
            * (d1 * d2 - 1))

        cSVV = (
            (S * np.exp((b - r) * T) / (4 * vbar ** 2))
            * nd1 * ((-d1 * (d2 ** 2)) + d1 + (2 * d2)))

        cVVV = (
            ((S * np.exp((b - r) * T) * nd1 * np.sqrt(T)) / (8 * vbar ** 2.5))
            * ((d1 * d2 - 1) * (d1 * d2 - 3) - ((d1 ** 2) + (d2 ** 2))))

        if abs(beta) < 0.0001:
            f1 = rho * ((a * T / 3) + v) * (T / 2) * cSV
            phi1 = (rho ** 2) * ((a * T / 4) + v) * ((T ** 3) / 6)
            phi2 = (2 + (1 / (rho ** 2))) * phi1
            phi3 = (rho ** 2) * (((a * T / 3) + v) ** 2) * ((T ** 4) / 8)
            phi4 = 2 * phi3

        else: # Beta different from zero
            phi1 = (
                ((rho ** 2) / (beta ** 4))
                * (((a + (beta * v))
                    * ((ed * (((delta ** 2) / 2) - delta + 1)) - 1))
                   + (a * ((ed * (2 - delta)) - (2 + delta)))))

            phi2 = (
                (2 * phi1)
                + ((1 / (2 * (beta ** 4)))
                   * (((a + (beta * v)) * ((ed ** 2) - (2 * delta * ed) - 1))
                      - ((a / 2) * ((ed ** 2) - (4 * ed) + (2 * delta) + 3)))))

            phi3 = (
                ((rho ** 2) / (2 * (beta ** 6)))
                * ((((a + (beta * v)) * (ed - delta * ed - 1))
                    - (a * (1 + delta - ed))) ** 2))

            phi4 = 2 * phi3

            f1 = (
                (rho / ((beta ** 3) * T))
                * (((a + (beta * v)) * (1 - ed + (delta * ed)))
                   + (a * (1 + delta - ed))) * cSV)

        f0 = S * np.exp((b - r) * T) * Nd1 - (K * np.exp(-r * T) * Nd2)

        f2 = (
            ((phi1 / T) * cSV)
            + ((phi2 / (T ** 2)) * cVV)
            + ((phi3 / (T ** 2)) * cSVV)
            + ((phi4 / (T ** 3)) * cVVV))

        callvalue = f0 + f1 * vvol + f2 * vvol ** 2

        if option == 'call':
            result = callvalue
        else:
            result = (
                callvalue - (S * np.exp((b - r) * T)) + (K * np.exp(-r * T)))

        return result
