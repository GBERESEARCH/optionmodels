"""
Methods for extracting implied volatility from option prices

"""

import numpy as np
from scipy.optimize import brentq
from scipy.special import erfcx
import scipy.stats as si
from optionmodels.analyticalmethods import AnalyticalMethods
from optionmodels.latticemethods import LatticeMethods
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
                return 'NA'

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


    @staticmethod
    def implied_vol_lattice(**kwargs):
        """
        Finds implied volatility by inverting the Leisen-Reimer binomial
        model, European or American, using Brent's method. The bracket's
        upper bound is set from the Black-Scholes implied vol of the price.

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
        steps : Int
            Number of time steps. Increased by one if even. The default
            is 1000.
        american : Bool
            Whether the option is American. The default is False.

        Returns
        -------
        result : Float
            Implied Volatility, or 'NA' if the price has no time value or
            lies outside the range spanned by vols of 1% and 500%.

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
            steps = params['steps']
            american = params['american']

        # Leisen-Reimer uses an odd number of steps
        if steps % 2 == 0:
            steps = steps + 1

        def price_diff(sigma):
            return LatticeMethods.leisen_reimer_binomial(
                S=S, K=K, T=T, r=r, q=q, sigma=sigma, steps=steps,
                option=option, output_flag='price', american=american,
                refresh=True) - cm

        vLow = 0.01
        vHigh = 5

        # No solution if the price is at or below the price at the lower
        # volatility bound (no time value)
        if price_diff(vLow) > -epsilon:
            return 'NA'

        # The Black-Scholes implied vol of the price is an upper bound for an
        # American option and close to the answer for a European option; use
        # it to narrow the bracket, otherwise check the price against the
        # upper volatility bound
        sigma_bs = ImpliedVol.implied_vol_inverse_gauss(
            S=S, K=K, T=T, r=r, q=q, cm=cm, option=option, refresh=True)

        if (not isinstance(sigma_bs, str)
                and price_diff(min(1.1 * sigma_bs + 0.01, vHigh)) >= 0):
            vHigh = min(1.1 * sigma_bs + 0.01, vHigh)
        elif price_diff(vHigh) < 0:
            return 'NA'

        vi = brentq(price_diff, vLow, vHigh, xtol=1e-8)

        if abs(price_diff(vi)) < epsilon:
            result = vi
        else:
            result = 'NA'

        return result


    @staticmethod
    def implied_vol_jaeckel(**kwargs):
        """
        Finds implied volatility using Jäckel's Let's Be Rational method.

        Uses a four-regime rational initial guess, the normalised Black
        formula via erfcx to avoid underflow at extreme strikes, and
        Halley's third-order iteration to achieve machine-precision
        convergence, typically in two iterations.

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
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.

        Returns
        -------
        result : Float
            Implied Volatility, or 'NA' if the price is outside the
            no-arbitrage bounds or has no time value.

        References
        ----------
        Jäckel, P. (2015). Let's be rational. Wilmott, 75, 40-53.
        Jäckel, P. (2024). Reference implementation.
            http://www.jaeckel.org/LetsBeRational.7z. Revision 1520.

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
            option = params['option']

        sqrt2 = np.sqrt(2.0)
        sqrt2pi = np.sqrt(2.0 * np.pi)

        # Forward price and discount factor
        F = S * np.exp((r - q) * T)
        D = np.exp(-r * T)

        # Convert put to call via put-call parity
        if option == 'put':
            cm_call = cm + D * (F - K)
        else:
            cm_call = cm

        # Normalised call price; log-moneyness x = log(F/K)
        beta = cm_call / (D * F)
        x = np.log(F / K)

        # Normalised intrinsic value and no-arbitrage bounds
        beta_intrinsic = max(1.0 - np.exp(-x), 0.0)
        if beta <= beta_intrinsic + 1e-14 or beta >= 1.0 - 1e-14:
            return 'NA'

        # Reflect ITM calls to OTM to obtain absolute moneyness and OTM price
        if x > 0.0:
            x_abs = x
            p = beta - (1.0 - np.exp(-x))
        else:
            x_abs = -x
            p = beta

        if p <= 0.0:
            return 'NA'

        # Initial guess: four regimes based on moneyness and price
        if x_abs < 1e-7:
            # Regime 1, at the money: inversion of beta = sigma / sqrt(2 pi)
            sigma = sqrt2pi * beta

        elif p >= 0.05:
            # Regimes 2 and 3, moderately out of the money: interpolates
            # between the at-the-money limit (sigma = p sqrt(2 pi)) and the
            # moneyness limit (sigma = |x|)
            sigma = np.sqrt(x_abs * x_abs + (sqrt2pi * p) * (sqrt2pi * p))

        else:
            # Regime 4, deep out of the money: the Mills-ratio approximation
            # of the normal tail gives |d+| = sqrt(-2 log(p)), so
            # sigma = |x| / |d+|
            log_p = np.log(p)
            if -2.0 * log_p < 1e-14:
                return 'NA'
            sigma = x_abs / np.sqrt(-2.0 * log_p)

        sigma = max(min(sigma, 10.0), 1e-9)

        # Halley iteration
        # Normalised vega:  f'  = phi(d+)
        # Second deriv:     f'' = phi(d+) * d+ * (x / sigma^2 - 0.5)
        # Halley step:      sigma -= 2 eta / (2 - eta f2r)
        #   where eta = residual / vega and f2r = f'' / f'
        for _ in range(8):
            d_p = x / sigma + 0.5 * sigma
            d_m = d_p - sigma

            # Normalised Black via erfcx:
            # Phi(d) = erfcx(-d/sqrt(2)) exp(-d^2/2) / 2
            # Avoids underflow to zero for large negative d values
            beta_calc = (
                erfcx(-d_p / sqrt2) * np.exp(-0.5 * d_p * d_p)
                - np.exp(-x) * erfcx(-d_m / sqrt2) * np.exp(-0.5 * d_m * d_m)
                ) / 2.0

            residual = beta_calc - beta

            if abs(residual) < 1e-14:
                break

            vega = si.norm.pdf(d_p)
            if vega < 1e-16:
                break

            eta = residual / vega
            f2r = d_p * (x / (sigma * sigma) - 0.5)
            halley_denom = 2.0 - eta * f2r

            if abs(halley_denom) < 1e-14:
                sigma = sigma - eta
            else:
                sigma = sigma - 2.0 * eta / halley_denom

            sigma = max(sigma, 1e-9)

        # Convert total vol sigma * sqrt(T) to annualised
        result = sigma / np.sqrt(T)

        return result


    @staticmethod
    def implied_vol_inverse_gauss(**kwargs):
        """
        Finds implied volatility using an explicit closed-form solution
        via the inverse Gaussian quantile function (Schadner, 2026).

        The normalised call price is identified as the survival probability
        of an inverse Gaussian distribution. Inverting this identity gives
        implied volatility directly, requiring no initial guess, iterative
        inversion, or approximation.

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
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.

        Returns
        -------
        result : Float
            Implied Volatility, or 'NA' if the price is outside the
            no-arbitrage bounds or has no time value.

        References
        ----------
        Schadner, W. (2026). An Explicit Solution to Black-Scholes Implied
        Volatility. arXiv:2604.24480.

        Notes
        -----
        Uses scipy.stats.invgauss, which parameterises the inverse Gaussian
        as IG(mu, lambda=1) when scale=1, matching the paper's convention.

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
            option = params['option']

        # Forward price and discount factor
        F = S * np.exp((r - q) * T)
        D = np.exp(-r * T)

        # Forward log-moneyness
        k = np.log(K / F)

        # Normalised option price
        c = cm / (D * F)

        # Normalised intrinsic value; no solution if the price has no time
        # value
        if option == 'put':
            c_intrinsic = max(np.exp(k) - 1.0, 0.0)
        else:
            c_intrinsic = max(1.0 - np.exp(k), 0.0)
        if c <= c_intrinsic + 1e-14:
            return 'NA'

        # At the forward: closed form via the normal quantile (Eq. 2). Call
        # and put prices are equal here by put-call parity
        if k == 0:
            if c >= 1.0:
                return 'NA'
            result = (2 / np.sqrt(T)) * si.norm.ppf((c + 1) / 2)
            return result

        # Scaling factor m (same for calls and puts, Eq. 1 and Eq. 9)
        m = 1.0 if K > F else K / F

        # Inverse Gaussian mean parameter mu = 2 / |k|, shape lambda = 1
        # (scipy scale=1)
        ig_mu = 2.0 / abs(k)

        # Probability argument per option type (Eq. 1 for calls, Eq. 9 for
        # puts)
        if option == 'put':
            ig_q = (np.exp(k) - c) / m
        else:
            ig_q = (1.0 - c) / m

        # Guard against quantile arguments outside (0, 1)
        if not 0.0 < ig_q < 1.0:
            return 'NA'

        ig_quantile = si.invgauss.ppf(ig_q, ig_mu)

        if not np.isfinite(ig_quantile) or ig_quantile <= 0:
            return 'NA'

        # Total implied volatility v = 2 / sqrt(quantile), then
        # sigma = v / sqrt(T)
        vi = 2.0 / np.sqrt(ig_quantile)
        result = vi / np.sqrt(T)

        return result
