"""
Methods for extracting implied volatility from option prices

"""

import numpy as np
from optionmodels.analyticalmethods import AnalyticalMethods
from optionmodels.utils import Utils
# pylint: disable=invalid-name

class ImpliedVol():
    """
    Methods for extracting implied volatility from option prices

    """
    @staticmethod
    def implied_vol_newton_raphson(**kwargs):
        """
        Finds implied volatility using Newton-Raphson method - needs
        knowledge of partial derivative of option pricing formula
        with respect to volatility (vega)

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
        cm : Float
            # Option price used to solve for vol. The default is 5.
        epsilon : Float
            Degree of precision. The default is 0.0001
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
            Implied Volatility.

        """

        # Update pricing input parameters to default if not supplied
        if 'refresh' in kwargs and kwargs['refresh']:
            params = Utils.init_params(kwargs)
            S = params['S']
            K = params['K']
            T = params['T']
            r = params['r']
            q = params['q']
            cm = params['cm']
            epsilon = params['epsilon']
            option = params['option']

        # Manaster and Koehler seed value
        vi = np.sqrt(abs(np.log(S / K) + r * T) * (2 / T))

        ci = AnalyticalMethods.black_scholes_merton(
            S=S, K=K, T=T, r=r, q=q, sigma=vi, option=option, refresh=True)

        vegai = AnalyticalMethods.black_scholes_merton_vega(
            S=S, K=K, T=T, r=r, q=q, sigma=vi, refresh=True)

        mindiff = abs(cm - ci)

        while abs(cm - ci) >= epsilon and abs(cm - ci) <= mindiff:
            vi = vi - (ci - cm) / vegai

            ci = AnalyticalMethods.black_scholes_merton(
                S=S, K=K, T=T, r=r, q=q, sigma=vi, option=option, refresh=True)

            vegai = AnalyticalMethods.black_scholes_merton_vega(
                S=S, K=K, T=T, r=r, q=q, sigma=vi, refresh=True)

            mindiff = abs(cm - ci)

        if abs(cm - ci) < epsilon:
            result = vi
        else:
            result = 'NA'

        return result


    @staticmethod
    def implied_vol_bisection(**kwargs):
        """
        Finds implied volatility using bisection method.

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
        cm : Float
            # Option price used to solve for vol. The default is 5.
        epsilon : Float
            Degree of precision. The default is 0.0001
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
            Implied Volatility.

        """

        # Update pricing input parameters to default if not supplied
        if 'refresh' in kwargs and kwargs['refresh']:
            params = Utils.init_params(kwargs)
            S = params['S']
            K = params['K']
            T = params['T']
            r = params['r']
            q = params['q']
            cm = params['cm']
            epsilon = params['epsilon']
            option = params['option']

        vLow = 0.005
        vHigh = 4
        cLow = AnalyticalMethods.black_scholes_merton(
            S=S, K=K, T=T, r=r, q=q, sigma=vLow, option=option, refresh=True)

        cHigh = AnalyticalMethods.black_scholes_merton(
            S=S, K=K, T=T, r=r, q=q, sigma=vHigh, option=option, refresh=True)

        counter = 0

        vi = vLow + (cm - cLow) * (vHigh - vLow) / (cHigh - cLow)

        while abs(cm - AnalyticalMethods.black_scholes_merton(
                S=S, K=K, T=T, r=r, q=q, sigma=vi, option=option,
                refresh=True)) > epsilon:

            counter = counter + 1
            if counter == 100:
                result = 'NA'

            if AnalyticalMethods.black_scholes_merton(
                    S=S, K=K, T=T, r=r, q=q, sigma=vi, option=option,
                    refresh=True) < cm:
                vLow = vi

            else:
                vHigh = vi

            cLow = AnalyticalMethods.black_scholes_merton(
                S=S, K=K, T=T, r=r, q=q, sigma=vLow, option=option,
                refresh=True)

            cHigh = AnalyticalMethods.black_scholes_merton(
                S=S, K=K, T=T, r=r, q=q, sigma=vHigh, option=option,
                refresh=True)

            vi = vLow + (cm - cLow) * (vHigh - vLow) / (cHigh - cLow)

        result = vi

        return result


    @staticmethod
    def implied_vol_naive(**kwargs):
        """
        Finds implied volatility using simple naive iteration,
        increasing precision each time the difference changes sign.

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
        cm : Float
            # Option price used to solve for vol. The default is 5.
        epsilon : Float
            Degree of precision. The default is 0.0001
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
            Implied Volatility.

        """

        # Update pricing input parameters to default if not supplied
        if 'refresh' in kwargs and kwargs['refresh']:
            params = Utils.init_params(kwargs)
            S = params['S']
            K = params['K']
            T = params['T']
            r = params['r']
            q = params['q']
            cm = params['cm']
            epsilon = params['epsilon']
            option = params['option']

        # Seed vol
        vi = 0.2

        # Calculate starting option price using this vol
        ci = AnalyticalMethods.black_scholes_merton(
            S=S, K=K, T=T, r=r, q=q, sigma=vi, option=option, refresh=True)

        # Initial price difference
        price_diff = cm - ci

        if price_diff > 0:
            flag = 1

        else:
            flag = -1

        # Starting vol shift size
        shift = 0.01

        price_diff_start = price_diff

        while abs(price_diff) > epsilon:

            # If the price difference changes sign after the vol shift,
            # reduce the decimal by one and reverse the sign
            if np.sign(price_diff) != np.sign(price_diff_start):
                shift = shift * -0.1

            # Calculate new vol
            vi += (shift * flag)

            # Set initial price difference
            price_diff_start = price_diff

            # Calculate the option price with new vol
            ci = AnalyticalMethods.black_scholes_merton(
                S=S, K=K, T=T, r=r, q=q, sigma=vi, option=option, refresh=True)

            # Price difference after shifting vol
            price_diff = cm - ci

            # If values are diverging reverse the shift sign
            if abs(price_diff) > abs(price_diff_start):
                shift = -shift

        result = vi

        return result


    @staticmethod
    def implied_vol_naive_verbose(**kwargs):
        """
        Finds implied volatility using simple naive iteration,
        increasing precision each time the difference changes sign.

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
        cm : Float
            # Option price used to solve for vol. The default is 5.
        epsilon : Float
            Degree of precision. The default is 0.0001
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
            Implied Volatility.

        """

        # Update pricing input parameters to default if not supplied
        if 'refresh' in kwargs and kwargs['refresh']:
            params = Utils.init_params(kwargs)
            S = params['S']
            K = params['K']
            T = params['T']
            r = params['r']
            q = params['q']
            cm = params['cm']
            epsilon = params['epsilon']
            option = params['option']

        vi = 0.2
        ci = AnalyticalMethods.black_scholes_merton(
            S=S, K=K, T=T, r=r, q=q, sigma=vi, option=option, refresh=True)

        price_diff = cm - ci
        if price_diff > 0:
            flag = 1
        else:
            flag = -1
        while abs(price_diff) > epsilon:
            while price_diff * flag > 0:
                ci = AnalyticalMethods.black_scholes_merton(
                    S=S, K=K, T=T, r=r, q=q, sigma=vi, option=option,
                    refresh=True)

                price_diff = cm - ci
                vi += (0.01 * flag)

            while price_diff * flag < 0:
                ci = AnalyticalMethods.black_scholes_merton(
                    S=S, K=K, T=T, r=r, q=q, sigma=vi, option=option,
                    refresh=True)

                price_diff = cm - ci
                vi -= (0.001 * flag)

            while price_diff * flag > 0:
                ci = AnalyticalMethods.black_scholes_merton(
                    S=S, K=K, T=T, r=r, q=q, sigma=vi, option=option,
                    refresh=True)

                price_diff = cm - ci
                vi += (0.0001 * flag)

            while price_diff * flag < 0:
                ci = AnalyticalMethods.black_scholes_merton(
                    S=S, K=K, T=T, r=r, q=q, sigma=vi, option=option,
                    refresh=True)

                price_diff = cm - ci
                vi -= (0.00001 * flag)

            while price_diff * flag > 0:
                ci = AnalyticalMethods.black_scholes_merton(
                    S=S, K=K, T=T, r=r, q=q, sigma=vi, option=option,
                    refresh=True)

                price_diff = cm - ci
                vi += (0.000001 * flag)

            while price_diff * flag < 0:
                ci = AnalyticalMethods.black_scholes_merton(
                    S=S, K=K, T=T, r=r, q=q, sigma=vi, option=option,
                    refresh=True)

                price_diff = cm - ci
                vi -= (0.0000001 * flag)

        result = vi

        return result
