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

import datetime
import json
import numbers
import time
import socket

import numpy as np
import pandas as pd

from getml import (
    data,
    engine,
    predictors
)

from getml.data import (
    Placeholder,
    _decode_placeholder,
    _decode_joined_tables
)

import getml.communication as comm

from getml.predictors import _Predictor

from .modutils import (
    _make_random_name,
    _print_time_taken
)

from .loss_functions import (
    _decode_loss_function,
    _LossFunction,
    SquareLoss
)

from .list_models import list_models
from .validation import _validate_relboost_model_parameters

# --------------------------------------------------------------------

class RelboostModel(object):
    """Feature engineering based on Gradient Boosting.
    
    :class:`~getml.models.RelboostModel` automates feature engineering
    for relational data and time series. It is based on a
    generalization of the XGBoost algorithm to relational data, hence
    the name.

    For more information on the underlying feature engineering
    algorithm, check out
    :ref:`feature_engineering_algorithms_relboost`. For details about
    the :class:`~getml.models.RelboostModel` container in general, see
    the documentation of the :mod:`~getml.models` module.

    Examples:
        A :class:`~getml.models.MultirelModel` can be created in two
        different ways. The first one is to directly use the 
        constructor:
        
        .. code-block:: python

            population_table, peripheral_table = getml.datasets.make_numerical()

            population_placeholder = population_table.to_placeholder()
            peripheral_placeholder = peripheral_table.to_placeholder()

            population_placeholder.join(peripheral_placeholder,
                                        join_key="join_key",
                                        time_stamp="time_stamp"
            )

            model = getml.models.RelboostModel(
                population=population_placeholder,
                peripheral=peripheral_placeholder,
                name="relboost",
                predictor=getml.predictors.LinearRegression()
            )

        This creates a handler in the Python
        API. To construct the actual model in the getML engine, the
        information in the handler has to be sent to the engine:

        .. code-block:: python

            model.send()

        You can also call the
        :func:`~getml.models.RelboostModel` constructor with the
        `send` argument set to True.

        The second way of obtaining a
        :class:`~getml.models.RelboostModel` handler to a model is to
        use :func:`~getml.models.load_model`:

        .. code-block:: python

            model_loaded = getml.models.load_model("model-name")

    Args:
        population (:class:`~getml.data.Placeholder`):

            Abstract representation of the main table.

        peripheral (Union[:class:`~getml.data.Placeholder`, List[:class:`~getml.data.Placeholder`]]): 

            Abstract representations of the additional tables used to
            augment the information provided in `population`. These
            have to be the same objects that got
            :meth:`~getml.data.Placeholder.join` on the
            `population` :class:`~getml.data.Placeholder` and
            their order strictly determines the order of the
            peripheral :class:`~getml.data.DataFrame` provided in
            the 'peripheral_tables' argument of
            :meth:`~getml.models.RelboostModel.fit`,
            :meth:`~getml.models.RelboostModel.predict`,
            :meth:`~getml.models.RelboostModel.score`, and
            :meth:`~getml.models.RelboostModel.transform`.

        name (str, optional):

            Unique name of the container created in the getML
            engine. If an empty string is provided, a random value
            based on the current time stamp will be used.

        feature_selector (:class:`~getml.predictors`, optional):

            Predictor used to selected the best features among all
            automatically generated ones.

        predictor (:class:`~getml.predictors`, optional):

            Predictor used to make predictions on new, unseen data.

        units (dict, optional):

            DEPRECATED: only required when a
            :py:class:`pandas.DataFrame` is provided in the
            :meth:`~getml.models.RelboostModel.fit`,
            :meth:`~getml.models.RelboostModel.predict`,
            :meth:`~getml.models.RelboostModel.score`, and
            :meth:`~getml.models.RelboostModel.transform` method. If
            you already uploaded your data to the getML engine, this
            argument will not have any effect and can be omitted.

        session_name (string, optional):

            Determines whether which :mod:`~getml.hyperopt` run the
            model was created in or - in case of an empty string - if
            it's a stand-alone one.
        
        allow_null_weights (bool, optional):
        
            Whether you want to allow
            :class:`~getml.models.RelboostModel` to set weights to
            NULL.
        
        delta_t (float, optional):

            Frequency with which lag variables will be explored in a
            time series setting. When set to 0.0, there will be no lag
            variables.

            Please note that getML does not handle UNIX time stamps,
            but encodes time as multiples and fractions of
            days since the 01.01.1970 (1970-01-01T00:00:00). For
            example :math:`7.334722222222222 = 7 + 6/24 + 2/(24*60)`
            would be interpreted 1970-01-08T06:02:00.

            For more information see
            :ref:`data_model_time_series`. Range: [0, :math:`\\infty`]

        gamma (float, optional):

            During the training of Relboost, which is based on
            gradient tree boosting, this value serves as the minimum
            improvement in terms of the `loss_function` required for a
            split of the tree to be applied. Larger `gamma` will lead
            to fewer partitions of the tree and a more conservative
            algorithm. Range: [0, :math:`\\infty`]

        include_categorical (bool, optional):

            Whether you want to pass categorical columns from the
            population table to the `feature_selector` and
            `predictor`. Passing columns directly allows you to include
            handcrafted feature as well as raw data. Note, however,
            that this does not guarantee their presence in the
            resulting features because it is the task of the
            `feature_selector` to pick only the best performing
            ones.

        loss_function (:class:`~getml.models.loss_functions`, optional):

            Objective function used by the feature engineering algorithm
            to optimize your features. For regression problems use
            :class:`~getml.models.loss_functions.SquareLoss` and for
            classification problems use
            :class:`~getml.models.loss_functions.CrossEntropyLoss`.

        max_depth (int, optional):

            Maximum depth of the trees generated during the gradient
            tree boosting. Deeper trees will result in more complex
            models and increase the risk of overfitting. Range: [0,
            :math:`\\infty`]

        min_num_samples (int, optional):

            Determines the minimum number of samples a subcondition
            should apply to in order for it to be considered. Higher
            values lead to less complex statements and less danger of
            overfitting. Range: [1, :math:`\\infty`]

        num_features (int, optional):

            Number of features generated by the feature engineering 
            algorithm. For the total number of features
            available `share_selected_features` has to be taken into
            account as well. Range: [1, :math:`\\infty`]

        num_subfeatures (int, optional):

            The number of subfeatures you would like to extract in a
            subensemble (for snowflake data model only). See
            :ref:`data_model_snowflake_schema` for more
            information. Range: [1, :math:`\\infty`]

        num_threads (int, optional):

            Number of threads used by the feature engineering algorithm. If set to
            zero or a negative value, the number of threads will be
            determined automatically by the getML engine. Range:
            [-:math:`\\infty`, :math:`\\infty`]

        reg_lambda (float, optional):

            L2 regularization on the weights in the gradient boosting
            routine. This is one of the most important hyperparameters
            in the :class:`~getml.models.RelboostModel` as it allows
            for the most direct regularization. Larger values will
            make the resulting model more conservative. Range: [0,
            :math:`\\infty`]

        sampling_factor (float, optional):

            Relboost uses a bootstrapping procedure (sampling with
            replacement) to train each of the features. The sampling
            factor is proportional to the share of the samples
            randomly drawn from the population table every time
            Relboost generates a new feature. A lower sampling factor
            (but still greater than 0.0), will lead to less danger of
            overfitting, less complex statements and faster
            training. When set to 1.0, roughly 20,000 samples are drawn
            from the population table. If the population table
            contains less than 20,000 samples, it will use standard
            bagging. When set to 0.0, there will be no sampling at
            all. Range: [0, :math:`\\infty`]

        seed (Union[int,None], optional):

            Seed used for the random number generator that underlies
            the sampling procedure to make the calculation
            reproducible. Due to nature of the underlying algorithm
            this is only the case if the fit is done without
            multithreading. To reflect this, a `seed` of None does
            represent an unreproducible and is only allowed to be set
            to an actual integer if both `num_threads` and ``n_jobs``
            instance variables of the `predictor` and
            `feature_selector` - if they are instances of either
            :class:`~getml.predictors.XGBoostRegressor` or
            :class:`~getml.predictors.XGBoostClassifier` - are set to
            1. Internally, a `seed` of None will be mapped to
            5543. Range: [0, :math:`\\infty`]

        send (bool, optional):

            If True, the Model will be automatically sent to the getML
            engine without you having to explicitly call
            :meth:`~getml.models.RelboostModel.send`.

        share_selected_features (float, optional):

            Percentage of features selected by the
            `feature_selector`. Any feature with a importance of zero
            will be removed. Therefore, the number of features
            actually selected can be smaller than `num_features` *
            `share_selected_features`.  When set to 0.0, no feature
            selection will be conducted and all generated ones will
            provided in :meth:`~getml.models.RelboostModel.transform`
            and used in
            :meth:`~getml.models.RelboostModel.predict`. Range: [0, 1]

        shrinkage (float, optional):

            Since Relboost works using a gradient-boosting-like
            algorithm, `shrinkage` (or learning rate) scales down the
            weights and thus the impact of each new tree. This gives
            more room for future ones to improve the overall
            performance of the model in this greedy algorithm. It must
            be between 0.0 and 1.0 with higher values leading to more
            danger of overfitting. Range: [0, 1]

        silent (bool, optional):

            Controls the logging during training.

        target_num (int, optional):

            Signifies which of the targets to use, since
            :class:`~getml.models.RelboostModel` does not support
            multiple targets. See :ref:`annotating_roles_target` for
            details. Range: [0, :math:`\\infty`]

        use_timestamps (bool, optional):

            Whether you want to ignore all elements in the peripheral
            tables where the time stamp is greater than the one in the
            corresponding elements of the population table. In other
            words, this determines whether you want add the condition

            .. code-block:: sql

                t2.time_stamp <= t1.time_stamp

            at the very end of each feature. It is strongly recommend
            to enable this behavior.

        Raises:
            TypeError:
                If any of the input arguments is of wrong type.
            KeyError: 
                If an unsupported instance variable is encountered
                (via :meth:`~getml.models.RelboostModel.validate`).
            TypeError: 
                If any instance variable is of wrong type (via
                :meth:`~getml.models.RelboostModel.validate`).
            ValueError:
                If any instance variable does not match its possible
                choices (string) or is out of the expected bounds
                (numerical) (via
                :meth:`~getml.models.RelboostModel.validate`).

    """
        # ------------------------------------------------------------

    def __init__(self,
                 population,
                 peripheral,
                 name="",
                 feature_selector=None,
                 predictor=None,
                 units=dict(),
                 session_name="",
                 allow_null_weights=False,
                 delta_t=0.0,
                 gamma=0.0,
                 include_categorical=False,
                 loss_function=SquareLoss(),
                 max_depth=3,
                 min_num_samples=1,
                 num_features=100,
                 num_subfeatures=100,
                 num_threads=0,
                 reg_lambda=0.0,
                 sampling_factor=1.0,
                 seed=None,
                 send=False,
                 share_selected_features=0.0,
                 shrinkage=0.1,
                 silent=False,
                 target_num=0,
                 use_timestamps=True):

	# ------------------------------------------------------------
        
        # In case a single peripheral table was provided directly, it
        # has to be wrapped into a list.
        if isinstance(peripheral, Placeholder):
            peripheral = [peripheral]
            
	# ------------------------------------------------------------
        
        if name == "":
            name = self._make_name()
        
        self.type = "RelboostModel"
        
	# ------------------------------------------------------------
       
        self.allow_null_weights = allow_null_weights
        self.delta_t = delta_t
        self.feature_selector = feature_selector
        self.gamma = gamma
        self.include_categorical = include_categorical
        self.loss_function = loss_function
        self.max_depth = max_depth
        self.min_num_samples = min_num_samples	
        self.name = name
        self.num_features = num_features
        self.num_subfeatures = num_subfeatures
        self.num_threads = num_threads
        self.peripheral = peripheral
        self.population = population
        self.predictor = predictor
        self.reg_lambda = reg_lambda
        self.sampling_factor = sampling_factor
        self.seed = seed
        self.session_name = session_name
        self.share_selected_features = share_selected_features
        self.shrinkage = shrinkage
        self.silent = silent
        self.target_num = target_num
        self.units = units
        self.use_timestamps = use_timestamps
        
        # ------------------------------------------------------------
        
        self.validate()

	# ------------------------------------------------------------

	# If requested, send the newly constructed model to the
        # engine.
        if send:
            self.send()
            
    # ----------------------------------------------------------------
    
    def __eq__(self, other):
        """Compares the current instance of the
        :class:`~getml.models.RelboostModel` with another one.

        Args:
            other: Another :class:`~getml.models.RelboostModel` to
                compare the current instance against.

        Returns:
            bool: Whether the current instance and `other` share the
                same content.

        Raises:
            TypeError: If `other` is not of class
                :class:`~getml.models.RelboostModel`
        """
        
        if not isinstance(other, RelboostModel):
            raise TypeError("A RelboostModel can only be compared to another RelboostModel")

	# ------------------------------------------------------------
    
        # Check whether both objects have the same number of instance
        # variables.
        if len(set(self.__dict__.keys())) != len(set(other.__dict__.keys())):
            return False
    
	# ------------------------------------------------------------
        
        for kkey in self.__dict__:
            
            if kkey not in other.__dict__:
                return False
            
            # Take special care when comparing numbers.
            if isinstance(self.__dict__[kkey], numbers.Real):
                if not np.isclose(self.__dict__[kkey], other.__dict__[kkey]):
                    return False
            
            elif self.__dict__[kkey] != other.__dict__[kkey]:
                return False
            
	# ------------------------------------------------------------
        
        return True

    # ----------------------------------------------------------------

    def __repr__(self):
        return str(self)
    
    # ----------------------------------------------------------------

    def __str__(self):
        
	# ------------------------------------------------------------
	# String containing the final representation
        result = ""
        
	# ------------------------------------------------------------
        # Define some custom indentation levels for beautification.
        indent1 = "  "
        indent2 = indent1 + indent1

	# ------------------------------------------------------------
		
        result += "RelboostModel:"
        
	# ------------------------------------------------------------
	
        for kkey, vvalue in self.__dict__.items():
            
            # ---------------------------------------------------------------
            # Some of the fields need special treatment 
            
            if kkey == "loss_function":
                
                # For now the loss function does feature only a single
                # instance variable which is a string holding the
                # class name. Thus, we will just display latter.
                result += "\n" + indent1 + kkey + ": " + vvalue.type
            
	        # ----------------------------------------------------
            
            elif kkey == "peripheral":

                if vvalue is not None:
                    # The peripheral key is a list of Placeholder and does require
                    # special care.
                    result += "\n" + indent1 + "peripheral (list):"

                    for pplaceholder in vvalue:
                        result += "\n" + indent2 + str(pplaceholder).replace("\n", "\n" + indent2)
                else:
                    result += "\n" + indent1 + "peripheral: None"
                    
	            # ------------------------------------------------
	
            elif kkey == "population":
                
                if vvalue is not None:
                    # In case of the joined tables we do not care
                    # about the presence of the 'Placeholder:'
                    # line.
                    result += "\n" + indent1 + "population (Placeholder):" + str(vvalue).lstrip("Placeholder:").replace("\n", "\n" + indent1)
                else:
                    result += "\n" + indent1 + "population: None"
                    
	            # ------------------------------------------------
                
            elif kkey == "predictor" or kkey == "feature_selector":
                
                if vvalue is not None:
                    result += "\n" + indent1 + kkey +  ": " + str(vvalue).replace("\n","\n" + indent1)
                else:
                    result += "\n" + indent1 + kkey + ": None"
                    
	            # ------------------------------------------------
            
            else:
                result += "\n" + indent1 + kkey + ": " + str(vvalue)
        
	# ------------------------------------------------------------
	
        return result

        # ------------------------------------------------------------

    def _close(self, sock):
        """
        Raises:
            TypeError: If `sock` is not of type 
                :py:class:`socket.socket`
        """
    
        if type(sock) is not socket.socket:
            raise TypeError("'sock' must be a socket.")
        
	# ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = self.type+".close"
        cmd["name_"] = self.name

        comm.send_string(sock, json.dumps(cmd))

        msg = comm.recv_string(sock)

        if msg != "Success!":
            comm.engine_exception_handler(msg)
        
    # ----------------------------------------------------------------

    def _convert_peripheral_tables(self, peripheral_tables, sock):
        """Converts a list of :class:`getml.data.DataFrame` and
        :class:`pandas.DataFrame` to a :class:`getml.data.DataFrame`
        only list.

        All occurrences of :class:`pandas.DataFrame` will be converted
        to :class:`getml.data.DataFrame`. In order to achieve this a
        new DataFrame will be constructed using the schema information
        of the `peripheral` tables stored in the current instance. The
        mapping which peripheral schema will be used for which element
        in `peripheral_tables` is determined by order. Therefore, the
        order of the peripheral tables supplied in `peripheral` upon
        construction :class:`~getml.models.RelboostModel` and supplied
        in `peripheral_tables` *must* be identically.

        Note that when converting a :class:`pandas.DataFrame` into a
        :class:`getml.data.DataFrame` the latter will be created on
        the engine first and all the data of the former will be
        uploaded into it afterwards. Thus, depending on the size of
        you tables, this step might take a while.

        Args:
            peripheral_tables (list): List of
                :class:`getml.data.DataFrame` or
                :class:`pandas.DataFrame`. Both classes can be
                arbitrarily mixed.
            sock (:py:class:`socket.socket`): Established
                communication to the getML engine used to upload
                create new data frames and upload data when converting
                a :class:`pandas.DataFrame` into a
                :class:`getml.data.DataFrame`.

        Raises:
            TypeError: If `peripheral_tables` is not a list of
                :class:`pandas.DataFrame` and
                :class:`getml.data.DataFrame` or `sock` is not of
                type :py:class:`socket.socket`.

        Returns:
            List: Version of `peripheral_tables` containing only
                :class:`getml.data.DataFrame` elements.

        """

	# ------------------------------------------------------------
        
        # In case a single peripheral table was provided directly, it
        # has to be wrapped into a list.
        if isinstance(peripheral_tables, pd.DataFrame) or isinstance(peripheral_tables, data.DataFrame):
            peripheral_tables = [peripheral_tables]
            
	# ------------------------------------------------------------
        
        if type(peripheral_tables) is not list or not (len(peripheral_tables) > 0 and all([isinstance(ll, data.DataFrame) or isinstance(ll, pd.DataFrame) for ll in peripheral_tables])):
            raise TypeError("'peripheral_tables' must be a getml.data.DataFrame or pandas.DataFrame or a list of those.")
        if type(sock) is not socket.socket:
            raise TypeError("'sock' must be a socket.")

	# ------------------------------------------------------------
    
        # Will contain all resulting getml.data.DataFrame
        peripheral_data_frames = []
        
	# ------------------------------------------------------------
	
        for ii, pperipheral_table in enumerate(peripheral_tables):

            if type(pperipheral_table) is data.DataFrame:

                peripheral_data_frames.append(pperipheral_table)
                
            elif type(pperipheral_table) is pd.DataFrame:

                categorical_peripheral = [
                    per.categorical for per in self.peripheral
                ]

                numerical_peripheral = [
                    per.numerical for per in self.peripheral
                ]

                join_keys_peripheral = [
                    per.join_keys for per in self.peripheral
                ]

                names_peripheral = [
                    per.name for per in self.peripheral
                ]

                time_stamps_peripheral = [
                    per.time_stamps for per in self.peripheral
                ]
                
	        # ----------------------------------------------------
	        
                # Create a data frame on the engine.
                peripheral_data_frames.append(
                    data.DataFrame(
                        name=_make_random_name(),
                        roles={
                            "join_key": join_keys_peripheral[ii],
                            "time_stamp": time_stamps_peripheral[ii],
                            "categorical": categorical_peripheral[ii],
                            "numerical": numerical_peripheral[ii],
                            "target": []}
                    )
                )

	        # ----------------------------------------------------

                # Upload the data contain in the pandas.DataFrame.
                peripheral_data_frames[ii]._send_pandas_df(
                    data_frame=pperipheral_table, 
                    sock=sock
                )
                
	        # ----------------------------------------------------
	        
            else:
                raise TypeError(
                    "Unknown type of peripheral table"  + str(ii) + """
                    : [""" + str(type(pperipheral_table)) + """ 
                    ]. Only getml.data.DataFrame and pandas.DataFrame 
                    are allowed!""")
 
	# ------------------------------------------------------------
        # The changes to the units will only be temporary.
       
        for df in peripheral_data_frames:
            colnames = df.numerical_names
            colnames += df.categorical_names

            for cname in colnames:
                if cname in self.units:
                    unit = self.units[cname]
                    df._set_unit(cname, unit, sock)
        
        # ------------------------------------------------------------
	
        return peripheral_data_frames

    # ----------------------------------------------------------------

    def _convert_population_table(self, population_table, targets, sock):
        """Ensures an input of either class :class:`getml.data.DataFrame` or
        :class:`pandas.DataFrame` will be a valid
        :class:`getml.data.DataFrame`.

        If `population_table` is a :class:`pandas.DataFrame` it will
        be converted to :class:`getml.data.DataFrame`. In order to
        achieve this a new DataFrame will be constructed using the
        schema information of the `population` tables stored in the
        current instance and the `targets` supplied as input argument.

        Note that when converting a :class:`pandas.DataFrame` into a
        :class:`getml.data.DataFrame` the latter will be created on
        the engine first and all the data of the former will be
        uploaded into it afterwards. Thus, depending on the size of
        you tables, this step might take a while.

        Args:
            population_table (:class:`getml.data.DataFrame` or
                :class:`pandas.DataFrame`): Table which' class should
                be ensured.
            targets (List[str]): List with the names of all columns
                considered the target variable. Depending on the
                context this function is called, e.g. within
                :method:`~getml.models.RelboostModel.fit` or
                :method:`~getml.models.RelboostModel.predict`, it will
                just correspond to the `targets` instance variable of
                the current instance's `population` or requires some
                more processing and checking.
            sock (:py:class:`socket.socket`): Established
                communication to the getML engine used to create new
                data frame and upload data when converting a
                :class:`pandas.DataFrame` into a
                :class:`getml.data.DataFrame`.

        Raises:
            TypeError: If any of the input arguments is not of the
                requested type.

        Returns:
            List: Version of `peripheral_tables` containing only
                :class:`getml.data.DataFrame` elements.

        """
        
        if not (isinstance(population_table, data.DataFrame) or isinstance(population_table, pd.DataFrame)):
            raise TypeError("'population_table' must be a getml.data.DataFrame or pandas.data.DataFrame")
        if type(targets) is not list or not (len(targets) == 0 or all([type(ll) is str for ll in targets])):
            raise TypeError("'targets' must be an empty list or a list of str.")
        if type(sock) is not socket.socket:
            raise TypeError("'sock' must be a socket.")

	# ------------------------------------------------------------
    
        if type(population_table) == data.DataFrame:

            population_data_frame = population_table
            
	    # --------------------------------------------------------

        elif type(population_table) == pd.DataFrame:

            # Create a data frame on the engine.
            population_data_frame = data.DataFrame(
                name=_make_random_name(),
                roles={
                    "join_key": self.population.join_keys,
                    "time_stamp": self.population.time_stamps,
                    "categorical": self.population.categorical,
                    "numerical": self.population.numerical,
                    "target": targets}
            )

	    # --------------------------------------------------------

	    # Upload the data contain in the pandas.DataFrame.
            population_data_frame._send_pandas_df(
                data_frame=population_table, 
                sock=sock
            )

	    # --------------------------------------------------------

        else:
            raise TypeError(
                """Unknown type of population table: [
                """ + str(type(population_table)) + """
                ]. Only getml.data.DataFrame and 
                pandas.DataFrame are allowed!""")

	# ------------------------------------------------------------
        # The changes to the units will only be temporary.
       
        colnames = population_data_frame.numerical_names
        colnames += population_data_frame.categorical_names

        for cname in colnames:
            if cname in self.units:
                unit = self.units[cname]
                population_data_frame._set_unit(cname, unit, sock)
    
	# ------------------------------------------------------------
	
        return population_data_frame
 
    # ----------------------------------------------------------------
    
    def _make_name(self):
        return datetime.datetime.now().isoformat().split(".")[0].replace(':', '-') + "-relboost"

    # ----------------------------------------------------------------
    
    def _save(self):
        """
        Saves the model as a JSON file.
        """

        # ------------------------------------------------------------
        # Send JSON command to getML engine

        cmd = dict()
        cmd["type_"] = self.type+".save"
        cmd["name_"] = self.name

        comm.send(cmd)

        # ------------------------------------------------------------

    def _score(self, yhat, y):
        """
        Returns the score for a set of predictions.
        
        Args:
            yhat (numpy.ndarray): Predictions.
            y (numpy.ndarray): Targets.

        Raises:
            TypeError: If any of the input arguments is of wrong type.
        """
        
        if type(yhat) is not np.ndarray:
            raise TypeError("'yhat' must be a numpy.ndarray.")
        if type(y) is not np.ndarray:
            raise TypeError("'y' must be a numpy.ndarray.")

        # ------------------------------------------------------------
        # Build the cmd string

        cmd = dict()
        cmd["type_"] = "RelboostModel.score"
        cmd["name_"] = self.name

        # ------------------------------------------------------------
        # Establish connection with the getML engine and send command

        s = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(s)

        if msg != "Found!":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------
        # Send data
        
        comm.send_matrix(s, yhat)

        comm.send_matrix(s, y)

        msg = comm.recv_string(s)

        # ------------------------------------------------------------
        # Ensure success, receive scores

        if msg != "Success!":
            comm.engine_exception_handler(msg)

        scores = comm.recv_string(s)

        s.close()

        # ------------------------------------------------------------

        return json.loads(scores)

        # ------------------------------------------------------------

    def _transform(
        self,
        peripheral_data_frames,
        population_data_frame,
        sock,
        score=False,
        predict=False,
        df_name="",
        table_name=""
    ):
        """Returns the features learned by the model or writes them into a data base.

        Args:  
            population_table (:class:`getml.data.DataFrame`):
                Population table. Targets will be ignored.
            peripheral_tables (List[:class:`getml.data.DataFrame`]):
                Peripheral tables.
                The peripheral tables have to be passed in the exact same order as their
                corresponding placeholders!
            sock (:py:class:`socket.socket`): TCP socket used to
                communicate with the getML engine.
            score (bool, optional): Whether the engine should calculate the
                scores of the model based on the input data.
            predict (bool, optional): Whether the engine should transform the
                input data into features.
            df_name (str, optional):
                If not an empty string, the resulting features will be
                written into a newly created DataFrame, instead of returning
                them. 
            table_name (str, optional):
                If not an empty string, the resulting features will be
                written into the data base, instead of returning
                them. See :ref:`unified_import_interface` for
                further information.

        Raises:
            TypeError: If any of the input arguments is of wrong type.

        """

	# ------------------------------------------------------------
        
        # In case a single peripheral table was provided directly, it
        # has to be wrapped into a list.
        if isinstance(peripheral_data_frames, data.DataFrame):
            peripheral_data_frames = [peripheral_data_frames]

        # ------------------------------------------------------------
        
        if type(peripheral_data_frames) is not list or not (len(peripheral_data_frames) > 0 and all([isinstance(ll, data.DataFrame) for ll in peripheral_data_frames])):
            raise TypeError("'peripheral_data_frames' must be a getml.data.DataFrame or a list of those.")
        if not isinstance(population_data_frame, data.DataFrame):
            raise TypeError("'population_data_frame' must be a getml.data.DataFrame")
        if type(sock) is not socket.socket:
            raise TypeError("'sock' must be a socket.")
        if type(score) is not bool:
            raise TypeError("'score' must be of type bool")
        if type(predict) is not bool:
            raise TypeError("'predict' must be of type bool")
        if type(table_name) is not str:
            raise TypeError("'table_name' must be of type str")
	
	# ------------------------------------------------------------
    
        # Prepare the command for the getML engine
        cmd = dict()
        cmd["type_"] = self.type+".transform"
        cmd["name_"] = self.name

        cmd["score_"] = score
        cmd["predict_"] = predict

        cmd["peripheral_names_"] = [df.name for df in peripheral_data_frames]
        cmd["population_name_"] = population_data_frame.name

        cmd["df_name_"] = df_name
        cmd["table_name_"] = table_name
        
        comm.send_string(sock, json.dumps(cmd))

        # ------------------------------------------------------------
        # Do the actual transformation

        msg = comm.recv_string(sock)

        if msg == "Success!":
            if table_name == "" and df_name == "":
                yhat = comm.recv_matrix(sock)
            else:
                yhat = None
        else:
            comm.engine_exception_handler(msg)
 
        # ------------------------------------------------------------

        return yhat
    
    # ----------------------------------------------------------------

    def copy(self, new_name=""):
        """Creates a copy of the model in the engine and returns its 
        handler.
        
        Since there can not be two models in the engine holding the
        same name, a `new_name` has to be assigned to the new
        one (which must not be present in the engine yet).

        Examples:

            A possible use case is to pick a particularly well-performing
            model, create a new one based on it, do a slight adjustment of
            its attributes, and fit it.

            .. code-block:: python

                model = getml.models.load_model("relboost")

                model_new = model.copy("model-new")
                model_new.shrinkage = 0.8

                model_new.send()

                model_new.fit(population_table, peripheral_table)

        Args:
            new_name (str, optional): Name of the new model. In case
                of an empty string, a new name will be generated 
                automatically.

        Raises:
            NameError: If there is already a model present in the
                engine carrying the name `new_name`.
            TypeError: If `new_name` is not of type str.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.RelboostModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.RelboostModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.RelboostModel.validate`).

        Returns:
            :class:`getml.models.RelboostModel`:
                The handler of the copied model.

        """
        
        if type(new_name) is not str:
            raise TypeError("'new_name' must be of type str")
        
        # ------------------------------------------------------------
        
        self.validate()

        # ------------------------------------------------------------
        
        if new_name == "":
            new_name = self._make_name()
        
	# ------------------------------------------------------------
        
        # Check whether a model holding this name is already present
        # in the engine.
        model_names_dict = list_models()
        model_names = model_names_dict['multirel_models'] + model_names_dict['relboost_models']
        
        if new_name in model_names:
            raise NameError("A model called '"+new_name+"' is already present in the engine.")
        
	# ------------------------------------------------------------
	
        cmd = dict()
        cmd["type_"] = self.type+".copy"
        cmd["name_"] = new_name
        cmd["other_"] = self.name

        comm.send(cmd)
        
	# ------------------------------------------------------------
	
        # We can not use the load_model function in here because it
        # would create a circular dependence. Instead, we will
        # manually construct the model and load its content from the
        # engine using the refresh method.
        new_model = RelboostModel(
            name=new_name,
            population=Placeholder(name='placebert'),
            peripheral=Placeholder(name='placebert')
        ).refresh()

        # ------------------------------------------------------------

        return new_model

    # ----------------------------------------------------------------
    
    def delete(self):
        """
        Deletes the model from the engine.

        Raises:
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.RelboostModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.RelboostModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.RelboostModel.validate`).

        Note:
            Caution: You can not undo this action!
        """
        
        # ------------------------------------------------------------
        
        self.validate()

        # ------------------------------------------------------------
        
        # Send JSON command to getML engine
        cmd = dict()
        cmd["type_"] = self.type+".delete"
        cmd["name_"] = self.name
        cmd["mem_only_"] = False

        comm.send(cmd)

        # ------------------------------------------------------------
    
    def deploy(self, deploy):
        """Allows a fitted model to be addressable via an HTTP request.
        See :ref:`deployment` for details.
        
        Args:
            deploy (bool): If :code:`True`, the deployment of the model
                will be triggered.

        Raises:
            TypeError: If `deploy` is not of type bool.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.RelboostModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.RelboostModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.RelboostModel.validate`).

        """
        
        if type(deploy) is not bool:
            raise TypeError("'deploy' must be of type bool")
        
        # ------------------------------------------------------------
        
        self.validate()

	# ------------------------------------------------------------
	
        cmd = dict()
        cmd["type_"] = self.type+".deploy"
        cmd["name_"] = self.name
        cmd["deploy_"] = deploy

        comm.send(cmd)
    
        self._save()

    # ------------------------------------------------------------

    def fit(
        self,
        population_table,
        peripheral_tables
    ):
        """Trains the feature engineering algorithm and all predictors on the 
        provided data.

        Both the ``feature_selector`` and ``predictor`` will be
        trained alongside the Relboost feature engineering algorithm if present.

        Examples:

            .. code-block:: python

                model.fit(
                    population_table=population_table, 
                    peripheral_tables=peripheral_table)

        Args:
            population_table (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`]):
                Main table containing the target variable(s) and
                corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable.
            peripheral_tables (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`, List[:class:`pandas.DataFrame`],List[:class:`getml.data.DataFrame`]]):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. They have to be provided in the exact same
                order as their corresponding placeholders! A single
                DataFrame will be wrapped into a list internally.

        Raises:
            IOError: If the model corresponding to the instance
                variable ``name`` could not be found on the engine or
                the model could not be fitted.
            TypeError: If any input argument is not of proper type.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.RelboostModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.RelboostModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.RelboostModel.validate`).

        Note:

            This method will only work if there is a corresponding
            model in the getML engine. If you used the
            :class:`~getml.models.RelboostModel` constructor of the
            model in the Python API, be sure to use the
            :meth:`~getml.models.RelboostModel.send` method afterwards
            create its counterpart in the engine.

            All parameters customizing this process have been already
            supplied to the constructor and are assigned as instance
            variables. Any changes applied to them will only be
            respected if the :meth:`~getml.models.RelboostModel.send`
            method will be called on the modified version of the model
            first.

            If a `population_table` or `peripheral_tables` will be
            provided as :class:`pandas.DataFrame`, they will be
            converted to temporary :class:`getml.data.DataFrame`,
            uploaded to the engine, and discarded after the function
            call. Since `peripheral_tables` can very well be the same
            for the :meth:`~getml.models.RelboostModel.predict`,
            :meth:`~getml.models.RelboostModel.score`, and
            :meth:`~getml.models.RelboostModel.transform` methods,
            this way of interacting with the engine can be highly
            inefficient and is discouraged.

        """

	# ------------------------------------------------------------
        
        # In case a single peripheral table was provided directly, it
        # has to be wrapped into a list.
        if isinstance(peripheral_tables, pd.DataFrame) or isinstance(peripheral_tables, data.DataFrame):
            peripheral_tables = [peripheral_tables]
        
	# ------------------------------------------------------------
	
        if not (isinstance(population_table, data.DataFrame) or isinstance(population_table, pd.DataFrame)):
            raise TypeError("'population_table' must be a getml.data.DataFrame or pandas.data.DataFrame")
        if type(peripheral_tables) is not list or not (len(peripheral_tables) > 0 and all([isinstance(ll, data.DataFrame) or isinstance(ll, pd.DataFrame) for ll in peripheral_tables])):
            raise TypeError("'peripheral_tables' must be a getml.data.DataFrame or pandas.DataFrame or a list of those")
        
        # ------------------------------------------------------------
        
        self.send()

        # ------------------------------------------------------------
        
        # Prepare the command for the getML engine.
        cmd = dict()
        cmd["type_"] = self.type+".fit"
        cmd["name_"] = self.name

        # ------------------------------------------------------------
        
        # Send command to engine and make sure that model has been
        # found.
        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            sock.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------
        
        # Ensure all elements in `peripheral_tables` are of type
        # getml.data.DataFrame. All occurrences of type
        # pandas.DataFrame will be converted.
        peripheral_data_frames = self._convert_peripheral_tables(
            peripheral_tables,
            sock
        )

        # ------------------------------------------------------------
        
        targets = self.population.targets

        # Ensure `population_table` is of type
        # getml.data.DataFrame. In case it is of type
        # pandas.DataFrame instead, it will be converted.
        population_data_frame = self._convert_population_table(
            population_table,
            targets,
            sock
        )

        # ------------------------------------------------------------
        # Send the complete fit command.

        cmd = dict()
        cmd["type_"] = self.type+".fit"
        cmd["name_"] = self.name

        cmd["peripheral_names_"] = [df.name for df in peripheral_data_frames]
        cmd["population_name_"] = population_data_frame.name
        
	# ------------------------------------------------------------
	
        comm.send_string(sock, json.dumps(cmd))

        # ------------------------------------------------------------

        # Measure the performance.
        begin = time.time()

        print("Loaded data. Features are now being trained...")

        # Do the actual fitting
        msg = comm.recv_string(sock)
        
        end = time.time()

        # ------------------------------------------------------------
        # Print final message

        if "Trained" in msg:
            print(msg)
            _print_time_taken(begin, end, "Time taken: ")
            
	    # --------------------------------------------------------
	        
            # Tell the engine the fit is completed and we are about to
            # close the connection (not done within the _close
            # method).
            self._close(sock)
            
	    # --------------------------------------------------------
	        
        elif "has already been fitted" in msg:
            print(msg)
            print("")
            
	    # --------------------------------------------------------
	        
        else:
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        # Close the connection to the engine.
        sock.close()

	# ------------------------------------------------------------
	
        # Tell the engine (in a fresh connection established within
        # _save) to write a copy of the model held in memory to disk.
        self._save()

	# ------------------------------------------------------------
	        
        # Discard the current instance and replace it with the most
        # recent version found at the engine. This way we ensure we do
        # not miss any updates done on the engine.
        return self.refresh()
    
        # ------------------------------------------------------------

    def predict(
        self,
        population_table,
        peripheral_tables,
        table_name=""
    ):
        """Forecasts on new, unseen data using the trained ``predictor``.

        Returns the predictions generated by the model based on
        `population_table` and `peripheral_tables` or writes them into
        a data base named `table_name`.

        Examples:

            .. code-block:: python

                model.predict(
                    population_table=population_table,
                    peripheral_tables=peripheral_table)

        Args:  
            population_table (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`]):
                Main table corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable. Its target variable(s) will be ignored.
            peripheral_tables (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`, List[:class:`pandas.DataFrame`],List[:class:`getml.data.DataFrame`]]):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. They have to be provided in the exact same
                order as their corresponding placeholders! A single
                DataFrame will be wrapped into a list internally.
            table_name (str, optional): 
                If not an empty string, the resulting predictions will
                be written into the :mod:`~getml.database` of the same
                name. See :ref:`unified_import_interface` for further information.


        Raises:
            IOError: If the model corresponding to the instance
                variable ``name`` could not be found on the engine or
                the model could not be fitted.
            TypeError: If any input argument is not of proper type.
            ValueError: If no valid ``predictor`` was set.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.RelboostModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.RelboostModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.RelboostModel.validate`).

        Return:
            :class:`numpy.ndarray`:
                Resulting predictions provided in an array of the
                (number of rows in `population_table`, number of
                targets in `population_table`).

        Note:
            Only fitted models
            (:meth:`~getml.models.RelboostModel.fit`) can be used for
            prediction. In addition, a valid ``predictor`` must be
            trained as well.

            If a `population_table` or `peripheral_tables` will be
            provided as :class:`pandas.DataFrame`, they will be
            converted to temporary :class:`getml.data.DataFrame`,
            uploaded to the engine, and discarded after the function
            call. Since `peripheral_tables` can very well be the same
            for the :meth:`~getml.models.RelboostModel.predict`,
            :meth:`~getml.models.RelboostModel.score`, and
            :meth:`~getml.models.RelboostModel.transform` methods,
            this way of interacting with the engine can be highly
            inefficient and is discouraged.

        """

	# ------------------------------------------------------------
        
        # In case a single peripheral table was provided directly, it
        # has to be wrapped into a list.
        if isinstance(peripheral_tables, pd.DataFrame) or isinstance(peripheral_tables, data.DataFrame):
            peripheral_tables = [peripheral_tables]
        
	# ------------------------------------------------------------
	
        if not (isinstance(population_table, data.DataFrame) or isinstance(population_table, pd.DataFrame)):
            raise TypeError("'population_table' must be a getml.data.DataFrame or pandas.data.DataFrame")
        if type(peripheral_tables) is not list or not (len(peripheral_tables) > 0 and all([isinstance(ll, data.DataFrame) or isinstance(ll, pd.DataFrame) for ll in peripheral_tables])):
            raise TypeError("'peripheral_tables' must be a getml.data.DataFrame or pandas.DataFrame or a list of those")
        if type(table_name) is not str:
            raise TypeError("'table_name' must be of type str")
        
        # ------------------------------------------------------------
        
        self.validate()

        # ------------------------------------------------------------

        # Prepare the command for the getML engine.
        cmd = dict()
        cmd["type_"] = self.type+".transform"
        cmd["name_"] = self.name
        cmd["http_request_"] = False
        
        # ------------------------------------------------------------
        
        # Send command to engine and make sure that model has
        # been found.
        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            sock.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        # Ensure all elements in `peripheral_tables` are of type
        # getml.data.DataFrame. All occurrences of type
        # pandas.DataFrame will be converted.
        peripheral_data_frames = self._convert_peripheral_tables(
            peripheral_tables,
            sock
        )

        # ------------------------------------------------------------

        # Ensure the targets in listed in the `population` instance
        # variable are corresponding to columns in the povided
        # pandas.DataFrame - in case this class of input was used.
        if type(population_table) is data.DataFrame:
            targets = []
        else:
            targets = [
                elem for elem in self.population.targets
                if elem in population_table.columns
            ]

        # Ensure `population_table` is of type
        # getml.data.DataFrame. In case it is of type
        # pandas.DataFrame instead, it will be converted.
        population_data_frame = self._convert_population_table(
            population_table,
            targets,
            sock
        )

        # ------------------------------------------------------------
        # Get features as numpy array

        y_hat = self._transform(
            peripheral_data_frames, 
            population_data_frame, 
            sock, 
            predict = True, 
            table_name=table_name
        )

	# ------------------------------------------------------------
	        
        # Tell the engine the prediction is completed and we are about
        # to close the connection (not done within the _close
        # method).
        self._close(sock)

        # ------------------------------------------------------------

        # Close the connection to the engine.
        sock.close()

	# ------------------------------------------------------------
	
        return y_hat
    
        # ------------------------------------------------------------

    def refresh(self):
        """Reloads the model from the engine.

        Discards all local changes applied to the model after the last
        invocation of its :meth:`~getml.models.RelboostModel.send`
        method by loading the model corresponding to the ``name``
        attribute from the engine and replacing the attributes of the
        current instance with the results.

        Raises:
            IOError:
                If the engine did not send a proper model.

        Returns:
            :class:`~getml.models.RelboostModel`:
                Current instance
        """

        # ------------------------------------------------------------
        
        # Send JSON command to getml engine
        cmd = dict()
        cmd["type_"] = self.type+".refresh"
        cmd["name_"] = self.name

        s = comm.send_and_receive_socket(cmd)

        # ------------------------------------------------------------

        # Make sure everything went well and close
        # connection
        msg = comm.recv_string(s)

        s.close()

        if msg[0] != '{':
          comm.engine_exception_handler(msg)

        # ------------------------------------------------------------
        # Parse results.

        json_obj = json.loads(msg)
        
	# ------------------------------------------------------------
	
        # Assign those parameters defined as fundamental types. All
        # class objects will be reconstructed and assigned afterwards.

        for kkey in json_obj["hyperparameters_"]:
            
            # Exclude the more complex parameters.
            if kkey not in ['feature_selector_', 'loss_function_', 
                        'peripheral_', 'peripheral_schema_', 
                        'placeholder_', 'population_schema_', 
                        'predictor_']:
                
                # Remove the trailing underscore in the parameter
                # keys.
                self.__dict__[kkey[:len(kkey) - 1]] = json_obj["hyperparameters_"][kkey]
        
	# ------------------------------------------------------------
	
        if "predictor_" in json_obj["hyperparameters_"]:
            self.predictor = predictors._decode_predictor(json_obj["hyperparameters_"]["predictor_"])

	# ------------------------------------------------------------
	            
        if "feature_selector_" in json_obj["hyperparameters_"]:
            self.feature_selector = predictors._decode_predictor(json_obj["hyperparameters_"]["feature_selector_"])
        
        # ------------------------------------------------------------
        
        # If any of the ML subclasses is set to be multithreaded, the
        # results won't be reproducible and the seed will be
        # disregarded to make this fact transparent to the user.
        multithreaded = False
        
        if self.num_threads > 1:
            multithreaded = True
        if self.predictor is not None and (isinstance(self.predictor, predictors.XGBoostClassifier) or isinstance(self.predictor, predictors.XGBoostRegressor)) and self.predictor.n_jobs > 1:
            multithreaded = True
        if self.feature_selector is not None and (isinstance(self.feature_selector, predictors.XGBoostClassifier) or isinstance(self.feature_selector, predictors.XGBoostRegressor)) and self.feature_selector.n_jobs > 1:
            multithreaded = True

        if multithreaded:
            self.seed = None
        
        # ------------------------------------------------------------
	
        self.loss_function = _decode_loss_function(json_obj["hyperparameters_"]["loss_function_"])
        
        # ------------------------------------------------------------

        # The engine splits of the schema information of the
        # population table in the 'population_schema_' and the
        # relational information in the 'placeholder_' key.
        population = _decode_placeholder(json_obj["population_schema_"])

        # Before assigning the relational information all placeholders
        # in its 'joined_tables_' must be converted to proper
        # placeholder. Since they could themselves hold other joined
        # tables, we will use a recursive function for decoding.
        joined_tables = _decode_joined_tables(json_obj["placeholder_"]["joined_tables_"])

        population.set_relations(
                join_keys_used = json_obj["placeholder_"]["join_keys_used_"],
                other_join_keys_used = json_obj["placeholder_"]["other_join_keys_used_"],
                time_stamps_used = json_obj["placeholder_"]["time_stamps_used_"],
                other_time_stamps_used = json_obj["placeholder_"]["other_time_stamps_used_"],
                upper_time_stamps_used = json_obj["placeholder_"]["upper_time_stamps_used_"],
                joined_tables = joined_tables
        )

        self.population =  population

        # ------------------------------------------------------------

        # Since we are dealing with a list of peripheral placeholders
        # and not just a single dict, we have to be careful.
        peripheral_placeholders = list()
        for pp in range(0, len(json_obj["peripheral_"])):

            # The name of the peripheral placeholder is stored in the
            # 'peripheral_' array and all its schema information in
            # 'peripheral_schema_'.
            #
            # Caution: due to historical reasons the keys used by the
            # engine and the ones used by the constructor of the
            # placeholder do differ.
            pperipheral = Placeholder(
                name = json_obj["peripheral_"][pp],
                categorical = json_obj["peripheral_schema_"][pp]["categoricals_"],
                numerical = json_obj["peripheral_schema_"][pp]["numericals_"],
                join_keys = json_obj["peripheral_schema_"][pp]["join_keys_"],
                time_stamps = json_obj["peripheral_schema_"][pp]["time_stamps_"],
                targets = json_obj["peripheral_schema_"][pp]["targets_"]
            )

            peripheral_placeholders.append(pperipheral)

        self.peripheral = peripheral_placeholders        

	# ------------------------------------------------------------
	
        return self

    # ----------------------------------------------------------------

    def score(
        self,
        population_table,
        peripheral_tables
    ):
        """Calculates the performance of the ``predictor``.

        Returns different scores calculated on `population_table` and
        `peripheral_tables`.

        Examples:

            .. code-block:: python

                model.score(
                    population_table = population_table,
                    peripheral_tables = peripheral_table)

        Args:  
            population_table (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`]):
                Main table corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable. Its target variable(s) will be ignored.
            peripheral_tables (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`, List[:class:`pandas.DataFrame`],List[:class:`getml.data.DataFrame`]]):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. They have to be provided in the exact same
                order as their corresponding placeholders! A single
                DataFrame will be wrapped into a list internally.

        Raises:
            IOError: If the model corresponding to the instance
                variable ``name`` could not be found on the engine or
                the model could not be fitted.
            TypeError: If any input argument is not of proper type.
            ValueError: If no valid ``predictor`` was set.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.RelboostModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.RelboostModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.RelboostModel.validate`).

        Return:
            dict:

                Mapping of the name of the score (str) to the
                corresponding value (float).
        
                For regression problems the following scores are
                returned:

                * :const:`~getml.models.scores.rmse`
                * :const:`~getml.models.scores.mae`
                * :const:`~getml.models.scores.rsquared`

                For classification problems, on the other hand, the
                following scores are returned: Possible values for a
                classification problem are:

                * :const:`~getml.models.scores.accuracy`
                * :const:`~getml.models.scores.auc`
                * :const:`~getml.models.scores.cross_entropy`

        Note:

            Only fitted models
            (:meth:`~getml.models.RelboostModel.fit`) can be
            scored. In addition, a valid ``predictor`` must be trained
            as well.

            If a `population_table` or `peripheral_tables` will be
            provided as :class:`pandas.DataFrame`, they will be
            converted to temporary :class:`getml.data.DataFrame`,
            uploaded to the engine, and discarded after the function
            call. Since `peripheral_tables` can very well be the same
            for the :meth:`~getml.models.RelboostModel.predict`,
            :meth:`~getml.models.RelboostModel.score`, and
            :meth:`~getml.models.RelboostModel.transform` methods,
            this way of interacting with the engine can be highly
            inefficient and is discouraged.

        """

	# ------------------------------------------------------------
        
        # In case a single peripheral table was provided directly, it
        # has to be wrapped into a list.
        if isinstance(peripheral_tables, pd.DataFrame) or isinstance(peripheral_tables, data.DataFrame):
            peripheral_tables = [peripheral_tables]
        
	# ------------------------------------------------------------
	
        if not (isinstance(population_table, data.DataFrame) or isinstance(population_table, pd.DataFrame)):
            raise TypeError("'population_table' must be a getml.data.DataFrame or pandas.data.DataFrame")
        if type(peripheral_tables) is not list or not (len(peripheral_tables) > 0 and all([isinstance(ll, data.DataFrame) or isinstance(ll, pd.DataFrame) for ll in peripheral_tables])):
            raise TypeError("'peripheral_tables' must be a getml.data.DataFrame or pandas.DataFrame or a list of those")
        
        # ------------------------------------------------------------
        
        self.validate()

        # ------------------------------------------------------------
        
        # Prepare the command for the getml engine.
        cmd = dict()
        cmd["type_"] = self.type+".transform"
        cmd["name_"] = self.name
        cmd["http_request_"] = False

        # ------------------------------------------------------------

        # Send command to engine and make sure that model has
        # been found.
        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            sock.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        # Ensure all elements in `peripheral_tables` are of type
        # getml.data.DataFrame. All occurrences of type
        # pandas.DataFrame will be converted.
        peripheral_data_frames = self._convert_peripheral_tables(
            peripheral_tables,
            sock
        )

        # ------------------------------------------------------------

        # Ensure the targets in listed in the `population` instance
        # variable are corresponding to columns in the povided
        # pandas.DataFrame - in case this class of input was used.
        if type(population_table) is data.DataFrame:
            targets = []
        else:
            targets = [
                elem for elem in self.population.targets
                if elem in population_table.columns
            ]

        # Ensure `population_table` is of type
        # getml.data.DataFrame. In case it is of type
        # pandas.DataFrame instead, it will be converted.
        population_data_frame = self._convert_population_table(
            population_table,
            targets,
            sock
        )

        # ------------------------------------------------------------

        # Get features as numpy array
        yhat = self._transform(
            peripheral_data_frames, 
            population_data_frame, 
            sock,
            predict=True,
            score=True
        )

        # ------------------------------------------------------------
        
        # Get targets.
        colname = population_data_frame.target_names[self.target_num]

        y = population_data_frame[colname].to_numpy(sock).ravel()

        # ------------------------------------------------------------
        
        # Tell the engine the scoring is completed and we are about to
        # close the connection (not done within the _close method).

        self._close(sock)

        # ------------------------------------------------------------

        # Close the connection to the engine.
        sock.close()

        # ------------------------------------------------------------
        
        # Do the actual scoring.
        scores = self._score(yhat, y)

        # ------------------------------------------------------------

        # Tell the engine (in a fresh connection established within
        # _save) to write a copy of the model held in memory to disk.
        self._save()

	# ------------------------------------------------------------
        
        # Remove the trailing underscore from the key names.
        scores_formatted = dict()
        
        for sscore in scores:

            if sscore[len(sscore) - 1] != "_":
                raise ValueError("All scores are expected to have a trailing underscore.")

            scores_formatted[sscore[:len(sscore) - 1]] = scores[sscore]
	
        # ------------------------------------------------------------
        
        return scores_formatted

        # ------------------------------------------------------------

    def send(self):
        """Creates a model in the getML engine.

        Serializes the handler with all information provided either
        via the :meth:`~getml.models.RelboostModel.__init__` method,
        by :func:`~getml.models.load_model`, or by manually altering
        the instance variables. These will be sent to the engine,
        which constructs a new model based on them.

        Raises:
            TypeError: If the `population` instance variables is not
                of type :class:`~getml.data.Placeholder` and
                `peripheral` is not a list of these.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.RelboostModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.RelboostModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.RelboostModel.validate`).

        Returns:
            :class:`~getml.models.RelboostModel`:
                Current instance

        Note:

            If there is already a model with the same ``name``
            attribute is present in the getML engine, it will be
            replaced. Therefore, when calling the
            :meth:`~getml.models.RelboostModel.send` method *after*
            :meth:`~getml.models.RelboostModel.fit` all fit results
            (and calculated scores) will be discarded too and the
            model has to be refitted.

            Imagine you run the following command

            .. code-block:: python

                model.fit(
                    population_table = population_table, 
                    peripheral_tables = peripheral_table)

                model.send()

            Is it possible to undo the changes resulting from calling
            :meth:`~getml.models.RelboostModel.send`?

            The discarding of the old model just happens in memory
            since the :meth:`~getml.models.RelboostModel.send` does
            not trigger the :meth:`~getml.models.RelboostModel._save`
            method and thus does not write the new model to
            disk. These in-memory changes can be undone by using
            :func:`~getml.engine.set_project` to switch to a different
            project and right back to the current one. Since the
            loading of a project is accomplished by reading all
            corresponding objects written to disk, we have restored
            the fitted model.

        """

        # -------------------------------------------
        
        if type(self.population) is not Placeholder:
            raise TypeError("'population' must be a valid data.Placeholder!")

        # `peripheral` is allowed to be either an empty list or a list
        # of placeholder.
        if type(self.peripheral) is not list or not (len(self.peripheral) == 0 or all([type(ll) is Placeholder for ll in self.peripheral])):
            raise TypeError("'peripheral' must be an empty list or a list of getml.data.Placeholder")
        
        # ------------------------------------------------------------
        
        self.validate()

	# ------------------------------------------------------------
	
        # The command will be the serialized version of the model.
        cmd = dict()
        
        # For historical reasons the engine expects most of the
        # parameters to be part of a dict called 'hyperparameters'.
        hyperparameterDict = dict()

	# ------------------------------------------------------------
        
        # A trailing underscore has to be added to all scores in order
        # for the engine to process them correctly.
        for kkey in self.__dict__:
            
            if kkey == "population":
                # The Placeholder of the Python API combines two
                # objects: the schema describing the structure of a
                # particular table and the actual placeholder defining
                # the relations between different tables. They have to
                # be splitted in order for the engine to process them
                # properly. This will be done by creating two new
                # Placeholder holding only the relevant information.
                
                population = self.__dict__[kkey]

                population_schema = Placeholder(
                    name = population.name,
                    categorical = population.categorical,
                    numerical = population.numerical,
                    join_keys = population.join_keys,
                    time_stamps = population.time_stamps,
                    targets = population.targets
                )
                
                population_placeholder = Placeholder(
                    name = population.name
                )
                population_placeholder.set_relations(
                    join_keys_used = population.join_keys_used,
                    other_join_keys_used = population.other_join_keys_used,
                    time_stamps_used = population.time_stamps_used,
                    other_time_stamps_used = population.other_time_stamps_used,
                    upper_time_stamps_used = population.upper_time_stamps_used,
                    joined_tables = population.joined_tables
                )
                
	        # ----------------------------------------------------
	
                cmd["placeholder_"] = population_placeholder
                cmd["population_schema_"] = population_schema
                
	        # ----------------------------------------------------
                
            elif kkey == "peripheral":
                # Only a list of all names of the peripheral tables
                # and not the placeholders themselves will be
                # transmitted. Apart from this the same comment as for
                # population applies.
                
                peripheral = self.__dict__[kkey]
                peripheral_schema = []
                peripheral_placeholder = []
                
                for pperipheral in peripheral:

                    peripheral_schema.append(
                        Placeholder(
                            name = pperipheral.name,
                            categorical = pperipheral.categorical,
                            numerical = pperipheral.numerical,
                            join_keys = pperipheral.join_keys,
                            time_stamps = pperipheral.time_stamps,
                            targets = pperipheral.targets
                        )
                    )
                
                    peripheral_placeholder.append(pperipheral.name)
                
	        # ----------------------------------------------------

                cmd["peripheral_"] = peripheral_placeholder
                cmd["peripheral_schema_"] = peripheral_schema
                
	        # ----------------------------------------------------
                
            elif kkey in ["name", "type"]:
                # Some variables can be written directly
                cmd[kkey+"_"] = self.__dict__[kkey]
        
                # ----------------------------------------------------
                
            elif kkey == "seed":
                # Replace the seed with a numerical value (what is
                # exported by the engine).
                if self.seed is None:
                    hyperparameterDict[kkey+"_"] = 5543
                else:
                    hyperparameterDict[kkey+"_"] = self.seed
                
            else:
                # All others have to be written to a separate dict
                # instead.
                hyperparameterDict[kkey+"_"] = self.__dict__[kkey]

	# ------------------------------------------------------------
		        
        cmd["hyperparameters_"] = hyperparameterDict
        
	# ------------------------------------------------------------
        
        comm.send(cmd)

        # ------------------------------------------------------------

        return self

    # ----------------------------------------------------------------
        
    def to_sql(self):
        """Returns SQL statements visualizing the trained features.

        In order to get insights into the complex features, 
        they are expressed as SQL statements.

        Examples:

            .. code-block:: python

                print(model.to_sql())

        Raises:
            IOError: If the model corresponding to the instance
                variable ``name`` could not be found on the engine or
                the model could not be fitted.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.RelboostModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.RelboostModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.RelboostModel.validate`).

        Returns:
            str:
                String containing the formatted SQL command.

        Note:

            Only fitted models
            (:meth:`~getml.models.RelboostModel.fit`) do hold trained
            features which can be returned as SQL statements.

            In order to display the returned string properly, it has
            to be pretty printed first using the :py:func:`print`
            function.

            The dialect is based on SQLite3 but not guaranteed to be
            fully compliant with its standard.

        """

        # ------------------------------------------------------------
        # Build and send JSON command
        
        # ------------------------------------------------------------
        
        self.validate()
        
        # ------------------------------------------------------------
        
        cmd = dict()
        cmd["type_"] = self.type+".to_sql"
        cmd["name_"] = self.name

        s = comm.send_and_receive_socket(cmd)

        # ------------------------------------------------------------
        # Make sure model exists on getML engine

        msg = comm.recv_string(s)

        if msg != "Found!":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------
        # Receive SQL code from getML engine

        sql = comm.recv_string(s)

        # ------------------------------------------------------------

        s.close()

        return sql

    # ----------------------------------------------------------------

    def transform(
        self,
        population_table,
        peripheral_tables,
        df_name="", 
        table_name=""
    ):
        """Translates new data into the trained features.

        Transforms the data provided in `population_table` and
        `peripheral_tables` into features, which can be used to drive
        machine learning models. In addition to returning them as
        numerical array, this method is also able to write the results
        in a data base called `table_name`.

        Examples:

            .. code-block:: python

                model.transform(
                    population_table = population_table,
                    peripheral_tables = peripheral_table)

        Args:  
            population_table (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`]):
                Main table corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable. Its target variable(s) will be ignored.
            peripheral_tables (Union[:class:`pandas.DataFrame`, :class:`getml.data.DataFrame`, List[:class:`pandas.DataFrame`],List[:class:`getml.data.DataFrame`]]):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. They have to be provided in the exact same
                order as their corresponding placeholders! A single
                DataFrame will be wrapped into a list internally.
            df_name (str, optional): 
                If not an empty string, the resulting features will be
                written into a newly created DataFrame. 
            table_name (str, optional): 
                If not an empty string, the resulting features will be
                written into the :mod:`~getml.database` of the same
                name. See :ref:`unified_import_interface` for further information.

        Raises:
            IOError: If the model corresponding to the instance
                variable ``name`` could not be found on the engine or
                the model could not be fitted.
            TypeError: If any input argument is not of proper type.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.models.RelboostModel.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.models.RelboostModel.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.models.RelboostModel.validate`).

        Return:
            :class:`numpy.ndarray`:
                Resulting features provided in an array of the
                (number of rows in `population_table`, number of
                selected features).
            or :class:`getml.data.DataFrame`:
                A DataFrame containing the resulting features.
        Note:

            Only fitted models
            (:meth:`~getml.models.RelboostModel.fit`) can transform
            data into features.

            If a `population_table` or `peripheral_tables` will be
            provided as :class:`pandas.DataFrame`, they will be
            converted to temporary :class:`getml.data.DataFrame`,
            uploaded to the engine, and discarded after the function
            call. Since `peripheral_tables` can very well be the same
            for the :meth:`~getml.models.RelboostModel.predict`,
            :meth:`~getml.models.RelboostModel.score`, and
            :meth:`~getml.models.RelboostModel.transform` methods,
            this way of interacting with the engine can be highly
            inefficient and is discouraged.

        """

	# ------------------------------------------------------------
        
        # In case a single peripheral table was provided directly, it
        # has to be wrapped into a list.
        if isinstance(peripheral_tables, pd.DataFrame) or isinstance(peripheral_tables, data.DataFrame):
            peripheral_tables = [peripheral_tables]
        
	# ------------------------------------------------------------
	
        if not (isinstance(population_table, data.DataFrame) or isinstance(population_table, pd.DataFrame)):
            raise TypeError("'population_table' must be a getml.data.DataFrame or pandas.data.DataFrame")
        if type(peripheral_tables) is not list or not (len(peripheral_tables) > 0 and all([isinstance(ll, data.DataFrame) or isinstance(ll, pd.DataFrame) for ll in peripheral_tables])):
            raise TypeError("'peripheral_tables' must be a getml.data.DataFrame or pandas.DataFrame or a list of those")
        if type(table_name) is not str:
            raise TypeError("'table_name' must be of type str")
        
        # ------------------------------------------------------------
        
        self.validate()

        # ------------------------------------------------------------

        # Prepare the command for the getML engine.
        cmd = dict()
        cmd["type_"] = self.type+".transform"
        cmd["name_"] = self.name
        cmd["http_request_"] = False

        # ------------------------------------------------------------

        # Send command to engine and make sure that model has
        # been found.
        sock = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            sock.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------
        # Load peripheral tables

        # Ensure all elements in `peripheral_tables` are of type
        # getml.data.DataFrame. All occurrences of type
        # pandas.DataFrame will be converted.
        peripheral_data_frames = self._convert_peripheral_tables(
            peripheral_tables,
            sock
        )

        # ------------------------------------------------------------

        # Ensure the targets in listed in the `population` instance
        # variable are corresponding to columns in the povided
        # pandas.DataFrame - in case this class of input was used.
        if type(population_table) == data.DataFrame:
            targets = []
        else:
            targets = [
                elem for elem in self.population.targets
                if elem in population_table.columns
            ]

        # Ensure `population_table` is of type
        # getml.data.DataFrame. In case it is of type
        # pandas.DataFrame instead, it will be converted.
        population_data_frame = self._convert_population_table(
            population_table,
            targets,
            sock
        )

        # ------------------------------------------------------------
        
        # Get features as numpy array
        y_hat = self._transform(
            peripheral_data_frames, 
            population_data_frame, 
            sock,
            df_name=df_name,
            table_name=table_name
        )

	# ------------------------------------------------------------
	        
        # Tell the engine the prediction is completed and we are about
        # to close the connection (not done within the _close
        # method).
        self._close(sock)

        # ------------------------------------------------------------

        # Close the connection to the engine.
        sock.close()

        # ------------------------------------------------------------
        
        if df_name != "":
            y_hat = data.DataFrame(name=df_name).refresh()
	
        # ------------------------------------------------------------

        return y_hat
    
    # ----------------------------------------------------------------
    
    def validate(self):
        """Checks both the types and the values of all instance 
        variables and raises an exception if something is off.

        Examples:

            .. code-block:: python

                population_table, peripheral_table = getml.datasets.make_numerical()

                population_placeholder = population_table.to_placeholder()
                peripheral_placeholder = peripheral_table.to_placeholder()

                population_placeholder.join(peripheral_placeholder,
                                            join_key = "join_key",
                                            time_stamp = "time_stamp"
                )

                model = getml.models.RelboostModel(
                    population = population_placeholder,
                    peripheral = peripheral_placeholder,
                    name = "relboost"
                )
                model.num_features = 300
                model.shrinkage = 1.7

                model.validate()


        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note: 

            This method is triggered at end of the __init__
            constructor and every time a function communicating with
            the getML engine - except
            :meth:`~getml.models.RelboostModel.refresh` - is called.

            To directly access the validity of single or multiple
            parameters instead of the whole class, you can used
            :func:`getml.helpers.validation.validate_RelboostModel_parameters`.

        """
        
        ## Check for the correct types of the instance variable not
        ## considered to be parameters (which could be altered during
        ## the hyperparameter optimization).
        if type(self.name) is not str:
            raise TypeError("'name' must be of type str")
        if not isinstance(self.population, Placeholder):
            raise TypeError("'population' must be a getml.data.Placeholder or None.")
        if type(self.peripheral) is not list or not (len(self.peripheral) > 0 and all([isinstance(ll, Placeholder) for ll in self.peripheral])):
            raise TypeError("'peripheral' must be either a getml.data.Placeholder or a list of those")
        if not (self.feature_selector is None or isinstance(self.feature_selector, _Predictor)):
            raise TypeError("'feature_selector' must implement getml.predictors._Predictor or None.")
        if not (self.predictor is None or isinstance(self.predictor, _Predictor)):
            raise TypeError("'predictor' must implement getml.predictors._Predictor or None.")
        if type(self.units) is not dict:
            raise TypeError("'units' must be of type dict")
        if type(self.session_name) is not str:
            raise TypeError("'session_name' must be of type str")
        if not isinstance(self.loss_function, _LossFunction):
            raise TypeError("'loss_function' must implement getml.models.loss_functions._LossFunction or None.")
        if type(self.silent) is not bool:
            raise TypeError("'silent' must be of type bool")
        
	# ------------------------------------------------------------

        # Check whether there are additional, unsupported instance
        # variables.
        supported = {'allow_null_weights','delta_t', 'feature_selector', 
                     'gamma', 'include_categorical',
                     'loss_function', 'max_depth', 'min_num_samples',
                     'name', 'num_features', 'num_subfeatures',
                     'num_threads', 'peripheral', 'population',
                     'predictor', 'reg_lambda', 'sampling_factor',
                     'seed', 'session_name',
                     'share_selected_features', 'shrinkage', 'silent',
                     'target_num', 'type', 'units', 'use_timestamps'}
        
        for kkey in self.__dict__:
            if kkey not in supported:
                raise KeyError("Instance variable ["+kkey+"] is not supported in RelboostModel")
        
        # ------------------------------------------------------------
        
        # Check whether the values of the instance variables are
        # correct or (in terms of multiple possible strings or
        # numerical values) plausible.
        if self.type != "RelboostModel":
            raise ValueError("'type' must be 'RelboostModel'")
        if not self.name:
            raise ValueError("'name' must not be empty")

        # ------------------------------------------------------------

        # Check the validity of the hyperparameters.
        _validate_relboost_model_parameters(
            allow_null_weights = self.allow_null_weights,
            delta_t = self.delta_t,
            feature_selector = self.feature_selector,
            gamma = self.gamma,
            include_categorical = self.include_categorical,
            loss_function = self.loss_function,
            max_depth = self.max_depth,
            min_num_samples = self.min_num_samples,
            num_features = self.num_features,
            num_subfeatures = self.num_subfeatures,
            num_threads = self.num_threads,
            predictor = self.predictor,
            reg_lambda = self.reg_lambda,
            sampling_factor = self.sampling_factor,
            seed = self.seed,
            share_selected_features = self.share_selected_features,
            shrinkage = self.shrinkage,
            target_num = self.target_num,
            use_timestamps = self.use_timestamps
        )

        # ------------------------------------------------------------

        # Check for the validity of the stored classes.
        if self.predictor is not None:
            self.predictor.validate()
        if self.feature_selector is not None:
            self.feature_selector.validate()

        # ------------------------------------------------------------

        # Check the consistency of the supplied placeholder.
        # self.peripheral
        # self.population

# --------------------------------------------------------------------
