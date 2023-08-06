# Copyright 2020 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import numpy as np
import numbers

from getml.helpers.validation import _check_parameter_bounds

def _validate_hyperopt_parameters(parameters):
    """Checks both the types and values of the `parameters` and raises an
    exception is something is off.

    Examples:

        .. code-block:: python

            getml.helpers.validation.validate_Hyperopt_parameters(
                {'n_iter': 10, 'score': 'auc'})

    Args:
        parameters (dict): Dictionary containing some of all
            parameters supported in
            :class:`~getml.predictors.RandomSearch`,
            :class:`~getml.predictors.GaussianHyperparameterSearch`, and
            :class:`~getml.predictors.LatinHypercubeSearch`.

    Raises:
        KeyError: If an unsupported parameter is encountered.
        TypeError: If any parameter is of wrong type.
        ValueError: If any parameter does not match its possible
            choices (string) or is out of the expected bounds
            (numerical).

    Note:

        In addition to checking the types and values of the
        `parameters`, the function also accesses whether:

            - `seed` is only used in a single-threaded context
            - `param_space` is both valid and consistent
            - `session_name` is set
            - `n_iter` matches the requirements of the algorithm
            - `score` is compatible with the loss function provided 
                in `model`

    """

    # The provided parameters are allowed to be a subset of all
    # possible parameters. But no extra ones can be provided.
    allowed_parameters = {"model",
                          "model_type",
                          "param_space",
                          "session_name",
                          "seed",
                          "n_iter",
                          "ratio_iter", 
                          "optimization_algorithm",
                          "optimization_burn_in_algorithm",
                          "optimization_burn_ins",
                          "surrogate_burn_in_algorithm",
                          "gaussian_kernel",
                          "gaussian_optimization_algorithm",
                          "gaussian_optimization_burn_in_algorithm",
                          "gaussian_optimization_burn_ins",
                          "score"}

    # ----------------------------------------------------------------
    
    for kkey in parameters:
        
        if kkey not in allowed_parameters:
            raise KeyError("'unknown Hyperopt parameter: "+kkey)

        if kkey == 'model':
            if parameters['model'].type != "MultirelModel" and parameters['model'].type != "RelboostModel":
                raise TypeError("'model' must be of type getml.models.MultirelModel or getml.models.RelboostModel")
        
        if kkey == 'model_type':
            if parameters['model_type'] not in ['Multirel', 'Relboost']:
                raise TypeError("'model_type' must be of either 'Multirel' or 'Relboost'")

        if kkey == 'param_space':
            if type(parameters['param_space']) is not dict:
                raise TypeError("'param_space' must be a dict")
            
            if len(parameters['param_space']) == 0:
                raise ValueError("'param_space' must contain at least one key-value pair")
            
            for ddimension in parameters['param_space']:
                if len(parameters['param_space'][ddimension]) != 2:
                    raise ValueError("In key '"+ddimension+"' of 'param_space': provided value must be a numerical array of length 2")
                
                if not all([isinstance(bb, numbers.Real) for bb in parameters['param_space'][ddimension]]):
                    raise ValueError("In key '"+ddimension+"' of 'param_space': all values must be numerical")
                
                if parameters['param_space'][ddimension][0] > parameters['param_space'][ddimension][1]:
                    raise ValueError("In key '"+ddimension+"' of 'param_space': Lower bound exceeds upper one! Syntax 'key: [lower, upper]'")

        if kkey == 'session_name':
            if type(parameters['session_name']) is not str:
                raise TypeError("'session_name' must be a str")
            if not parameters['session_name']:
                raise ValueError("'session_name' must not be empty")

        if kkey == 'seed':
            if parameters['seed'] is not None and not isinstance(parameters['seed'], numbers.Real):
                raise TypeError("'seed' must be either None or a real number")
            
            if parameters['seed'] is not None:
                _check_parameter_bounds(parameters['seed'], 'seed',
                                        [0, np.iinfo(np.uint64).max])

        if kkey == 'ratio_iter':
            if not isinstance(parameters['ratio_iter'], numbers.Real):
                raise TypeError("'ratio_iter' must be a real number")
            _check_parameter_bounds(parameters['ratio_iter'], 'ratio_iter',
                                    [0.0, 1.0])

        if kkey == 'n_iter':
            if not isinstance(parameters['n_iter'], numbers.Real):
                raise TypeError("'n_iter' must be a real number")
            
            if parameters['ratio_iter'] == 1:
                _check_parameter_bounds(parameters['n_iter'], 'n_iter',
                                        [1, np.iinfo(np.int32).max])
            else:
                # In case of the Gaussian hyperparameter optimization,
                # we need some burn ins in order to fit the surrogate
                # (Gaussian process).
                _check_parameter_bounds(parameters['n_iter'], 'n_iter',
                                        [4, np.iinfo(np.int32).max])

        if kkey == 'optimization_algorithm':
            if type(parameters['optimization_algorithm']) is not str:
                raise TypeError("'optimization_algorithm' must be a str")
            if parameters['optimization_algorithm'] not in ['nelderMead', 'bfgs']:
                raise ValueError("'optimization_algorithm' must be either 'nelderMead' or  'bfgs'")

        if kkey == 'optimization_burn_in_algorithm':
            if type(parameters['optimization_burn_in_algorithm']) is not str:
                raise TypeError("'optimization_burn_in_algorithm' must be a str")
            if parameters['optimization_burn_in_algorithm'] not in ['latinHypercube', 'random']:
                raise ValueError("'optimization_burn_in_algorithm' must be either 'latinHypercube' or  'random'")

        if kkey == 'optimization_burn_ins':
            if not isinstance(parameters['optimization_burn_ins'], numbers.Real):
                raise TypeError("'optimization_burn_ins' must be a real number")
            _check_parameter_bounds(parameters['optimization_burn_ins'], 'optimization_burn_ins',
                                    [3, np.iinfo(np.int32).max])

        if kkey == 'surrogate_burn_in_algorithm':
            if type(parameters['surrogate_burn_in_algorithm']) is not str:
                raise TypeError("'surrogate_burn_in_algorithm' must be a str")
            if parameters['surrogate_burn_in_algorithm'] not in ['latinHypercube', 'random']:
                raise ValueError("'surrogate_burn_in_algorithm' must be either 'latinHypercube' or  'random'")

        if kkey == 'gaussian_kernel':
            if type(parameters['gaussian_kernel']) is not str:
                raise TypeError("'gaussian_kernel' must be a str")
            if parameters['gaussian_kernel'] not in ['matern32', 'matern52', 'exp', 'gauss']:
                raise ValueError("'gaussian_kernel' must be either 'matern32', 'matern52', 'exp' or  'gauss'")

        if kkey == 'gaussian_optimization_algorithm':
            if type(parameters['gaussian_optimization_algorithm']) is not str:
                raise TypeError("'gaussian_optimization_algorithm' must be a str")
            if parameters['gaussian_optimization_algorithm'] not in ['nelderMead', 'bfgs']:
                raise ValueError("'gaussian_optimization_algorithm' must be either 'nelderMead' or  'bfgs'")

        if kkey == 'gaussian_optimization_burn_in_algorithm':
            if type(parameters['gaussian_optimization_burn_in_algorithm']) is not str:
                raise TypeError("'gaussian_optimization_burn_in_algorithm' must be a str")
            if parameters['gaussian_optimization_burn_in_algorithm'] not in ['latinHypercube', 'random']:
                raise ValueError("'gaussian_optimization_burn_in_algorithm' must be either 'latinHypercube' or  'random'")

        if kkey == 'gaussian_optimization_burn_ins':
            if not isinstance(parameters['gaussian_optimization_burn_ins'], numbers.Real):
                raise TypeError("'gaussian_optimization_burn_ins' must be a real number")
            _check_parameter_bounds(parameters['gaussian_optimization_burn_ins'], 'gaussian_optimization_burn_ins',
                                    [3, np.iinfo(np.int32).max])

        if kkey == 'score':
            if type(parameters['score']) is not str:
                raise TypeError("'score' must be a str")
            if parameters['score'] not in ['auc', 'accuracy', 'cross_entropy', 'mae', 'rmse', 'rsquared']:
                raise ValueError("'score' must be either 'auc', 'accuracy', 'cross_entropy', 'mae', 'rmse', or 'rsquared'")
