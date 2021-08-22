"""
Dictionary of key models parameters

"""

models_params_dict = {
    'S':100,
    'F':100,
    'K':100,
    'T':0.25,
    'r':0.005,
    'q':0,
    'sigma':0.2,
    'option':'call',
    'steps':1000,
    'steps_itt':10,
    'nodes':100,
    'vvol':0.5,
    'simulations':10000,
    'output_flag':'price',
    'american':False,
    'step':5,
    'state':5,
    'skew':0.0004,
    'sig0':0.09,
    'sigLR':0.0625,
    'halflife':0.1,
    'rho':0,
    'cm':5.0,
    'epsilon':0.0001,
    'refresh':True,
    'timing':False,
    'option_method':'bsm',
    'vol_method':'nr',

    'pricer_dict':{
        'bsm':('AnalyticalMethods', 'black_scholes_merton'),
        'bsm_vega':('AnalyticalMethods', 'black_scholes_merton_vega'),
        'black76':('AnalyticalMethods', 'black_76'),
        'euro_bin':('LatticeMethods', 'european_binomial'),
        'crr_bin':('LatticeMethods', 'cox_ross_rubinstein_binomial'),
        'lr_bin':('LatticeMethods', 'leisen_reimer_binomial'),
        'tt':('LatticeMethods', 'trinomial_tree'),
        'itt':('LatticeMethods', 'implied_trinomial_tree'),
        'efd':('FiniteDifference', 'explicit_finite_difference'),
        'ifd':('FiniteDifference', 'implicit_finite_difference'),
        'efd_lns':('FiniteDifference', 'explicit_finite_difference_lns'),
        'cn':('FiniteDifference', 'crank_nicolson'),
        'emc':('MonteCarlo', 'european_monte_carlo'),
        'emc_greeks':('MonteCarlo', 'european_monte_carlo_with_greeks'),
        'hw87':('HullWhite', 'hull_white_87'),
        'hw88':('HullWhite', 'hull_white_88')
        },

    # Dictionary of lattice based option models
    'lattice_dict':{
        'euro_bin':'european_binomial',
        'crr_bin':'cox_ross_rubinstein_binomial',
        'lr_bin':'leisen_reimer_binomial',
        'tt':'trinomial_tree',
        'itt':'implied_trinomial_tree'
        },

    # Dictionary of finite difference based option models
    'finite_difference_dict':{
        'efd':'explicit_finite_difference',
        'ifd':'implicit_finite_difference',
        'efd_lns':'explicit_finite_difference_lns',
        'cn':'crank_nicolson'
        },

    # Dictionary of montecarlo based option models
    'montecarlo_dict':{
        'emc':'european_monte_carlo',
        'emc_greeks':'european_monte_carlo_with_greeks'
        },

    # Dictionary of Hull-White based option models
    'hullwhite_dict':{
        'hw87':'hull_white_87',
        'hw88':'hull_white_88'
        },

    # Dictionary of interpolation methods used in implied vol calculation
    'implied_vol_method_dict':{
        'nr':'implied_vol_newton_raphson',
        'bisection':'implied_vol_bisection',
        'naive':'implied_vol_naive',
        'naive_verbose':'implied_vol_naive_verbose'
        },

    'params_list':[
        'S',
        'F',
        'K',
        'T',
        'r',
        'q',
        'sigma',
        'option',
        'steps',
        'steps_itt',
        'nodes',
        'vvol',
        'simulations',
        'output_flag',
        'american',
        'step',
        'state',
        'skew',
        'sig0',
        'sigLR',
        'halflife',
        'rho',
        'cm',
        'epsilon',
        'timing',
        'refresh',
        'option_method',
        'vol_method'
        ]
    }

sabr_params_dict = {
    'F':100,
    'K':70,
    'T':0.5,
    'r':0.05,
    'atmvol':0.3,
    'beta':0.9999,
    'volvol':0.5,
    'rho':-0.4,
    'option':'put',
    'timing':False,
    'output_flag':'price'
    }
