"""
SABR Volatility calibration

"""

import copy
import math
import numpy as np
from optionmodels.analyticalmethods import AnalyticalMethods
from optionmodels.models_params import sabr_params_dict
from optionmodels.utils import Utils
# pylint: disable=invalid-name

class SABRVolatility():
    """
    Stochastic, Alpha, Beta, Rho model

    Extension of Black 76 model to include an easily implementable
    stochastic volatility model

    Beta will typically be chosen a priori according to how traders
    observe market prices:
        e.g. In FX markets, standard to assume lognormal terms, Beta = 1
             In some Fixed Income markets traders prefer to assume
             normal terms, Beta = 0

    Alpha will need to be calibrated to ATM volatility

    """

    def __init__(self, **kwargs):

        # Import dictionary of default parameters
        self.default_dict = copy.deepcopy(sabr_params_dict)

        # Store initial inputs
        inputs = {}
        for key, value in kwargs.items():
            inputs[key] = value

        # Initialise system parameters
        params = Utils.init_sabr_params(inputs)

        self.params = params


    def calibrate(self, **kwargs):
        """
        Run the SABR calibration

        Returns
        -------
        Float
            Black-76 equivalent SABR volatility and price.

        """
        if 'refresh' not in kwargs:
            kwargs['refresh'] = True

        # Update pricing input parameters to default if not supplied
        if 'refresh' in kwargs and kwargs['refresh']:
            params = Utils.init_sabr_params(kwargs)
            F = params['F']
            K = params['K']
            T = params['T']
            r = params['r']
            atmvol = params['atmvol']
            beta = params['beta']
            volvol = params['volvol']
            rho = params['rho']
            output_flag = params['output_flag']
            option = params['option']

        black_vol = self._alpha_sabr(
            F, K, T, beta, volvol, rho, self._find_alpha(
                F=F, T=T, atmvol=atmvol, beta=beta, volvol=volvol, rho=rho,))

        black_price = AnalyticalMethods.black_76(
            F=F, K=K, T=T, r=r, sigma=black_vol, option=option, refresh=True)

        output_dict = {
            'vol':black_vol,
            'price':black_price,
            'all':{
                'Price':black_price,
                'Vol':black_vol
                }
            }

        return output_dict.get(output_flag, "Please enter a valid output flag")

#        if output_flag == 'vol':
#            return black_vol

#        elif output_flag == 'price':
#            return black_price

#        elif output_flag == 'all':
#            return {'Price':black_price,
#                    'Vol':black_vol}


    @staticmethod
    def _alpha_sabr(F, K, T, beta, volvol, rho, alpha):
        """
        The SABR skew vol function

        Parameters
        ----------
        Alpha : Float
            Alpha value.

        Returns
        -------
        result : Float
            Black-76 equivalent SABR volatility.

        """

        dSABR = np.zeros(4)
        dSABR[1] = (
            alpha
            / ((F * K) ** ((1 - beta) / 2)
               * (1
                  + (((1 - beta) ** 2) / 24)
                  * (np.log(F / K) ** 2)
                  + ((1 - beta) ** 4 / 1920)
                  * (np.log(F / K) ** 4))))

        if abs(F - K) > 10 ** -8:
            sabrz = (volvol / alpha) * (F * K) ** (
                (1 - beta) / 2) * np.log(F / K)
            y = (np.sqrt(1 - 2 * rho * sabrz + (
                sabrz ** 2)) + sabrz - rho) / (1 - rho)
            if abs(y - 1) < 10 ** -8:
                dSABR[2] = 1
            elif y > 0:
                dSABR[2] = sabrz / np.log(y)
            else:
                dSABR[2] = 1
        else:
            dSABR[2] = 1

        dSABR[3] = (1 + ((((1 - beta) ** 2 / 24) * alpha ** 2 / (
            (F * K) ** (1 - beta))) + (
                0.25 * rho * beta * volvol * alpha) / (
                    (F * K) ** ((1 - beta) / 2)) + (
                        2 - 3 * rho ** 2) * volvol ** 2 / 24) * T)

        result = dSABR[1] * dSABR[2] * dSABR[3]

        return result


    @classmethod
    def _find_alpha(cls, F, T, atmvol, beta, volvol, rho):
        """
        Find alpha feeding values to _cube_root method.

        Returns
        -------
        result : Float
            Smallest positive root.

        """
        # Alpha is a function of atm vol etc

        alpha = cls._cube_root(
            ((1 - beta) ** 2 * T / (24 * F ** (2 - 2 * beta))),
            (0.25 * rho * volvol * beta * T / (F ** (1 - beta))),
            (1 + (2 - 3 * rho ** 2) / 24 * volvol ** 2 * T),
            (-atmvol * F ** (1 - beta)))

        return alpha


    @classmethod
    def _cube_root(cls, cubic, quadratic, linear, constant):
        """
        Finds the smallest positive root of the input cubic polynomial
        algorithm from Numerical Recipes

        Parameters
        ----------
        cubic : Float
            3rd order term of input polynomial.
        quadratic : Float
            2nd order term of input polynomial.
        linear : Float
            Linear term of input polynomial.
        constant : Float
            Constant term of input polynomial.

        Returns
        -------
        result : Float
            Smallest positive root.

        """
        a = quadratic / cubic
        b = linear / cubic
        C = constant / cubic
        Q = (a ** 2 - 3 * b) / 9
        r = (2 * a ** 3 - 9 * a * b + 27 * C) / 54
        roots = np.zeros(4)

        if r ** 2 - Q ** 3 >= 0:
            cap_A = -np.sign(r) * (abs(r) + np.sqrt(
                r ** 2 - Q ** 3)) ** (1 / 3)
            if cap_A == 0:
                cap_B = 0
            else:
                cap_B = Q / cap_A
            result = cap_A + cap_B - a / 3
        else:
            theta = cls._arccos(r / Q ** 1.5)

            # The three roots
            roots[1] = - 2 * np.sqrt(Q) * math.cos(
                theta / 3) - a / 3
            roots[2] = - 2 * np.sqrt(Q) * math.cos(
                theta / 3 + 2.0943951023932) - a / 3
            roots[3] = - 2 * np.sqrt(Q) * math.cos(
                theta / 3 - 2.0943951023932) - a / 3

            # locate that one which is the smallest positive root
            # assumes there is such a root (true for SABR model)
            # there is always a small positive root

            if roots[1] > 0:
                result = roots[1]
            elif roots[2] > 0:
                result = roots[2]
            elif roots[3] > 0:
                result = roots[3]

            if roots[2] > 0 and roots[2] < result:
                result = roots[2]

            if roots[3] > 0 and roots[3] < result:
                result = roots[3]

        return result


    @staticmethod
    def _arccos(y):
        """
        Inverse Cosine method

        Parameters
        ----------
        y : Float
            Input value.

        Returns
        -------
        result : Float
            Arc Cosine of input value.

        """
        result = np.arctan(-y / np.sqrt(-y * y + 1)) + 2 * np.arctan(1)

        return result
