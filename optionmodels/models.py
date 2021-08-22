"""
Option pricing models and tools

"""

import copy
from optionmodels.analyticalmethods import AnalyticalMethods # pylint: disable=unused-import
from optionmodels.finitedifferencemethods import FiniteDifference
from optionmodels.impliedvol import ImpliedVol
from optionmodels.latticemethods import LatticeMethods
from optionmodels.models_params import models_params_dict
from optionmodels.montecarlo import MonteCarlo
from optionmodels.hullwhite import HullWhite
from optionmodels.utils import Utils

class Pricer():
    """
    Option pricing models and tools

    """
    def __init__(self, **kwargs):

        # Import dictionary of default parameters
        self.default_dict = copy.deepcopy(models_params_dict)

        # Store initial inputs
        inputs = {}
        for key, value in kwargs.items():
            inputs[key] = value

        # Initialise system parameters
        params = Utils.init_params(inputs)

        self.params = params


    @Utils.timer
    def price(self, **kwargs):
        """
        Calculate option price

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
        for param, value in self.params.items():
            if param not in kwargs:
                kwargs[param] = value

        opt_mappings = {
            'AnalyticalMethods':AnalyticalMethods,
            'FiniteDifference':FiniteDifference,
            'LatticeMethods':LatticeMethods,
            'MonteCarlo':MonteCarlo,
            'HullWhite':HullWhite
            }

        method = kwargs['pricer_dict'][kwargs['option_method']][1]
        pricer_type = opt_mappings[
            kwargs['pricer_dict'][kwargs['option_method']][0]]

        option_price = getattr(pricer_type, method)(**kwargs)

        return option_price


    @Utils.timer
    def impliedvol(self, **kwargs):
        """
        Calculate implied volatility from option price.

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
            Option price used to solve for vol. The default is 5.
        epsilon : Float
            Degree of precision. The default is 0.0001
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.

        Returns
        -------
        result : Float
            Implied Volatility.

        """
        for param, value in self.params.items():
            if param not in kwargs:
                kwargs[param] = value

        for key, value in kwargs['implied_vol_method_dict'].items():
            if str(kwargs['vol_method']) == key:
                vol = getattr(ImpliedVol, value)(**kwargs)

        return vol


    @Utils.timer
    def lattice(self, **kwargs):
        """
        Calculate option price

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
        for param, value in self.params.items():
            if param not in kwargs:
                kwargs[param] = value

        method = kwargs['lattice_dict'][kwargs['option_method']]

        option_price = getattr(LatticeMethods, method)(**kwargs)

        return option_price


    @Utils.timer
    def finitedifference(self, **kwargs):
        """
        Calculate option price

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
        for param, value in self.params.items():
            if param not in kwargs:
                kwargs[param] = value

        method = kwargs['finite_difference_dict'][kwargs['option_method']]

        option_price = getattr(FiniteDifference, method)(**kwargs)

        return option_price


    @Utils.timer
    def montecarlo(self, **kwargs):
        """
        Calculate option price

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
        for param, value in self.params.items():
            if param not in kwargs:
                kwargs[param] = value

        method = kwargs['montecarlo_dict'][kwargs['option_method']]

        option_price = getattr(MonteCarlo, method)(**kwargs)

        return option_price


    @Utils.timer
    def hullwhite(self, **kwargs):
        """
        Calculate option price

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
        for param, value in self.params.items():
            if param not in kwargs:
                kwargs[param] = value

        method = kwargs['hullwhite_dict'][kwargs['option_method']]

        option_price = getattr(HullWhite, method)(**kwargs)

        return option_price
