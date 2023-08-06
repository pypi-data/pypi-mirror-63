
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

"""Contains handlers for all steps involved in a data science project after
data preparation:

* automated feature engineering
* automated feature selection
* training and evaluation of machine learning (ML) algorithms
* deployment of the fitted models

Both the :class:`~getml.models.MultirelModel` and
:class:`~getml.models.RelboostModel` are handlers for models in the
getML engine. The main difference between the two is that they use
different algorithms for the automated feature engineering (for more
details check out :ref:`feature_engineering_algorithms_relboost` and
the documentation of the particular class). 

Examples:
    A minimal version of a data science project using the
    :mod:`~getml.models` module might look like this:

    First, we need to have a relational dataset and upload it to the
    getML engine (here, we simulate this using 
    :meth:`~getml.datasets.make_numerical`).

    .. code-block:: python

        population_table, peripheral_table = getml.datasets.make_numerical()

        population_placeholder = population_table.to_placeholder()
        peripheral_placeholder = peripheral_table.to_placeholder()

        population_placeholder.join(peripheral_placeholder,
                                    join_key="join_key",
                                    time_stamp="time_stamp"
        )

    Using the :class:`~getml.data.Placeholder`s, we can now
    construct a model handler containing all components required for
    the ML part of the project. Calling its
    :meth:`~getml.models.MultirelModel.send` method tells the getML
    engine to create a model corresponding to the Python
    handler. (Alternatively, we could use
    :func:`~getml.models.load_model` to load and existing model from
    the getML engine or construct a new one using the
    :meth:`~getml.models.MultirelModel.copy` method).

    .. code-block:: python

        model = getml.models.MultirelModel(
            aggregation=[
                getml.models.aggregations.Count,
                getml.models.aggregations.Sum
            ],
            population=population_placeholder,
            peripheral=peripheral_placeholder,
            loss_function=getml.models.loss_functions.SquareLoss(),
            feature_selector=getml.predictors.LinearRegression(),
            predictor=getml.predictors.XGBoostRegressor(),
            num_features=10,
            share_aggregations=1.0,
            max_length=1,
            num_threads=0
        )

        model.send()

    This model enables us to train the
    e.g. :class:`~getml.predictors.XGBoostRegressor` we assigned to
    the :attr:`~getml.models.MultirelModel.predictor` member on our
    data and validate its performance. (For the sake of brevity we
    omit the creation of a validation set or any new data in the
    remaining examples).

    .. code-block:: python

        model = model.fit(
            population_table=population_table,
            peripheral_tables=peripheral_table
        )

        scores = model.score(
            population_table=population_table,
            peripheral_tables=peripheral_table
        )

    You can use getML to transform the input data into the
    set of generated features, which can be used with any external ML
    library:

    .. code-block:: python

        features = model.transform(
            population_table=population_table,
            peripheral_tables=peripheral_table
        )

    You can also use getML to build an end-to-end data science pipeline
    by using its built-in :mod:`~getml.predictors` making predictions
    for new, unseen data.

    .. code-block:: python

        predictions = model.predict(
            population_table=population_table,
            peripheral_tables=peripheral_table
        )

    getML allows you to quickly deploy your
    model into production. In order to access the features and
    predictions via the HTTP endpoint of the getML monitor. You need
    to call the following command:

    .. code-block:: python

        model.deploy(True)

Note:

    The lifecycle of the models works as
    follows: :class:`~getml.models.MultirelModel` and
    :class:`~getml.models.RelboostModel` combined with
    :meth:`~getml.models.MultirelModel.send` act as the constructors
    of new models in the getML engine. There, they will be held in
    memory as long as the engine is running and the current project is
    not changed. Loading a different project using
    :func:`~getml.engine.set_project` discards all models in memory
    and loads those associated with the new session from the
    corresponding JSON files in the project folder. 

    Calling :meth:`~getml.models.MultirelModel.send` on an existing
    model will overwrite the model in the engine and requires you to
    refit it.

    Models are saved automatically after you call any of the following methods:
    :meth:`~getml.models.MultirelModel.deploy`,
    :meth:`~getml.models.MultirelModel.fit`, and
    :meth:`~getml.models.MultirelModel.score` 
    (using the private :meth:`~getml.models.MultirelModel._save` method).

    Models are loaded automatically after you call 
    :meth:`~getml.engine.set_project`.

"""

from .list_models import list_models
from .load_model import load_model
from .multirel_model import MultirelModel
from .relboost_model import RelboostModel

__all__ = (
    "aggregations",
    "list_models",
    "load_model",
    "loss_functions",
    "MultirelModel",
    "RelboostModel"
)
