"""
Utility functions for refreshing parameters and timing

"""

import copy
import time
from typing import Callable
from functools import wraps
from optionmodels.models_params import models_params_dict, sabr_params_dict


class Utils():
    """
    Utility functions for refreshing parameters and timing

    """
    @staticmethod
    def timer(func: Callable) -> Callable:
        """
        Add timing to a function

        Parameters
        ----------
        func : Function
            The function to be timed.

        Returns
        -------
        Function
            The function with runtime.

        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            function = func(*args, **kwargs)
            end = time.perf_counter()
            for key, value in kwargs.items():
                if key == 'timing' and bool(value):
                    print('{}.{} : {} milliseconds'.format(
                        func.__module__, func.__name__, round((
                            end - start)*1e3, 2)))
            return function
        return wrapper


    @staticmethod
    def init_params(inputs: dict) -> dict:
        """
        Initialise parameter dictionary
        Parameters
        ----------
        inputs : Dict
            Dictionary of parameters supplied to the function.
        Returns
        -------
        params : Dict
            Dictionary of parameters.
        """
        # Copy the default parameters
        params = copy.deepcopy(models_params_dict)

        # For all the supplied arguments
        for key, value in inputs.items():

            # Replace the default parameter with that provided
            params[key] = value

        return params


    @staticmethod
    def init_sabr_params(inputs: dict) -> dict:
        """
        Initialise parameter dictionary
        Parameters
        ----------
        inputs : Dict
            Dictionary of parameters supplied to the function.
        Returns
        -------
        params : Dict
            Dictionary of parameters.
        """
        # Copy the default parameters
        params = copy.deepcopy(sabr_params_dict)

        # For all the supplied arguments
        for key, value in inputs.items():

            # Replace the default parameter with that provided
            params[key] = value

        return params
