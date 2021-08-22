"""
Lattice based option pricing models

"""
import numpy as np
from scipy.special import comb
from optionmodels.utils import Utils
# pylint: disable=invalid-name

class LatticeMethods():
    """
    Lattice based option pricing models

    """
    @staticmethod
    def european_binomial(**kwargs):
        """
        European Binomial Option price.
        Combinatorial function limit c1000

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
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.

        Returns
        -------
        Float
            European Binomial Option Price.

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
            option = params['option']

        b = r - q
        dt = T / steps
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        p = (np.exp(b * dt) - d) / (u - d)
        a = int(np.log(K / (S * (d ** steps))) / np.log(u / d)) + 1

        val = 0

        if option == 'call':
            for j in range(a, steps + 1):
                val = (
                    val + (comb(steps, j) * (p ** j)
                           * ((1 - p) ** (steps - j))
                           * ((S * (u ** j) * (d ** (steps - j))) - K)))
        if option == 'put':
            for j in range(0, a):
                val = (
                    val + (comb(steps, j) * (p ** j)
                           * ((1 - p) ** (steps - j))
                           * (K - ((S * (u ** j)) * (d ** (steps - j))))))

        return np.exp(-r * T) * val


    @staticmethod
    def cox_ross_rubinstein_binomial(**kwargs):
        """
        Cox-Ross-Rubinstein Binomial model

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
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.
        output_flag : Str
            Whether to return 'price', 'delta', 'gamma', 'theta' or
            'all'. The default is 'price'.
        american : Bool
            Whether the option is American. The default is False.

        Returns
        -------
        result : Various
            Depending on output flag:
                'price' : Float; Option Price
                'delta' : Float; Option Delta
                'gamma' : Float; Option Gamma
                'theta' : Float; Option Theta
                'all' : Tuple; Option Price, Option Delta, Option
                        Gamma, Option Theta

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
            option = params['option']
            output_flag = params['output_flag']
            american = params['american']

        if option == 'call':
            z = 1
        else:
            z = -1

        b = r - q
        dt = T / steps
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        p = (np.exp(b * dt) - d) / (u - d)
        df = np.exp(-r * dt)
        optionvalue = np.zeros((steps + 2))
        returnvalue = np.zeros((4))

        for i in range(steps + 1):
            optionvalue[i] = max(
                0, z * (S * (u ** i) * (d ** (steps - i)) - K))


        for j in range(steps - 1, -1, -1):
            for i in range(j + 1):
                if american:
                    optionvalue[i] = (
                        (p * optionvalue[i + 1])
                        + ((1 - p) * optionvalue[i])) * df
                else:
                    optionvalue[i] = max(
                        (z * (S * (u ** i) * (d ** (j - i)) - K)),
                        ((p * optionvalue[i + 1])
                         + ((1 - p) * optionvalue[i])) * df)

            if j == 2:
                returnvalue[2] = (((optionvalue[2] - optionvalue[1])
                                   / (S * (u ** 2) - S)
                                   - (optionvalue[1] - optionvalue[0])
                                   / (S - S * (d ** 2)))
                                  / (0.5 * (S * (u ** 2) - S * (d ** 2))))

                returnvalue[3] = optionvalue[1]

            if j == 1:
                returnvalue[1] = ((
                    optionvalue[1] - optionvalue[0]) / (S * u - S * d))

        returnvalue[3] = (returnvalue[3] - optionvalue[0]) / (2 * dt) / 365
        returnvalue[0] = optionvalue[0]

        if output_flag == 'price':
            result = returnvalue[0]
        if output_flag == 'delta':
            result = returnvalue[1]
        if output_flag == 'gamma':
            result = returnvalue[2]
        if output_flag == 'theta':
            result = returnvalue[3]
        if output_flag == 'all':
            result = {'Price':returnvalue[0],
                      'Delta':returnvalue[1],
                      'Gamma':returnvalue[2],
                      'Theta':returnvalue[3]}

        return result


    @staticmethod
    def leisen_reimer_binomial(**kwargs):
        """
        Leisen Reimer Binomial

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
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.
        output_flag : Str
            Whether to return 'price', 'delta', 'gamma' or 'all'. The
            default is 'price'.
        american : Bool
            Whether the option is American. The default is False.

        Returns
        -------
        result : Various
            Depending on output flag:
                'price' : Float; Option Price
                'delta' : Float; Option Delta
                'gamma' : Float; Option Gamma
                'all' : Tuple; Option Price, Option Delta, Option Gamma

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
            option = params['option']
            output_flag = params['output_flag']
            american = params['american']

        if option == 'call':
            z = 1
        else:
            z = -1

        b = r - q
        d1 = ((np.log(S / K) + (b + (0.5 * sigma ** 2)) * T)
              / (sigma * np.sqrt(T)))
        d2 = ((np.log(S / K) + (b - (0.5 * sigma ** 2)) * T)
              / (sigma * np.sqrt(T)))
        hd1 = (
            0.5 + np.sign(d1) * (0.25 - 0.25 * np.exp(
                -(d1 / (steps + 1 / 3 + 0.1 / (steps + 1))) ** 2
                * (steps + 1 / 6))) ** (0.5))
        hd2 = (
            0.5 + np.sign(d2) * (0.25 - 0.25 * np.exp(
                -(d2 / (steps + 1 / 3 + 0.1 / (steps + 1))) ** 2
                * (steps + 1 / 6))) ** (0.5))

        dt = T / steps
        p = hd2
        u = np.exp(b * dt) * hd1 / hd2
        d = (np.exp(b * dt) - p * u) / (1 - p)
        df = np.exp(-r * dt)

        optionvalue = np.zeros((steps + 1))
        returnvalue = np.zeros((4))

        for i in range(steps + 1):
            optionvalue[i] = max(0, z * (S * (u ** i) * (
                d ** (steps - i)) - K))

        for j in range(steps - 1, -1, -1):
            for i in range(j + 1):
                if american:
                    optionvalue[i] = (
                        (p * optionvalue[i + 1])
                        + ((1 - p) * optionvalue[i])) * df
                else:
                    optionvalue[i] = max(
                        (z * (S * (u ** i) * (d ** (j - i)) - K)),
                        ((p * optionvalue[i + 1])
                         + ((1 - p) * optionvalue[i])) * df)

            if j == 2:
                returnvalue[2] = (
                    ((optionvalue[2] - optionvalue[1])
                     / (S * (u ** 2) - S * u * d)
                     - (optionvalue[1] - optionvalue[0])
                     / (S * u * d - S * (d ** 2)))
                    / (0.5 * (S * (u ** 2) - S * (d ** 2))))

                returnvalue[3] = optionvalue[1]

            if j == 1:
                returnvalue[1] = ((optionvalue[1] - optionvalue[0])
                                  / (S * u - S * d))

        returnvalue[0] = optionvalue[0]

        if output_flag == 'price':
            result = returnvalue[0]
        if output_flag == 'delta':
            result = returnvalue[1]
        if output_flag == 'gamma':
            result = returnvalue[2]
        if output_flag == 'all':
            result = {'Price':returnvalue[0],
                      'Delta':returnvalue[1],
                      'Gamma':returnvalue[2]}

        return result


    @staticmethod
    def trinomial_tree(**kwargs):
        """
        Trinomial Tree

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
        option : Str
            Type of option, 'put' or 'call'. The default is 'call'.
        output_flag : Str
            Whether to return 'price', 'delta', 'gamma', 'theta' or
            'all'. The default is 'price'.
        american : Bool
            Whether the option is American. The default is False.

        Returns
        -------
        result : Various
            Depending on output flag:
                'price' : Float; Option Price
                'delta' : Float; Option Delta
                'gamma' : Float; Option Gamma
                'theta' : Float; Option Theta
                'all' : Tuple; Option Price, Option Delta, Option Gamma,
                        Option Theta

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
            option = params['option']
            output_flag = params['output_flag']
            american = params['american']

        if option == 'call':
            z = 1
        else:
            z = -1

        b = r - q
        dt = T / steps
        u = np.exp(sigma * np.sqrt(2 * dt))
        d = np.exp(-sigma * np.sqrt(2 * dt))
        pu = ((np.exp(b * dt / 2) - np.exp(-sigma * np.sqrt(dt / 2)))
              / (np.exp(sigma * np.sqrt(dt / 2))
                 - np.exp(-sigma * np.sqrt(dt / 2)))) ** 2
        pd = ((np.exp(sigma * np.sqrt(dt / 2)) - np.exp(b * dt / 2))
              / (np.exp(sigma * np.sqrt(dt / 2))
                 - np.exp(-sigma * np.sqrt(dt / 2)))) ** 2
        pm = 1 - pu - pd
        df = np.exp(-r * dt)
        optionvalue = np.zeros((steps * 2 + 2))
        returnvalue = np.zeros((4))

        for i in range(2 * steps + 1):
            optionvalue[i] = max(
                0, z * (S * (u ** max(i - steps, 0))
                        * (d ** (max((steps - i), 0))) - K))


        for j in range(steps - 1, -1, -1):
            for i in range(j * 2 + 1):

                optionvalue[i] = (pu * optionvalue[i + 2]
                                  + pm * optionvalue[i + 1]
                                  + pd * optionvalue[i]) * df

                if american:
                    optionvalue[i] = max(
                        z * (S * (u ** max(i - j, 0))
                             * (d ** (max((j - i), 0))) - K), optionvalue[i])

            if j == 1:
                returnvalue[1] = (
                    (optionvalue[2] - optionvalue[0]) / (S * u - S * d))

                returnvalue[2] = (
                    ((optionvalue[2] - optionvalue[1]) / (S * u - S)
                     - (optionvalue[1] - optionvalue[0]) / (S - S * d ))
                    / (0.5 * ((S * u) - (S * d))))

                returnvalue[3] = optionvalue[0]

        returnvalue[3] = (returnvalue[3] - optionvalue[0]) / dt / 365

        returnvalue[0] = optionvalue[0]

        if output_flag == 'price':
            result = returnvalue[0]
        if output_flag == 'delta':
            result = returnvalue[1]
        if output_flag == 'gamma':
            result = returnvalue[2]
        if output_flag == 'theta':
            result = returnvalue[3]
        if output_flag == 'all':
            result = {'Price':returnvalue[0],
                      'Delta':returnvalue[1],
                      'Gamma':returnvalue[2],
                      'Theta':returnvalue[3]}

        return result


    @classmethod
    def implied_trinomial_tree(cls, **kwargs):
        """
        Implied Trinomial Tree

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
        steps_itt : Int
            Number of time steps. The default is 10.
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.
        output_flag : Str
            UPM: A matrix of implied up transition probabilities
            UPni: The implied up transition probability at a single
                  node
            DPM: A matrix of implied down transition probabilities
            DPni: The implied down transition probability at a single
                  node
            LVM: A matrix of implied local volatilities
            LVni: The local volatility at a single node
            ADM: A matrix of Arrow-Debreu prices at a single node
            ADni: The Arrow-Debreu price at a single node (at
                  time step - 'step' and state - 'state')
            price: The value of the European option
        step : Int
            Time step used for Arrow Debreu price at single node. The
            default is 5.
        state : Int
            State position used for Arrow Debreu price at single node.
            The default is 5.
        skew : Float
            Rate at which volatility increases (decreases) for every
            one point decrease
            (increase) in the strike price. The default is 0.0004.

        Returns
        -------
        result : Various
            Depending on output flag:
                UPM: A matrix of implied up transition probabilities
                UPni: The implied up transition probability at a single
                      node
                DPM: A matrix of implied down transition probabilities
                DPni: The implied down transition probability at a
                      single node
                LVM: A matrix of implied local volatilities
                LVni: The local volatility at a single node
                ADM: A matrix of Arrow-Debreu prices at a single node
                ADni: The Arrow-Debreu price at a single node (at
                      time step - 'step' and state - 'state')
                price: The European option price.

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
            option = params['option']
            output_flag = params['output_flag']
            step = params['step']
            state = params['state']
            skew = params['skew']

        if option == 'call':
            z = 1
        else:
            z = -1

        optionvaluenode = np.zeros((steps_itt * 2 + 1))
        # Arrow Debreu prices
        ad = np.zeros((steps_itt + 1, steps_itt * 2 + 1), dtype='float')
        pu = np.zeros((steps_itt, steps_itt * 2 - 1), dtype='float')
        pd = np.zeros((steps_itt, steps_itt * 2 - 1), dtype='float')
        localvol = np.zeros((steps_itt, steps_itt * 2 - 1), dtype='float')

        dt = T / steps_itt
        u = np.exp(sigma * np.sqrt(2 * dt))
        d = 1 / u
        df = np.exp(-r * dt)
        ad[0, 0] = 1

        for n in range(steps_itt):
            for i in range(n * 2 + 1):
                val = 0
                Si1 = (S * (u ** (max(i - n, 0)))
                       * (d ** (max(n * 2 - n - i, 0))))
                Si = Si1 * d
                Si2 = Si1 * u
                b = r - q
                Fi = Si1 * np.exp(b * dt)
                sigmai = sigma + (S - Si1) * skew

                if i < (n * 2) / 2 + 1:
                    for j in range(i):
                        Fj = (S * (u ** (max(j - n, 0)))
                              * (d ** (max(n * 2 - n - j, 0)))
                              * np.exp(b * dt))

                        val = val + ad[n, j] * (Si1 - Fj)

                    optionvalue = cls.trinomial_tree(
                        S=S, K=Si1, T=(n + 1) * dt, r=r, q=q, sigma=sigmai,
                        steps=(n + 1), option='put', output_flag='price',
                        american=False, refresh=True)

                    qi = ((np.exp(r * dt) * optionvalue - val)
                          / (ad[n, i] * (Si1 - Si)))

                    pi = (Fi + qi * (Si1 - Si) - Si1) / (Si2 - Si1)

                else:
                    optionvalue = cls.trinomial_tree(
                        S=S, K=Si1, T=(n + 1) * dt, r=r, q=q, sigma=sigmai,
                        steps=(n + 1), option='call', output_flag='price',
                        american=False, refresh=True)

                    val = 0
                    for j in range(i + 1, n * 2 + 1):
                        Fj = (S * (u ** (max(j - n, 0)))
                              * (d ** (max(n * 2 - n - j, 0)))
                              * np.exp(b * dt))

                        val = val + ad[n, j] * (Fj- Si1)

                    pi = ((np.exp(r * dt) * optionvalue - val)
                          / (ad[n, i] * (Si2 - Si1)))

                    qi = (Fi - pi * (Si2 - Si1) - Si1) / (Si - Si1)

                # Replacing negative probabilities
                if pi < 0 or pi > 1 or qi < 0 or qi > 1:
                    if Si2 > Fi > Si1:
                        pi = (1 / 2 * ((Fi - Si1) / (Si2 - Si1)
                                       + (Fi - Si) / (Si2 - Si)))

                        qi = 1 / 2 * ((Si2 - Fi) / (Si2 - Si))

                    elif Si1 > Fi > Si:
                        pi = 1 / 2 * ((Fi - Si) / (Si2 - Si))

                        qi = (1 / 2 * ((Si2 - Fi) / (Si2 - Si1)
                                       + (Si1 - Fi) / (Si1 - Si)))

                pd[n, i] = qi
                pu[n, i] = pi

                # Calculating local volatilities
                Fo = (pi * Si2 + qi * Si + (1 - pi -qi) * Si1)
                localvol[n, i] = np.sqrt(
                    (pi * (Si2 - Fo) ** 2
                     + (1 - pi - qi) * (Si1 - Fo) ** 2
                     + qi * (Si - Fo) ** 2) / (Fo ** 2 * dt))

                # Calculating Arrow-Debreu prices
                if n == 0:
                    ad[n + 1, i] = qi * ad[n, i] * df
                    ad[n + 1, i + 1] = (1 - pi - qi) * ad[n, i] * df
                    ad[n + 1, i + 2] = pi * ad[n, i] * df

                elif n > 0 and i == 0:
                    ad[n + 1, i] = qi * ad[n, i] * df

                elif n > 0 and i == n * 2:
                    ad[n + 1, i] = (
                        pu[n, i - 2] * ad[n, i - 2] * df
                        + (1 - pu[n, i - 1] - pd[n, i - 1])
                        * (ad[n, i - 1]) * df + qi * (ad[n, i] * df))
                    ad[n + 1, i + 1] = (
                        pu[n, i - 1] * (ad[n, i - 1]) * df
                        + (1 - pi - qi) * (ad[n, i] * df))
                    ad[n + 1, i + 2] = pi * ad[n, i] * df

                elif n > 0 and i == 1:
                    ad[n + 1, i] = (
                        (1 - pu[n, i - 1] - (pd[n, i - 1]))
                        * ad[n, i - 1] * df + (qi * ad[n, i] * df))

                else:
                    ad[n + 1, i] = (
                        pu[n, i - 2] * (ad[n, i - 2]) * df
                        + (1 - pu[n, i - 1] - pd[n, i - 1])
                        * (ad[n, i - 1]) * df + qi * (ad[n, i]) * df)

        # Calculation of option price using the implied trinomial tree
        for i in range(2 * steps_itt + 1):
            optionvaluenode[i] = max(
                0, z * (S * (u ** max(i - steps_itt, 0))
                        * (d ** (max((steps_itt - i), 0))) - K))

        for n in range(steps_itt - 1, -1, -1):
            for i in range(n * 2 + 1):
                optionvaluenode[i] = (
                    (pu[n, i] * optionvaluenode[i + 2]
                     + (1 - pu[n, i] - pd[n, i])
                     * (optionvaluenode[i + 1])
                     + pd[n, i] * (optionvaluenode[i])) * df)


        price = optionvaluenode[0]

        output_dict = {
            'UPM':pu,
            'UPni':pu[step, state],
            'DPM':pd,
            'DPni':pd[step, state],
            'LVM':localvol,
            'LVni':localvol[step, state],
            'ADM':ad,
            'ADni':ad[step, state],
            'price':price
            }

        return output_dict.get(
            output_flag, "Please select a valid output flag")
