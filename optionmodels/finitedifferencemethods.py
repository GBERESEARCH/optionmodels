"""
Finite Difference option pricing models

"""
import numpy as np
from optionmodels.utils import Utils
# pylint: disable=invalid-name

class FiniteDifference():
    """
    Finite Difference option pricing models

    """
    @staticmethod
    def explicit_finite_difference(**kwargs):
        """
        Explicit Finite Difference

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
        nodes : Int
            Number of price steps. The default is 100.
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.
        american : Bool
            Whether the option is American. The default is False.
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
            nodes = params['nodes']
            option = params['option']
            american = params['american']

        if option == 'call':
            z = 1
        else:
            z = -1

        b = r - q
        dS = S / nodes
        nodes = int(K / dS) * 2
        St = np.zeros((nodes + 2), dtype='float')

        SGridtPt = int(S / dS)
        dt = (dS ** 2) / ((sigma ** 2) * 4 * (K ** 2))
        N = int(T / dt) + 1

        C = np.zeros((N + 1, nodes + 2), dtype='float')
        dt = T / N
        Df = 1 / (1 + r * dt)

        for i in range(nodes + 1):
            St[i] = i * dS # Asset price at maturity
            C[N, i] = max(0, z * (St[i] - K) ) # At maturity

        for j in range(N - 1, -1, -1):
            for i in range(1, nodes):
                pu = 0.5 * ((sigma ** 2) * (i ** 2) + b * i) * dt
                pm = 1 - (sigma ** 2) * (i ** 2) * dt
                pd = 0.5 * ((sigma ** 2) * (i ** 2) - b * i) * dt
                C[j, i] = Df * (pu * C[j + 1, i + 1] + pm * C[
                    j + 1, i] + pd * C[j + 1, i - 1])
                if american:
                    C[j, i] = max(z * (St[i] - K), C[j, i])

                if z == 1: # Call option
                    C[j, 0] = 0
                    C[j, nodes] = (St[i] - K)
                else:
                    C[j, 0] = K
                    C[j, nodes] = 0

        result = C[0, SGridtPt]

        return result


    @staticmethod
    def implicit_finite_difference(**kwargs):
        """
        Implicit Finite Difference
        # Slow to converge - steps has small effect, need nodes 3000+

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
        steps : Int
            Number of time steps. The default is 1000.
        nodes : Float
            Number of price steps. The default is 100.
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.
        american : Bool
            Whether the option is American. The default is False.
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
            steps = params['steps']
            nodes = params['nodes']
            option = params['option']
            american = params['american']

        if option == 'call':
            z = 1
        else:
            z = -1

        # Make sure current asset price falls at grid point
        dS = 2 * S / nodes
        SGridtPt = int(S / dS)
        nodes = int(K / dS) * 2
        dt = T / steps
        b = r - q

        CT = np.zeros(nodes + 1)
        p = np.zeros((nodes + 1, nodes + 1), dtype='float')

        for j in range(nodes + 1):
            CT[j] = max(0, z * (j * dS - K)) # At maturity
            for i in range(nodes + 1):
                p[j, i] = 0

        p[0, 0] = 1
        for i in range(1, nodes):
            p[i, i - 1] = 0.5 * i * (b - (sigma ** 2) * i) * dt
            p[i, i] = 1 + (r + (sigma ** 2) * (i ** 2)) * dt
            p[i, i + 1] = 0.5 * i * (-b - (sigma ** 2) * i) * dt

        p[nodes, nodes] = 1

        C = np.matmul(np.linalg.inv(p), CT.T)

        for j in range(steps - 1, 0, -1):
            C = np.matmul(np.linalg.inv(p), C)

            if american:
                for i in range(1, nodes + 1):
                    C[i] = max(float(C[i]), z * (
                        (i - 1) * dS - K))

        result = C[SGridtPt + 1]

        return result


    @staticmethod
    def explicit_finite_difference_lns(**kwargs):
        """
        Explicit Finite Differences - rewrite BS-PDE in terms of ln(S)

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
        steps : Int
            Number of time steps. The default is 1000.
        nodes : Float
            Number of price steps. The default is 100.
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.
        american : Bool
            Whether the option is American. The default is False.
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
            steps_itt = params['steps_itt']
            nodes = params['nodes']
            option = params['option']
            american = params['american']

        if option == 'call':
            z = 1
        else:
            z = -1

        b = r - q
        dt = T / steps_itt
        dx = sigma * np.sqrt(3 * dt)
        pu = 0.5 * dt * (((sigma / dx) ** 2) + (b - (sigma ** 2) / 2) / dx)
        pm = 1 - dt * ((sigma / dx) ** 2) - r * dt
        pd = 0.5 * dt * (((sigma / dx) ** 2) - (b - (sigma ** 2) / 2) / dx)
        St = np.zeros(nodes + 2)
        St[0] = S * np.exp(-nodes / 2 * dx)
        C = np.zeros((int(nodes / 2) + 1, nodes + 2), dtype='float')
        C[steps_itt, 0] = max(0, z * (St[0] - K))

        for i in range(1, nodes + 1):
            St[i] = St[i - 1] * np.exp(dx) # Asset price at maturity
            C[steps_itt, i] = max(0, z * (St[i] - K) ) # At maturity

        for j in range(steps_itt - 1, -1, -1):
            for i in range(1, nodes):
                C[j, i] = pu * C[j + 1, i + 1] + pm * C[j + 1, i] + (
                    pd * C[j + 1, i - 1])
                if american:
                    C[j, i] = max(C[j, i], z * (St[i] - K))

                # Upper boundary
                C[j, nodes] = C[j, nodes - 1] + (St[nodes] - St[nodes - 1])

                # Lower boundary
                C[j, 0] = C[j, 1]

        result = C[0, int(nodes / 2)]

        return result


    @staticmethod
    def crank_nicolson(**kwargs):
        """
        Crank Nicolson

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
        steps : Int
            Number of time steps. The default is 1000.
        nodes : Float
            Number of price steps. The default is 100.
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.
        american : Bool
            Whether the option is American. The default is False.
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
            steps = params['steps']
            nodes = params['nodes']
            option = params['option']
            american = params['american']

        if option == 'call':
            z = 1
        else:
            z = -1

        b = r - q
        dt = T / steps
        dx = sigma * np.sqrt(3 * dt)
        pu = -0.25 * dt * (((sigma / dx) ** 2) + (b - (sigma ** 2) / 2) / dx)
        pm = 1 + 0.5 * dt * ((sigma / dx) ** 2) + 0.5 * r * dt
        pd = -0.25 * dt * (((sigma / dx) ** 2) - (b - (sigma ** 2) / 2) / dx)
        St = np.zeros(nodes + 2)
        pmd = np.zeros(nodes + 1)
        p = np.zeros(nodes + 1)
        St[0] = S * np.exp(-nodes / 2 * dx)
        C = np.zeros((int(nodes / 2) + 2, nodes + 2), dtype='float')
        C[0, 0] = max(0, z * (St[0] - K))

        for node in range(1, nodes + 1):
            St[node] = St[node - 1] * np.exp(dx) # Asset price at maturity
            C[0, node] = max(0, z * (St[node] - K)) # At maturity

        pmd[1] = pm + pd
        p[1] = (-pu * C[0, 2]
                - (pm - 2) * C[0, 1]
                - pd * C[0, 0]
                - pd * (St[1] - St[0]))

        step = steps - 1
        while step > -1:
            for outer_node in range(2, nodes):
                p[outer_node] = (-pu * C[0, outer_node + 1]
                        - (pm - 2) * C[0, outer_node]
                        - pd * C[0, outer_node - 1]
                        - p[outer_node - 1] * pd / pmd[outer_node - 1])
                pmd[outer_node] = pm - pu * pd / pmd[outer_node - 1]

            for outer_node in range(nodes - 2, 0, -1):
                C[1, outer_node] = (
                    (p[outer_node] - pu * C[1, outer_node + 1])
                    / pmd[outer_node])

                for inner_node in range(nodes + 1):
                    if american:
                        C[0, inner_node] = max(
                            C[1, inner_node], z * (St[inner_node] - K))
                    else:
                        C[0, inner_node] = C[1, inner_node]
            step -= 1

        result = C[0, int(nodes / 2)]

        return result
