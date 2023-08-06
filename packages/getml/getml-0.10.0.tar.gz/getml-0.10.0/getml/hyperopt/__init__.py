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
# AUTHORS OR COPYRIGHT :wHOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""Automatically find the best parameters for 

* :class:`~getml.models.MultirelModel`
* :class:`~getml.models.RelboostModel`
* :class:`~getml.predictors.LinearRegression`
* :class:`~getml.predictors.LogisticRegression`
* :class:`~getml.predictors.XGBoostClassifier`
* :class:`~getml.predictors.XGBoostRegressor`

The most relevant parameters of these classes can be chosen to
constitute individual dimensions of a parameter space. For each
parameter, a lower and upper bound has to be provided and the
hyperparameter optimization will search the space within these
bounds. This will be done iteratively by drawing a specific parameter
combination, overwriting the corresponding parameters in a base
model, and fitting and score it. The algorithm used to draw from the
parameter space is represented by the different classes of
:mod:`~getml.hyperopt`. While :class:`~getml.hyperopt.RandomSearch`
and :class:`~getml.hyperopt.LatinHypercubeSearch` are purely
statistical approaches,
:class:`~getml.hyperopt.GaussianHyperparameterSearch` will use prior
knowledge obtained from evaluations of previous parameter combinations
to select the next one.

Examples:

    In order to use the hyperparameter optimization, you first have to
    construct a base `model` (of type
    :class:`~getml.models.MultirelModel` or
    :class:`~getml.models.RelboostModel`), upload it to the getML
    engine, and provided it to the constructor of the search class.
    
    In this example we use the default hyperparameter space:

    .. code-block:: python

        population_table_training, peripheral_table = getml.datasets.make_numerical(
                    random_state = 132)
        population_table_validation, _ = getml.datasets.make_numerical(
                    random_state = 133)

        population_placeholder = population_table_training.to_placeholder()
        peripheral_placeholder = peripheral_table.to_placeholder()
        population_placeholder.join(peripheral_placeholder,
                                    join_key = "join_key",
                                    time_stamp = "time_stamp"
        )

        feature_selector = getml.predictors.LinearRegression()
        predictor = getml.predictors.XGBoostRegressor()

        model = getml.models.RelboostModel(
            population = population_placeholder,
            peripheral = peripheral_placeholder,
            feature_selector = feature_selector,
            predictor = predictor,
            name = "relboost"
        ).send()

        l = getml.hyperopt.LatinHypercubeSearch(model = model)

        l.fit(
            population_table_training = population_table_training,
            population_table_validation = population_table_validation,
            peripheral_tables = peripheral_table
        )

        l.get_scores()

    In this example we use a custom hyperparameter space:

    .. code-block:: python

        param_space = {
            'num_features': [80, 300],
            'reg_lambda': [0, 0.1],
            'predictor_reg_lambda': [0, 10]
        }

        l = getml.hyperopt.LatinHypercubeSearch(
            model = model,
            param_space = param_space,
            n_iter = 35,
        )

        l.fit(
            population_table_training = population_table_training,
            population_table_validation = population_table_validation,
            peripheral_tables = peripheral_table
        )

        l.get_models()
        l.get_scores()

    More about naming conventions and which parameters are supported
    in the hyperparameter optimization can be found in the
    documentation of the `param_space` input argument of the
    particular classes.

    A rough *rule of thumb* is that we need to iterate *at least* 10
    times the number of dimension of the parameter space we are
    searching in when performing the hyperparameter
    optimization. Especially when dealing with the
    :class:`~getml.hyperopt.GaussianHyperparameterSearch` having more
    iterations will very likely yield better results. 

    Note:

    There are two ways to exclude a particular parameter from the
    hyperparameter search. First, omitting it in the dictionary
    provided as the `param_space` input argument in the class
    constructor and, second, by assigning the same value for both
    its lower and upper bound. For all excluded parameters as well as
    those not covered by the hyperparameter optimization the
    corresponding values of the base model will be used in all
    iterations.

"""

from .hyperopt import *
from .list_hyperopts import *
from .load_hyperopt import (
    _decode_hyperopt,
    load_hyperopt
)

__all__ = (
    "_decode_hyperopt",
    "list_hyperopts",
    "load_hyperopt",
    "GaussianHyperparameterSearch",
    "LatinHypercubeSearch",
    "RandomSearch"
)
