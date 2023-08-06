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
import warnings

import numpy as np

import getml.communication as comm

from getml import (
    data,
    engine,
    models,
    predictors
)

from getml.models import loss_functions

from getml.models.validation import (
   _validate_multirel_model_parameters,
   _validate_relboost_model_parameters
)

from getml.predictors import (
    _validate_linear_model_parameters,
    _validate_xgboost_parameters
)

from .validation import _validate_hyperopt_parameters

# -------------------------------------------------------------------

class _BaseSearch(object):
    """
    Base class - not meant to be called by the user.
    """
    
    def __init__(self, model, param_space=None):
        
        # Type checking did already take place in the
        # reimplementations of the __init__ methods of the child
        # classes.
        
        # -----------------------------------------------------------
        
        # Set default parameters. They will be overwritten by the
        # child implementation of __init__ using the user input later
        # on.
        self.n_iter = 100 # consistent naming with respect to sklearn
        self.ratio_iter = 0.75 # how much percent (relative) will be used for the burn-in.
        self.optimization_algorithm = 'nelderMead'
        self.optimization_burn_in_algorithm = 'latinHypercube'
        self.optimization_burn_ins = 15
        self.seed = int(datetime.datetime.now().timestamp()*100)
        self.surrogate_burn_in_algorithm = 'latinHypercube'
        self.gaussian_kernel = 'matern52'
        self.gaussian_optimization_algorithm = 'nelderMead'
        self.gaussian_optimization_burn_in_algorithm = 'latinHypercube'
        self.gaussian_optimization_burn_ins = 50
        
	# ------------------------------------------------------------
        
        # Only fall back to use a default parameter space in case it
        # was not provided by the user.
        use_default_param_space = False
        
        if param_space is None:
            use_default_param_space = True
            # Load the model-dependent default parameters and
            # overwrite them with proper parameters provided by the
            # user.
            if isinstance(model, models.MultirelModel):
                param_space = self._default_param_space_Multirel()
                
            else:
                param_space = self._default_param_space_Relboost()

	# ------------------------------------------------------------
        
        self.model = model
        if isinstance(model, models.MultirelModel):
            self.model_type = 'Multirel'
            
        else:
            self.model_type = 'Relboost'
            
        # -----------------------------------------------------------
        
        # It is possible to use a model without a predictor to just
        # build features. This scenario is incompatible with the
        # hyperparameter optimization and has to be asserted.
        if model.predictor is None:
            raise ValueError("No predictor present in supplied model")
        
        # -----------------------------------------------------------
        
        # In case the user did not provided a parameter space, also
        # get the default one for the chosen predictor.
        if use_default_param_space:
            if isinstance(model.predictor, predictors.LinearRegression):
                param_space.update(
                    self._default_param_space_LinearRegression())
            elif isinstance(model.predictor, predictors.LogisticRegression):
                param_space.update(
                    self._default_param_space_LogisticRegression())
            elif isinstance(model.predictor, predictors.XGBoostClassifier) or isinstance(model.predictor, predictors.XGBoostRegressor):
                param_space.update(
                    self._default_param_space_XGBoost())
            else:
                raise TypeError("Unknown type of predictor")

        # -----------------------------------------------------------
        
        self.param_space = param_space
        
    # ----------------------------------------------------------------

    def __eq__(self, other):
        """Compares the current instance with another one by converting them
        both to strings and compare them byte by byte.
        """
        if not isinstance(other, _BaseSearch):
            raise TypeError("A hyperparameter optimization run can only be compared to another hyperparameter optimization run")

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
	
        for kkey, vvalue in self.__dict__.items():
            
            # --------------------------------------------------------
            # Some of the fields need special treatment
        
            if kkey == "model":

                result += indent1 + "model:\n"
                result += indent2 + str(self.model).replace("\n", "\n" + indent2) + "\n"

                # ----------------------------------------------------

            elif kkey == "param_space":

                result += "\n" + indent1 + "param_space (dict):"

                for kkey, vvalue in self.param_space.items():
                    result += "\n" + indent2 + kkey + ": " + str(vvalue)
                    
	        # ----------------------------------------------------
                
            else:
                result += "\n" + indent1 + kkey + ": " + str(vvalue)
                
	# ------------------------------------------------------------
	
        return result

    # -----------------------------------------------------------
        
    def _default_param_space_Multirel(self):

        """Default parameter space for optimizing the
        :class:`~getml.models.MultirelModel`.

        Returns:
            dict: 
                Default parameter space for optimizing the Multirel
                model.

        """
        
        param_space = {
            'grid_factor': [1.0, 16.0],
            'max_length': [1, 10],
            'min_num_samples': [100, 500],
            'num_features': [10, 500],
            'regularization': [0.0, 0.01],
            'share_aggregations': [0.01, 1.0],
            'share_selected_features': [0.1, 1.0],
            'shrinkage': [0.01, 0.4]
        }
        
        # -----------------------------------------------------------
        
        return param_space

    # ---------------------------------------------------------------
    
    def _default_param_space_LinearRegression(self):
        """Default parameter space for the
        :class:`~getml.predictors.LinearRegression`.

        Returns:
            dict: 
                Default parameter space for
                :class:`~getml.predictors.LinearRegression` predictor.

        """
        param_space = {
            'predictor_learning_rate': [0.5, 1.0],
            'predictor_lambda': [0.0, 1.0]
        }
        
        # -----------------------------------------------------------
        
        return param_space

    # ---------------------------------------------------------------
    
    def _default_param_space_LogisticRegression(self):
        """Default parameter space for the
        :class:`~getml.predictors.LogisticRegression`.

        Returns:
            dict: 
                Default parameter space for
                :class:`~getml.predictors.LogisticRegression` predictor.

        """
        param_space = {
            'predictor_learning_rate': [0.0, 1.0],
            'predictor_lambda': [0.0, 1.0]
        }
        
        # -----------------------------------------------------------
        
        return param_space
    
    # ---------------------------------------------------------------
    
    def _default_param_space_Relboost(self):
        """Default parameter space for optimizing the Relboost model.
        """
        
        param_space = {
            'max_depth': [1, 10],
            'min_num_samples': [100, 500],
            'num_features': [10, 500],
            'reg_lambda': [0.0, 0.1],
            'share_selected_features': [0.1, 1.0],
            'shrinkage': [0.01, 0.4],
        }
        
        # -----------------------------------------------------------
        
        return param_space 
    
    # ---------------------------------------------------------------
    
    def _default_param_space_XGBoost(self):
        """Default parameter space for
        :class:`~getml.predictors.XGBoostClassifier` and
        :class:`~getml.predictors.XGBoostRegressor`.

        Returns:
            dict:  
                Default parameter space.

        """
        
        param_space = {
            'predictor_n_estimators': [10, 500],
            'predictor_learning_rate': [0.0, 1.0],
            'predictor_max_depth': [3, 15],
            'predictor_reg_lambda': [0.0, 10.0]
        }

        # -----------------------------------------------------------
        
        return param_space

    # -----------------------------------------------------------
    
    def _getml_deserialize(self):

            encodingDict = dict()

            for kkey in self.__dict__:
            
                if kkey == "model":

                    # Don't include the model handler. It's name is sufficient.
                    if isinstance(self.model, models.MultirelModel):
                        encodingDict["type_"] = "MultirelModel.launch_hyperopt"
                    elif isinstance(self.model, models.RelboostModel):
                        encodingDict["type_"] = "RelboostModel.launch_hyperopt"
                    else:
                        raise ValueError("Unknown type of 'model' instance variable. Has to be either models.MultirelModel or models.RelboostModel")

                    encodingDict["name_"] = self.model.name

                elif kkey == "score":

                    # Due to the internal implementation an underscore has
                    # to be added to the score.
                    encodingDict[kkey+"_"] = self.__dict__[kkey]+"_"

                elif kkey == "param_space":

                    # For all keys of the parameters space underscores
                    # have to be added as well.
                    anotherEncodingDict = dict()

                    for aa in self.__dict__[kkey]:
                        anotherEncodingDict[aa+"_"] = self.__dict__[kkey][aa]

                    encodingDict[kkey+"_"] = anotherEncodingDict
        
                    # ------------------------------------------------

                elif kkey == "seed":
                    # Replace the seed with a numerical value (what is
                    # exported by the engine).
                    if self.__dict__[kkey] is None:
                        encodingDict[kkey+"_"] = 5543
                    else:
                        encodingDict[kkey+"_"] = self.__dict__[kkey]
        
                    # ------------------------------------------------

                else:

                    encodingDict[kkey+"_"] = self.__dict__[kkey]
            
            # --------------------------------------------------------
            
            return encodingDict
        
            # --------------------------------------------------------

    # -----------------------------------------------------------
    
    def _validate_colnames(self, names_table1, names_table2, description):
        """Makes sure that the colnames of two tables provided in
        `names_table1` and `names_table2` do match.

        Args:
            names_table1 (list[string]): List of strings specifying a
                set of columns in one table.
            names_table2 (list[string]): List of strings specifying a
                set of columns in another table.
            description (string): Should specify the particular set of
                column to allow for more informative exceptions
                raised.

        Raises:
            ValueError: If the length of `names_table1` and
                `names_table2` do not match.
            ValueError: If one string in `names_table1` is not present
                in `names_table2` or the other way around.

        """

        if len(names_table1) != len(names_table2):
            raise ValueError("Number of " + description + " columns does not match")

        ## Check that all strings in names_table1 are contained in
        ## names_table2.
        for nname in names_table1:
            if nname not in names_table2:
                raise ValueError("Missing column in " + description + ":'" + nname + "'")

        ## Check that all strings in names_table2 are contained in
        ## names_table1.
        for nname in names_table1:
            if nname not in names_table2:
                raise ValueError("Missing column in " + description + ":'" + nname + "'")
            
    # ---------------------------------------------------------------

    def fit(
            self, 
            population_table_training,
            population_table_validation,
            peripheral_tables,
            score=None):
        """Launches the hyperparameter optimization.

        The optimization itself will be done by the getML software and
        this function returns immediately after constructing the
        request and checking whether `population_table_training` and
        `population_table_validation` do hold the same column names
        using :meth:`~getml.hyperopt._BaseSearch._validate_colnames`.
        
        In every iteration of the hyperparameter optimization a new
        set of hyperparameters will be drawn from the `param_space`
        member of the class, those particular parameters will be
        overwritten in the base model and it will be renamed, fitted,
        and scored. How the hyperparameters themselves are drawn
        depends on the particular class of hyperparameter
        optimization.

        The provided :class:`~getml.data.DataFrame`
        `population_table_training`, `population_table_validation` and
        `peripheral_tables` must be consistent with the
        :class:`~getml.engine.Placeholders` provided when constructing
        the base model.

        Args:
            population_table_training(:class:`~getml.data.DataFrame`):
                The population table that models will be trained on.
            population_table_validation(:class:`~getml.data.DataFrame`):
                The population table that models will be evaluated on.
            peripheral_tables(:class:`~getml.data.DataFrame`): The
                peripheral tables used to provide additional
                information for the population tables.
            score (string, optional): The score with respect to whom
                the hyperparameters are going to be optimized.
        
                Possible values for a regression problem are:

                * :const:`~getml.models.scores.rmse`
                * :const:`~getml.models.scores.mae`
                * :const:`~getml.models.scores.rsquared` (default)

                Possible values for a classification problem are:

                * :const:`~getml.models.scores.accuracy`
                * :const:`~getml.models.scores.auc`
                * :const:`~getml.models.scores.cross_entropy` (default)

        Raises:
            TypeError: If any of `population_table_training`,
                `population_table_validation` or `peripheral_tables`
                is not of type :class:`~getml.data.DataFrame`.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.hyperopt._BaseSearch.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.hyperopt._BaseSearch.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.hyperopt._BaseSearch.validate`).

        """

	# ------------------------------------------------------------
        
        # In case a single peripheral table was provided directly, it
        # has to be wrapped into a list.
        if isinstance(peripheral_tables, data.DataFrame):
            peripheral_tables = [peripheral_tables]
            
        # -----------------------------------------------------------
        # Type assertion since Pandas DataFrames are forbidden in
        # here.

        if (type(population_table_training) is not data.DataFrame) or \
           (type(population_table_validation) is not data.DataFrame) or \
           (any(type(pp) is not data.DataFrame for pp in peripheral_tables)):
           raise TypeError("Only data.DataFrame are supported by the hyperparameter search")
       
        if not (score is None or (type(score) is str and score in ['rmse', 'mae', 'rsquared', 'cross_entropy', 'auc', 'accuracy'])):
           raise TypeError("'score' must either be None or one of the following strings: ['rmse', 'mae', 'rsquared', 'cross_entropy', 'auc', 'accuracy']")
       
        if not (isinstance(self.model, models.MultirelModel) or isinstance(self.model, models.RelboostModel)):
            raise TypeError("Unknown model class.")
        
        # ------------------------------------------------------------
        
        self.validate()
        
        # -----------------------------------------------------------
        # Check the colnames
        
        self._validate_colnames(
            population_table_training.target_names, 
            population_table_validation.target_names, 
            "targets"
        )
        
        self._validate_colnames(
            population_table_training.join_key_names, 
            population_table_validation.join_key_names, 
            "join keys"
        )

        self._validate_colnames(
            population_table_training.time_stamp_names, 
            population_table_validation.time_stamp_names, 
            "time stamps"
        )

        self._validate_colnames(
            population_table_training.categorical_names, 
            population_table_validation.categorical_names, 
            "categorical"
        )

        self._validate_colnames(
            population_table_training.numerical_names, 
            population_table_validation.numerical_names, 
            "numerical"
        )

        # ----------------------------------------------------------- 
        # Check the score used during optimization

        if score is not None:
            
            # Check whether the score is compatible with the loss
            # function
            if score in ['rmse', 'mae', 'rsquared'] and isinstance(self.model.loss_function, loss_functions.SquareLoss):
                self.score = score
            elif score in ['auc', 'accuracy', 'cross_entropy'] and isinstance(self.model.loss_function, loss_functions.CrossEntropyLoss):
                self.score = score
            else:
                if isinstance(self.model.loss_function, loss_functions.SquareLoss):
                    raise ValueError("Please use one of the following scores when working with a loss_functions.SquareLoss: ['rmse', 'mae', 'rsquared']")
                else:
                    raise ValueError("Please use one of the following scores when working with a loss_functions.CrossEntropyLoss: ['auc', 'accuracy', 'cross_entropy']")

        elif 'score' not in self.__dict__:
            
            # Get a default score
            if isinstance(self.model.loss_function, loss_functions.SquareLoss):
                score = 'rmse'
            elif isinstance(self.model.loss_function, loss_functions.CrossEntropyLoss):
                score = 'cross_entropy'
            else:
                raise TypeError("Unknown type of loss function")
            
            self.score = score
            
        # Else the score already present in the current instance will
        # be used.
        
        # ----------------------------------------------------------- 
        # Check whether model was already sent to the engine.
        
        # Convert the current instances into a dict, which will be
        # latter used for serialization into JSON.
        cmd = self._getml_deserialize()
        
        # ----------------------------------------------------------- 
        # Send command

        sock = comm.send_and_receive_socket(cmd)
        
        # ----------------------------------------------------------- 
        # Make sure that reference model exists
        
        msg = comm.recv_string(sock)
        
        if msg != "Found!":
            sock.close()
            comm.engine_exception_handler(msg)
        
	# ------------------------------------------------------------
    
        # All data provided as input is assumed to already exists in
        # the engine. Therefore, only the names of the DataFrames will
        # be provided.
        cmd['peripheral_names_'] = [df.name for df in peripheral_tables]
        cmd['population_training_name_'] = population_table_training.name
        cmd['population_validation_name_'] = population_table_validation.name
        
	# ------------------------------------------------------------
        
        comm.send_string(sock, json.dumps(cmd))

        print("Launched hyperparameter optimization...")

        # ------------------------------------------------------------
        # Make sure that the hyperparameter optimization ran through.

        msg = comm.recv_string(sock)
        
        if msg != "Success!":
            sock.close()
            comm.engine_exception_handler(msg)
        
        # ----------------------------------------------------------- 
        # Close the socket connection

        sock.close()

    # ---------------------------------------------------------------
    
    def get_models(self):
        """Get a list of all models fitted during the hyperparameter
        optimization.

        Returns:
            list:  
                List of all models fitted during the hyperparameter
                optimization.

        Raises:
            Exception: If the engine yet reports back that the
                operation was not successful.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.hyperopt._BaseSearch.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.hyperopt._BaseSearch.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.hyperopt._BaseSearch.validate`).

        """
        
        # ------------------------------------------------------------
        
        self.validate()

        # ------------------------------------------------------------
        # Build and send JSON command

        cmd = dict()
        
        if type(self.model) is models.MultirelModel:
            cmd['type_'] = "MultirelModel.get_hyperopt_names"
        elif type(self.model) is models.RelboostModel:
            cmd['type_'] = "RelboostModel.get_hyperopt_names"
        else:
            raise TypeError("Unknown model class.")

        cmd['name_'] = self.session_name

        s = comm.send_and_receive_socket(cmd)

        # ------------------------------------------------------------
        # Make sure everything went well

        msg = comm.recv_string(s)

        if msg != "Success!":
            s.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------
        # Receive scores from getML engine

        names = comm.recv_string(s)

        # ------------------------------------------------------------

        s.close()
        
        # -----------------------------------------------------------
        # Transform names to models
        
        names = json.loads(names)["names_"]

        # -----------------------------------------------------------

        return names

    # ---------------------------------------------------------------
    
    def get_scores(self):
        """Get a dictionary of the score corresponding to all models fitted
        during the hyperparamer optimization.

        Returns:
            dict: 

                All score fitted during the hyperparameter
                optimization. Each field adheres the following scheme:

                .. code-block:: python

                    {"model-name": {"accuracy": [list_of_scores],
                                    "auc": [list_of_scores],
                                    "cross_entropy": [list_of_scores],
                                    "mae": [list_of_scores],
                                    "rmse": [list_of_scores],
                                    "rsquared": [list_of_scores]}

                For more information regarding the scores check out
                :mod:`getml.models.scores` (listed under 'Variables').

        Raises:
            Exception: If the engine yet reports back that the
                operation was not successful.
            KeyError: If an unsupported instance variable is
                encountered (via
                :meth:`~getml.hyperopt._BaseSearch.validate`).
            TypeError: If any instance variable is of wrong type (via
                :meth:`~getml.hyperopt._BaseSearch.validate`).
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical) (via
                :meth:`~getml.hyperopt._BaseSearch.validate`).

        """

        # ------------------------------------------------------------
        
        self.validate()
        
        # ------------------------------------------------------------
        # Build and send JSON command

        cmd = dict()
        
        if type(self.model) is models.MultirelModel:
            cmd['type_'] = "MultirelModel.get_hyperopt_scores"
        elif type(self.model) is models.RelboostModel:
            cmd['type_'] = "RelboostModel.get_hyperopt_scores"
        else:
            raise TypeError("Unknown model class.")

        cmd['name_'] = self.session_name

        s = comm.send_and_receive_socket(cmd)

        # ------------------------------------------------------------
        # Make sure everything went well

        msg = comm.recv_string(s)

        if msg != "Success!":
            s.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------
        # Receive scores from getML engine

        scores = comm.recv_string(s)

        # ------------------------------------------------------------

        s.close()
        
        # ------------------------------------------------------------

        model_scores = json.loads(scores)
        
	# ------------------------------------------------------------
        
        # Remove the trailing underscore from the key names.
        model_scores_formatted = dict()
        for mmodel in model_scores:
            
            scores_formatted = dict()
            
            for sscore in model_scores[mmodel]:
                
                if sscore[len(sscore) - 1] != "_":
                    raise ValueError("All scores are expected to have a trailing underscore.")

                scores_formatted[sscore[:len(sscore) - 1]] = model_scores[mmodel][sscore]
                
            model_scores_formatted[mmodel] = scores_formatted

        # ------------------------------------------------------------
        
        return model_scores_formatted
    
    # ---------------------------------------------------------------
    
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

                feature_selector = getml.predictors.LinearRegression()
                predictor = getml.predictors.XGBoostRegressor()

                m = getml.models.MultirelModel(
                    population = population_placeholder,
                    peripheral = peripheral_placeholder,
                    feature_selector = feature_selector,
                    predictor = predictor,
                    name = "multirel"
                ).send()

                param_space = {
                    'num_features': [80, 150],
                    'regularization': [0.3, 1.0],
                    'shrinkage': [0.1, 0.9]
                }

                g = getml.hyperopt.GaussianHyperparameterSearch(
                    model = m,
                    param_space = param_space,
                    seed = int(datetime.datetime.now().timestamp()*100),
                    session_name = 'test_search'
                )
                g.optimization_burn_ins = 240
                g.model.num_threads = 2

                g.validate()

        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note: 

            This method is called at end of the __init__ constructor
            and every time a method is communicating with
            the getML engine.

            To directly access the validity of single or multiple
            parameters instead of the whole class, you can used
            :func:`getml.helpers.validation.validate_hyperopt_parameters`.
        """

        # ------------------------------------------------------------
        
        # Check the presence of all required instance variables. All
        # others are still important but do have reasonable default
        # values. In the Python API all parameters should be present
        # anyway.
        required = ['model', 'model_type', 'session_name',
                    'param_space', 'n_iter', 'ratio_iter']
        
        for rr in required:
            if rr not in self.__dict__:
                raise KeyError("Instance variable '"+rr+"' must be present")
            
        # General check of the parameters.
        _validate_hyperopt_parameters(self.__dict__)
        
        # -----------------------------------------------------------
        
        # It is possible to use a model without a predictor to just
        # build features. This scenario is incompatible with the
        # hyperparameter optimization (for now) and has to be
        # asserted.
        if self.model.predictor is None:
            raise ValueError("No predictor present in supplied model")
        
        # ------------------------------------------------------------
        
        # Validate the base model
        self.model.validate()
        
	# ------------------------------------------------------------
        
        # Validate the provided parameter space of the model. Since
        # the validation of a Multirel and RelboostModel does involve
        # crosschecking various instance variables, not just the
        # particular parameters of the parameter space but the
        # remaining ones from the base model have to be provided as
        # well. All lower and upper bounds will be checked separately.
        params_lower_bound = dict()
        params_upper_bound = dict()
        
        # All parameters not present in the parameter space will be
        # filled by those of the base model.
        if isinstance(self.model, models.MultirelModel):
            possible_params = { 'grid_factor', 'max_length',
                                'min_num_samples', 'num_features',
                                'regularization', 'sampling_factor',
                                'share_aggregations',
                                'share_selected_features',
                                'shrinkage'}
        else:
            possible_params = { 'max_depth', 'min_num_samples',
                                'num_features', 'reg_lambda',
                                'share_selected_features',
                                'shrinkage'}
            
        for pparam in possible_params:
            if pparam not in self.param_space.keys():
                params_lower_bound[pparam] = self.model.__dict__[pparam]
                params_upper_bound[pparam] = self.model.__dict__[pparam]
            else:
                params_lower_bound[pparam] = self.param_space[pparam][0]
                params_upper_bound[pparam] = self.param_space[pparam][1]
                
        if isinstance(self.model, models.MultirelModel):
            _validate_multirel_model_parameters(
                aggregation = self.model.aggregation,
                allow_sets = self.model.allow_sets,
                delta_t = self.model.delta_t,
                feature_selector = self.model.feature_selector,
                grid_factor = params_lower_bound['min_num_samples'],
                include_categorical = self.model.include_categorical,
                loss_function = self.model.loss_function,
                max_length = params_lower_bound['max_length'],
                min_num_samples = params_lower_bound['min_num_samples'],
                num_features = params_lower_bound['num_features'],
                num_subfeatures = self.model.num_subfeatures,
                num_threads = self.model.num_threads,
                predictor = self.model.predictor,
                regularization = params_lower_bound['regularization'],
                round_robin = self.model.round_robin,
                sampling_factor = params_lower_bound['sampling_factor'],
                seed = self.model.seed,
                share_aggregations = self.model.share_aggregations,
                share_conditions = self.model.share_conditions,
                share_selected_features = params_lower_bound['share_selected_features'],
                shrinkage = params_lower_bound['shrinkage'],
                use_timestamps = self.model.use_timestamps
            )

            _validate_multirel_model_parameters(
                aggregation = self.model.aggregation,
                allow_sets = self.model.allow_sets,
                delta_t = self.model.delta_t,
                feature_selector = self.model.feature_selector,
                grid_factor = params_upper_bound['min_num_samples'],
                include_categorical = self.model.include_categorical,
                loss_function = self.model.loss_function,
                max_length = params_upper_bound['max_length'],
                min_num_samples = params_upper_bound['min_num_samples'],
                num_features = params_upper_bound['num_features'],
                num_subfeatures = self.model.num_subfeatures,
                num_threads = self.model.num_threads,
                predictor = self.model.predictor,
                regularization = params_upper_bound['regularization'],
                round_robin = self.model.round_robin,
                sampling_factor = params_upper_bound['sampling_factor'],
                seed = self.model.seed,
                share_aggregations = self.model.share_aggregations,
                share_conditions = self.model.share_conditions,
                share_selected_features = params_upper_bound['share_selected_features'],
                shrinkage = params_upper_bound['shrinkage'],
                use_timestamps = self.model.use_timestamps
            )
            
            # --------------------------------------------------------
        
        else:
            _validate_relboost_model_parameters(
                allow_null_weights = self.model.allow_null_weights,
                delta_t = self.model.delta_t,
                feature_selector = self.model.feature_selector,
                gamma = self.model.gamma,
                include_categorical = self.model.include_categorical,
                loss_function = self.model.loss_function,
                max_depth = params_lower_bound['max_depth'],
                min_num_samples = self.model.min_num_samples,
                num_features = params_lower_bound['num_features'],
                num_subfeatures = self.model.num_subfeatures,
                num_threads = self.model.num_threads,
                predictor = self.model.predictor,
                reg_lambda = params_lower_bound['reg_lambda'],
                sampling_factor = self.model.sampling_factor,
                seed = self.model.seed,
                share_selected_features = params_lower_bound['share_selected_features'],
                shrinkage = params_lower_bound['shrinkage'],
                target_num = self.model.target_num,
                use_timestamps = self.model.use_timestamps
            )

            _validate_relboost_model_parameters(
                allow_null_weights = self.model.allow_null_weights,
                delta_t = self.model.delta_t,
                feature_selector = self.model.feature_selector,
                gamma = self.model.gamma,
                include_categorical = self.model.include_categorical,
                loss_function = self.model.loss_function,
                max_depth = params_upper_bound['max_depth'],
                min_num_samples = self.model.min_num_samples,
                num_features = params_upper_bound['num_features'],
                num_subfeatures = self.model.num_subfeatures,
                num_threads = self.model.num_threads,
                predictor = self.model.predictor,
                reg_lambda = params_upper_bound['reg_lambda'],
                sampling_factor = self.model.sampling_factor,
                seed = self.model.seed,
                share_selected_features = params_upper_bound['share_selected_features'],
                shrinkage = params_upper_bound['shrinkage'],
                target_num = self.model.target_num,
                use_timestamps = self.model.use_timestamps
            )

        # ------------------------------------------------------------
        
        # Reset the dictionaries
        params_lower_bound = dict()
        params_upper_bound = dict()

        # Beware the convention to name the keys associated with the
        # predictors. They all do carry a 'predictor_' prefix.
        for kkey in self.param_space:
            
            # Select only those parameters belonging to the predictors
            # (allowed to be empty).
            if kkey.rfind('predictor_') == 0:
                
                # In case of the linear models there is some
                # inconsistency between the API and the getML engine
                # we have to take care of.
                if kkey == "predictor_lambda" and (isinstance(self.model.predictor, predictors.LinearRegression) or isinstance(self.model.predictor, predictors.LogisticRegression)):
                    params_lower_bound[kkey.replace('predictor_', 'reg_')] = self.param_space[kkey][0]
                    params_upper_bound[kkey.replace('predictor_', 'reg_')] = self.param_space[kkey][1]
                else:
                    params_lower_bound[kkey.replace('predictor_', '')] = self.param_space[kkey][0]
                    params_upper_bound[kkey.replace('predictor_', '')] = self.param_space[kkey][1]
                    
        # Validate the parameters associated with the predictor.
        if isinstance(self.model.predictor, predictors.LinearRegression) or isinstance(self.model.predictor, predictors.LogisticRegression):
            _validate_linear_model_parameters(params_lower_bound)
            _validate_linear_model_parameters(params_upper_bound)
            
        elif isinstance(self.model.predictor, predictors.XGBoostRegressor) or isinstance(self.model.predictor, predictors.XGBoostClassifier):
            _validate_xgboost_parameters(params_lower_bound)
            _validate_xgboost_parameters(params_upper_bound)
            
	# ------------------------------------------------------------

        if self.seed is not None:
            # If any of the ML subclasses is set to be multithreaded, the
            # results won't be reproducible and the seed will be
            # disregarded to make this fact transparent to the user.
            multithreaded = False

            if self.model.num_threads > 1:
                multithreaded = True
            if self.model.predictor is not None and (isinstance(self.model.predictor, predictors.XGBoostClassifier) or isinstance(self.model.predictor, predictors.XGBoostRegressor)) and self.model.predictor.n_jobs > 1:
                multithreaded = True
            if self.model.feature_selector is not None and (isinstance(self.model.feature_selector, predictors.XGBoostClassifier) or isinstance(self.model.feature_selector, predictors.XGBoostRegressor)) and self.model.feature_selector.n_jobs > 1:
                multithreaded = True

            if multithreaded:
                raise ValueError("'seed' can only be set in a single-threaded context in order to make the calculation reproducible. Please check the model.num_threads, model.predictor.n_jobs (XGBoost) and model.feature_selector.n_jobs (XGBoost) variables. They must all equal 1.")
            
        # ------------------------------------------------------------
        
        return True

# -------------------------------------------------------------------

class RandomSearch(_BaseSearch):
    """Uniformly distributed sampling of the hyperparameters.

    At each iteration a new set of hyperparameters is chosen at random
    by uniformly drawing a random value in between the lower and upper
    bound for each dimension of `param_space` independently.

    Examples:

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

            m = getml.models.MultirelModel(
                population = population_placeholder,
                peripheral = peripheral_placeholder,
                feature_selector = feature_selector,
                predictor = predictor,
                name = "multirel"
            ).send()

            param_space = {
                'num_features': [80, 150],
                'regularization': [0.3, 1.0],
                'shrinkage': [0.1, 0.9]
            }

            r = getml.hyperopt.RandomSearch(
                model = m,
                param_space = param_space,
                seed = int(datetime.datetime.now().timestamp()*100),
                session_name = 'test_search',
                n_iter = 10
            )

            r.fit(
                population_table_training = population_table_training,
                population_table_validation = population_table_validation,
                peripheral_tables = peripheral_table
            )

            r.get_scores()

    Args:
        model (Union[:class:`~getml.models.MultirelModel`, :class:`~getml.models.RelboostModel`]):

            Base model used to derive all models fitted and scored
            during the hyperparameter optimization. Be careful in
            constructing it since only those parameters present in
            `param_space` too will be overwritten. It defines the data
            schema, any hyperparameters that are not optimized, and
            contains the predictor which will - depending on the
            parameter space - will be optimized as well.

        param_space (dict, optional):

            Dictionary containing numerical arrays of length two
            holding the lower and upper bounds of all parameters which
            will be altered in `model` during the hyperparameter
            optimization. To keep a specific parameter fixed, you have
            two options. Either ensure it is not present in
            `param_space` but in `model`, or set both the lower and
            upper bound to the same value. Note that all parameters in
            the :mod:`~getml.models` and :mod:`~getml.predictors` do
            have appropriate default values.

            If `param_space` is None, a default space will be chosen
            depending on the particular `model` and
            `model.predictor`. These default spaces will contain *all*
            parameters supported for the corresponding class and are
            listed below.

            * :class:`~getml.models.MultirelModel`

                .. code-block:: python

                    {
                        'grid_factor': [1.0, 16.0],
                        'max_length': [1, 10],
                        'min_num_samples': [100, 500],
                        'num_features': [10, 500],
                        'regularization': [0.0, 0.01],
                        'share_aggregations': [0.01, 1.0],
                        'share_selected_features': [0.1, 1.0],
                        'shrinkage': [0.01, 0.4]
                    }

            * :class:`~getml.models.RelboostModel`

                .. code-block:: python

                    {
                        'max_depth': [1, 10],
                        'min_num_samples': [100, 500],
                        'num_features': [10, 500],
                        'reg_lambda': [0.0, 0.1],
                        'share_selected_features': [0.1, 1.0],
                        'shrinkage': [0.01, 0.4],
                    }

            * :class:`~getml.predictors.LinearRegression` and :class:`~getml.predictors.LogisticRegression`

                .. code-block:: python

                    {
                        'predictor_learning_rate': [0.5, 1.0],
                        'predictor_lambda': [0.0, 1.0]
                    }

            * :class:`~getml.predictors.XGBoostClassifier` and :class:`~getml.predictors.XGBoostRegressor`

                .. code-block:: python
    
                    {
                        'predictor_n_estimators': [10, 500],
                        'predictor_learning_rate': [0.0, 1.0],
                        'predictor_max_depth': [3, 15],
                        'predictor_reg_lambda': [0.0, 10.0]
                    }

            To distinguish between the parameters belonging to the
            `model` from the ones associated with its predictor, the
            prefix 'predictor\_' has to be added to the latter ones.

        seed (Union[int,None], optional):
    
            Seed used for the random number generator that underlies
            the sampling procedure to make the calculation
            reproducible. Due to nature of the underlying algorithm
            this is only the case if the fit is done without
            multithreading. To reflect this, a `seed` of None does
            represent an unreproducible and is only allowed to be set
            to an actual integer if both ``num_threads`` and
            ``n_jobs`` instance variables of the ``predictor`` and
            ``feature_selector`` in `model` - if they are instances of
            either :class:`~getml.predictors.XGBoostRegressor` or
            :class:`~getml.predictors.XGBoostClassifier` - are set to
            1. Internally, a `seed` of None will be mapped to
            5543. Range: [0, :math:`\\infty`]

        session_name (string, optional): 

            Unique ID which will be both used as prefix for the ``name``
            parameter of all models fitted during the hyperparameter
            optimization and directly inserted into ``session_name``. It
            will be used as a handle to load the constructed class
            from the getML engine.

            If `session_name` is empty, a default one based on the
            current date and time will be created.

            Using a session_name all models trained in the engine
            during the hyperparameter optimization, which are based
            on the provided model, can be identified unambiguously.

        n_iter (int, optional): 

            Number of iterations in the hyperparameter optimization
            and thus the number of parameter combinations to draw and
            evaluate. Range: [1, :math:`\\infty`]

    Raises:
        KeyError: If an unsupported instance variable is
            encountered (via
            :meth:`~getml.hyperopt.RandomSearch.validate`).
        TypeError: If any instance variable is of wrong type (via
            :meth:`~getml.hyperopt.RandomSearch.validate`).
        ValueError: If any instance variable does not match its
            possible choices (string) or is out of the expected
            bounds (numerical) (via
            :meth:`~getml.hyperopt.RandomSearch.validate`).
        ValueError: If not ``predictor`` is present in the provided
            `model`.
        """

    def __init__(self,
                 model,
                 param_space = None,
                 seed = None,
                 session_name = '',
                 n_iter = 30):
	
        super().__init__(
            model = model, param_space = param_space)
        
	# ------------------------------------------------------------

        # Predefined parameters that need to be set for a latin
        # hypercube search.
        self.ratio_iter = 1
        self.surrogate_burn_in_algorithm = 'random'
        
	# ------------------------------------------------------------
        
        # Add parameters provided by the user.
        self.n_iter = n_iter
        self.seed = seed
        
        # -----------------------------------------------------------

        # If an empty string was provided as `session_name`, default
        # to a name based on the current datetime.
        self.session_name = session_name or datetime.datetime.now().isoformat().split(".")[0].replace(':', '-')\
            + "-hyperopt-random" + "-" + self.model_type.lower()
        
	# ------------------------------------------------------------
        
        self.validate()
        
    # ----------------------------------------------------------------

    def __str__(self):
        
        result = "RandomSearch:\n" + super(RandomSearch, self).__str__()
        
	# ------------------------------------------------------------
	
        return result
    
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

                feature_selector = getml.predictors.LinearRegression()
                predictor = getml.predictors.XGBoostRegressor()

                m = getml.models.MultirelModel(
                    population = population_placeholder,
                    peripheral = peripheral_placeholder,
                    feature_selector = feature_selector,
                    predictor = predictor,
                    name = "multirel"
                ).send()

                param_space = {
                    'num_features': [80, 150],
                    'regularization': [0.3, 1.0],
                    'shrinkage': [0.1, 0.9]
                }

                r = getml.hyperopt.RandomSearch(
                    model = m,
                    param_space = param_space,
                    seed = int(datetime.datetime.now().timestamp()*100),
                    session_name = 'test_search'
                )
                r.optimization_burn_ins = 240
                r.model.num_threads = 2

                r.validate()

        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note: 

            This method is called at end of the __init__ constructor
            and every time a method is communicating with
            the getML engine.

            To directly access the validity of single or multiple
            parameters instead of the whole class, you can used
            :func:`getml.helpers.validation.validate_hyperopt_parameters`.
        """
        
        super(RandomSearch, self).validate()
        
        # ------------------------------------------------------------

        # Check some parameters that must be set to specific values in
        # this class.
        if self.ratio_iter != 1:
            raise ValueError("'ratio_iter' must be 1 for RandomSearch")
        if self.surrogate_burn_in_algorithm != 'random':
            raise ValueError("'surrogate_burn_in_algorithm' must be 'random' for RandomSearch")
        
# -------------------------------------------------------------------

class LatinHypercubeSearch(_BaseSearch):
    """Latin hypercube sampling of the hyperparameters.

    Uses a multidimensional, uniform cumulative distribution function
    to drawn the random numbers from. For drawing `n_iter` samples,
    the distribution will be divided in `n_iter`*`n_iter` hypercubes
    of equal size (`n_iter` per dimension). `n_iter` of them will be
    selected in such a way only one per dimension is used and an
    independent and identically-distributed (iid) random number is
    drawn within the boundaries of the hypercube.

    Like in :class:`~getml.hyperopt.RandomSearch` the sampling is
    based on a purely statistical algorithm and does not incorporate
    the results of previous evaluations.

    Examples:

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

            m = getml.models.MultirelModel(
                population = population_placeholder,
                peripheral = peripheral_placeholder,
                feature_selector = feature_selector,
                predictor = predictor,
                name = "multirel"
            ).send()

            param_space = {
                'num_features': [80, 150],
                'regularization': [0.3, 1.0],
                'shrinkage': [0.1, 0.9]
            }

            l = getml.hyperopt.LatinHypercubeSearch(
                model = m,
                param_space = param_space,
                seed = int(datetime.datetime.now().timestamp()*100),
                session_name = 'test_search',
                n_iter = 10
            )

            l.fit(
                population_table_training = population_table_training,
                population_table_validation = population_table_validation,
                peripheral_tables = peripheral_table
            )

            l.get_scores()

    Args:
        model (Union[:class:`~getml.models.MultirelModel`, :class:`~getml.models.RelboostModel`]):

            Base model used to derive all models fitted and scored
            during the hyperparameter optimization. Be careful in
            constructing it since only those parameters present in
            `param_space` too will be overwritten. It defines the data
            schema, any hyperparameters that are not optimized, and
            contains the predictor which will - depending on the
            parameter space - will be optimized as well.

        param_space (dict, optional):

            Dictionary containing numerical arrays of length two
            holding the lower and upper bounds of all parameters which
            will be altered in `model` during the hyperparameter
            optimization. To keep a specific parameter fixed, you have
            two options. Either ensure it is not present in
            `param_space` but in `model`, or set both the lower and
            upper bound to the same value. Note that all parameters in
            the :mod:`~getml.models` and :mod:`~getml.predictors` do
            have appropriate default values.

            If `param_space` is None, a default space will be chosen
            depending on the particular `model` and
            `model.predictor`. These default spaces will contain *all*
            parameters supported for the corresponding class and are
            listed below.

            * :class:`~getml.models.MultirelModel`

                .. code-block:: python

                    {
                        'grid_factor': [1.0, 16.0],
                        'max_length': [1, 10],
                        'min_num_samples': [100, 500],
                        'num_features': [10, 500],
                        'regularization': [0.0, 0.01],
                        'share_aggregations': [0.01, 1.0],
                        'share_selected_features': [0.1, 1.0],
                        'shrinkage': [0.01, 0.4]
                    }

            * :class:`~getml.models.RelboostModel`

                .. code-block:: python

                    {
                        'max_depth': [1, 10],
                        'min_num_samples': [100, 500],
                        'num_features': [10, 500],
                        'reg_lambda': [0.0, 0.1],
                        'share_selected_features': [0.1, 1.0],
                        'shrinkage': [0.01, 0.4],
                    }

            * :class:`~getml.predictors.LinearRegression` and :class:`~getml.predictors.LogisticRegression`

                .. code-block:: python

                    {
                        'predictor_learning_rate': [0.5, 1.0],
                        'predictor_lambda': [0.0, 1.0]
                    }

            * :class:`~getml.predictors.XGBoostClassifier` and :class:`~getml.predictors.XGBoostRegressor`

                .. code-block:: python
    
                    {
                        'predictor_n_estimators': [10, 500],
                        'predictor_learning_rate': [0.0, 1.0],
                        'predictor_max_depth': [3, 15],
                        'predictor_reg_lambda': [0.0, 10.0]
                    }

            To distinguish between the parameters belonging to the
            `model` from the ones associated with its predictor, the
            prefix 'predictor\_' has to be added to the latter ones.

        seed (Union[int,None], optional):
    
            Seed used for the random number generator that underlies
            the sampling procedure to make the calculation
            reproducible. Due to nature of the underlying algorithm
            this is only the case if the fit is done without
            multithreading. To reflect this, a `seed` of None does
            represent an unreproducible and is only allowed to be set
            to an actual integer if both ``num_threads`` and
            ``n_jobs`` instance variables of the ``predictor`` and
            ``feature_selector`` in `model` - if they are instances of
            either :class:`~getml.predictors.XGBoostRegressor` or
            :class:`~getml.predictors.XGBoostClassifier` - are set to
            1. Internally, a `seed` of None will be mapped to
            5543. Range: [0, :math:`\\infty`]

        session_name (string, optional): 

            Unique ID which will be both used as prefix for the ``name``
            parameter of all models fitted during the hyperparameter
            optimization and directly inserted into ``session_name``. It
            will be used as a handle to load the constructed class
            from the getML engine.

            If `session_name` is empty, a default one based on the
            current date and time will be created.

            Using a session_name all models trained in the engine
            during the hyperparameter optimization, which are based
            on the provided model, can be identified unambiguously.

        n_iter (int, optional): 

            Number of iterations in the hyperparameter optimization
            and thus the number of parameter combinations to draw and
            evaluate. Range: [1, :math:`\\infty`]

    Raises:
        KeyError: If an unsupported instance variable is
            encountered (via
            :meth:`~getml.hyperopt.LatinHypercubeSearch.validate`).
        TypeError: If any instance variable is of wrong type (via
            :meth:`~getml.hyperopt.LatinHypercubeSearch.validate`).
        ValueError: If any instance variable does not match its
            possible choices (string) or is out of the expected
            bounds (numerical) (via
            :meth:`~getml.hyperopt.LatinHypercubeSearch.validate`).
        ValueError: If not ``predictor`` is present in the provided
            `model`.
        """
    def __init__(self,
                 model,
                 param_space = None,
                 seed = None,
                 session_name = '',
                 n_iter = 30):
        
	# ------------------------------------------------------------
        
        super().__init__(
            model = model, param_space = param_space)
        
	# ------------------------------------------------------------

        # Predefined parameters that need to be set for a latin
        # hypercube search.
        self.ratio_iter = 1
        self.surrogate_burn_in_algorithm = 'latinHypercube'
        
	# ------------------------------------------------------------
        
        # Add parameters provided by the user.
        self.n_iter = n_iter
        self.seed = seed
        
        # -----------------------------------------------------------

        # If an empty string was provided as `session_name`, default
        # to a name based on the current datetime.
        self.session_name = session_name or datetime.datetime.now().isoformat().split(".")[0].replace(':', '-')\
            + "-hyperopt-latin" + "-" + self.model_type.lower()
        
	# ------------------------------------------------------------
        
        self.validate()
        
    # ----------------------------------------------------------------

    def __str__(self):
        
        result = "LatinHypercubeSearch:\n" + super(LatinHypercubeSearch, self).__str__()
        
	# ------------------------------------------------------------
	
        return result
    
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

                feature_selector = getml.predictors.LinearRegression()
                predictor = getml.predictors.XGBoostRegressor()

                m = getml.models.MultirelModel(
                    population = population_placeholder,
                    peripheral = peripheral_placeholder,
                    feature_selector = feature_selector,
                    predictor = predictor,
                    name = "multirel"
                ).send()

                param_space = {
                    'num_features': [80, 150],
                    'regularization': [0.3, 1.0],
                    'shrinkage': [0.1, 0.9]
                }

                l = getml.hyperopt.LatinHypercubeSearch(
                    model = m,
                    param_space = param_space,
                    seed = int(datetime.datetime.now().timestamp()*100),
                    session_name = 'test_search'
                )
                l.optimization_burn_ins = 240
                l.model.num_threads = 2

                l.validate()

        Raises:
            KeyError: If an unsupported instance variable is
                encountered.
            TypeError: If any instance variable is of wrong type.
            ValueError: If any instance variable does not match its
                possible choices (string) or is out of the expected
                bounds (numerical).

        Note: 

            This method is called at end of the __init__ constructor
            and every time a method is communicating with
            the getML engine.

            To directly access the validity of single or multiple
            parameters instead of the whole class, you can used
            :func:`getml.helpers.validation.validate_hyperopt_parameters`.
        """
        
        super(LatinHypercubeSearch, self).validate()
        
        # ------------------------------------------------------------

        # Check some parameters that must be set to specific values in
        # this class.
        if self.ratio_iter != 1:
            raise ValueError("'ratio_iter' must be 1 for LatinHypercubeSearch")
        if self.surrogate_burn_in_algorithm != 'latinHypercube':
            raise ValueError("'surrogate_burn_in_algorithm' must be 'latinHypercube' for LatinHypercubeSearch")

# -------------------------------------------------------------------

class GaussianHyperparameterSearch(_BaseSearch):
    """Bayesian hyperparameter optimization using a Gaussian process.

    In contrast to :class:`~getml.hyperopt.LatinHypercubeSearch` and
    :class:`~getml.hyperopt.RandomSearch` the Bayesian hyperparameter search is
    not a purely statistical algorithm. After a burn-in period (purely
    statistically), a Gaussian process is used to pick the most promising
    parameter combination to be evaluated next based on the knowledge gathered
    throughout previous evaluations. Accessing the quality of potential
    combinations will be done using the expected information (EI).

    Examples:

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

            m = getml.models.MultirelModel(
                population = population_placeholder,
                peripheral = peripheral_placeholder,
                feature_selector = feature_selector,
                predictor = predictor,
                name = "multirel"
            ).send()

            param_space = {
                'num_features': [80, 150],
                'regularization': [0.3, 1.0],
                'shrinkage': [0.1, 0.9]
            }

            g = getml.hyperopt.GaussianHyperparameterSearch(
                model = m,
                param_space = param_space,
                seed = int(datetime.datetime.now().timestamp()*100),
                session_name = 'test_search',
                n_iter = 45
            )

            g.fit(
                population_table_training = population_table_training,
                population_table_validation = population_table_validation,
                peripheral_tables = peripheral_table
            )

            g.get_scores()

    Args:
        model (Union[:class:`~getml.models.MultirelModel`, :class:`~getml.models.RelboostModel`]):

            Base model used to derive all models fitted and scored
            during the hyperparameter optimization. Be careful in
            constructing it since only those parameters present in
            `param_space` too will be overwritten. It defines the data
            schema, any hyperparameters that are not optimized, and
            contains the predictor which will - depending on the
            parameter space - will be optimized as well.

        param_space (dict, optional):

            Dictionary containing numerical arrays of length two
            holding the lower and upper bounds of all parameters which
            will be altered in `model` during the hyperparameter
            optimization. To keep a specific parameter fixed, you have
            two options. Either ensure it is not present in
            `param_space` but in `model`, or set both the lower and
            upper bound to the same value. Note that all parameters in
            the :mod:`~getml.models` and :mod:`~getml.predictors` do
            have appropriate default values.

            If `param_space` is None, a default space will be chosen
            depending on the particular `model` and
            `model.predictor`. These default spaces will contain *all*
            parameters supported for the corresponding class and are
            listed below.

            * :class:`~getml.models.MultirelModel`

                .. code-block:: python

                    {
                        'grid_factor': [1.0, 16.0],
                        'max_length': [1, 10],
                        'min_num_samples': [100, 500],
                        'num_features': [10, 500],
                        'regularization': [0.0, 0.01],
                        'share_aggregations': [0.01, 1.0],
                        'share_selected_features': [0.1, 1.0],
                        'shrinkage': [0.01, 0.4]
                    }

            * :class:`~getml.models.RelboostModel`

                .. code-block:: python

                    {
                        'max_depth': [1, 10],
                        'min_num_samples': [100, 500],
                        'num_features': [10, 500],
                        'reg_lambda': [0.0, 0.1],
                        'share_selected_features': [0.1, 1.0],
                        'shrinkage': [0.01, 0.4],
                    }

            * :class:`~getml.predictors.LinearRegression` and :class:`~getml.predictors.LogisticRegression`

                .. code-block:: python

                    {
                        'predictor_learning_rate': [0.5, 1.0],
                        'predictor_lambda': [0.0, 1.0]
                    }

            * :class:`~getml.predictors.XGBoostClassifier` and :class:`~getml.predictors.XGBoostRegressor`

                .. code-block:: python
    
                    {
                        'predictor_n_estimators': [10, 500],
                        'predictor_learning_rate': [0.0, 1.0],
                        'predictor_max_depth': [3, 15],
                        'predictor_reg_lambda': [0.0, 10.0]
                    }

            To distinguish between the parameters belonging to the
            `model` from the ones associated with its predictor, the
            prefix 'predictor\_' has to be added to the latter ones.

        seed (Union[int,None], optional):
    
            Seed used for the random number generator that underlies
            the sampling procedure to make the calculation
            reproducible. Due to nature of the underlying algorithm
            this is only the case if the fit is done without
            multithreading. To reflect this, a `seed` of None does
            represent an unreproducible and is only allowed to be set
            to an actual integer if both ``num_threads`` and
            ``n_jobs`` instance variables of the ``predictor`` and
            ``feature_selector`` in `model` - if they are instances of
            either :class:`~getml.predictors.XGBoostRegressor` or
            :class:`~getml.predictors.XGBoostClassifier` - are set to
            1. Internally, a `seed` of None will be mapped to
            5543. Range: [0, :math:`\\infty`]

        session_name (string, optional): 

            Unique ID which will be both used as prefix for the ``name``
            parameter of all models fitted during the hyperparameter
            optimization and directly inserted into ``session_name``. It
            will be used as a handle to load the constructed class
            from the getML engine.

            If `session_name` is empty, a default one based on the
            current date and time will be created.

            Using a session_name all models trained in the engine
            during the hyperparameter optimization, which are based
            on the provided model, can be identified unambiguously.

        n_iter (int, optional): 

            Number of iterations in the hyperparameter optimization
            and thus the number of parameter combinations to draw and
            evaluate.
    
            Literature on Gaussian processes suggests to have at least
            10 different evaluations per dimension covered during the
            burn-in. Due to the characteristics of our feature
            engineering algorithms, we found that more relaxed lower
            limit of having `n_iter` - and not just the burn-in phase
            - be at least 10 times the number of dimensions in
            `param_space` still produces desirable results (while
            sticking to the rule of thumb of `ratio_iter`). Range: [4,
            :math:`\\infty`]

        ratio_iter (float, optional): 

            Percentage of the iterations used for the burn-in while
            the remainder will be used in training the Gaussian
            process. For a `ratio_iter` of 1.0 all iterations will be
            spend in the burn-in period resulting in an equivalence of
            this class to
            :class:`~getml.hyperopt.LatinHypercubeSearch` or
            :class:`~getml.hyperopt.RandomSearch` - depending on
            `surrogate_burn_in_algorithm`. Range: [0, 1]

            As a *rule of thumb* at least 70 percent of the evaluation
            should be spent during the burn-in. The more comprehensive
            the exploration of the `param_space` during the burn-in,
            the less likely the Gaussian process to get stuck in bad
            local minima. While the training of the process itself
            uses a trade-off between exploration and exploitation and
            is thus able to escape these minima itself, it could very
            well stick in there for a dozen iterations.

        optimization_algorithm (string, optional): 

            Determines the optimization algorithm used for the local
            search in the optimization of the expected information
            (EI).

            Right now two choices are supported: 'nelderMead', a
            gradient-free downhill simplex method, and 'bfgs', a
            quasi-Newton method relying on both the negative
            log-likelihood and its gradient. We found the 'nelderMead'
            algorithm to work slightly more reliable.

        optimization_burn_in_algorithm (string, optional):

            Specifies the algorithm used to draw initial points in the
            burn-in period of the optimization of the expected
            information (EI).

            For a detailed explanation of the two possible choices -
            'latinHypercube' and 'random' - please have a look in the
            documentation of the
            :class:`~getml.hyperopt.LatinHypercubeSearch` and
            :class:`~getml.hyperopt.RandomSearch` class. In general,
            the 'latinHypercube' is recommended since it more likely
            to resulting in a good coverage of the parameter space.

        optimization_burn_ins (int, optional):

            Number of random evaluation points used during the burn-in
            of the minimization of the expected information (EI).

            After the surrogate model - the Gaussian process - was
            successfully fitted to the previous parameter combination,
            one is able to calculate the EI for a given point. In
            order to now get to the next combination, the EI has to be
            maximized over the whole parameter space. But this problem
            suffers heavily from local minima too. So, we have to
            start the optimization leading to the suggestion of the
            next parameter combination with evaluating the EI at
            various, random points - using
            `optimization_burn_in_algorithm` - and to use a local
            search - specified in `optimization_algorithm` - on the
            best result. Range: [3, :math:`\\infty`]

        surrogate_burn_in_algorithm (string, optional):

            Specifies the algorithm used to draw new parameter
            combinations during the burn-in period.

            For a detailed explanation of the two possible choices -
            'latinHypercube' and 'random' - please have a look in the
            documentation of the
            :class:`~getml.hyperopt.LatinHypercubeSearch` and
            :class:`~getml.hyperopt.RandomSearch` class. In general,
            the 'latinHypercube' is recommended since it more likely
            to resulting in a good coverage of the parameter space.

        gaussian_kernel (string, optional):

            Specifies the 1-dimensional kernel of the Gaussian process
            which will be used along each dimension of the parameter
            space. All of the choices below will result in continuous
            sample paths and their main difference is the degree of
            smoothness of the results with 'exp' yielding the least
            and 'gauss' yielding the most smooth ones.

            * 'exp' 

                A Exponential kernel yielding non-differentiable
                sample paths.

            * 'matern32' 

                A Matérn 3/2 kernel yielding once-differentiable
                sample paths.

            * 'matern52' 

                A Matérn 5/2 kernel yielding twice-differentiable
                sample paths.

            * 'gauss' 

                A Gaussian kernel yielding analytic
                (infinitely--differentiable) sample paths.

        gaussian_optimization_algorithm (string, optional): 

            Determines the optimization algorithm used for the local
            search in the fitting of the Gaussian process to the
            previous parameter combinations.

            Right now two choices are supported: 'nelderMead', a
            gradient-free downhill simplex method, and 'bfgs', a
            quasi-Newton method relying on both the negative
            log-likelihood and its gradient. We found the 'nelderMead'
            algorithm to work slightly more reliable.

        gaussian_optimization_burn_in_algorithm (string, optional):

            Specifies the algorithm used to draw new parameter
            combinations during the burn-in period of the optimization
            of the Gaussian process.

            For a detailed explanation of the two possible choices -
            'latinHypercube' and 'random' - please have a look in the
            documentation of the
            :class:`~getml.hyperopt.LatinHypercubeSearch` and
            :class:`~getml.hyperopt.RandomSearch` class. In general,
            the 'latinHypercube' is recommended since it more likely
            to resulting in a good coverage of the parameter space.

        gaussian_optimization_burn_ins (int, optional):

            Number of random evaluation points used during the burn-in
            of the fitting of the Gaussian process. Range: [3,
            :math:`\\infty`]

    Raises:
        KeyError: If an unsupported instance variable is
            encountered (via
            :meth:`~getml.hyperopt.GaussianHyperparameterSearch.validate`).
        TypeError: If any instance variable is of wrong type (via
            :meth:`~getml.hyperopt.GaussianHyperparameterSearch.validate`).
        ValueError: If any instance variable does not match its
            possible choices (string) or is out of the expected
            bounds (numerical) (via
            :meth:`~getml.hyperopt.GaussianHyperparameterSearch.validate`).
        ValueError: If not ``predictor`` is present in the provided
            `model`.

    Note:

        What's the incentive behind using a Bayesian hyperparameter
        optimization anyway and how does it work?

        Our overall goal is to get the best hyperparameter combination
        in order to perform the best prediction possible. To rephrase
        it in mathematical terms, we want to minimize the negative
        log-likelihood of an objective function representing the
        performance of the feature engineering algorithm, the feature
        selector, and predictor (measured using a particular score)
        given a set of data. But the surface of this negative
        log-likelihood is not convex and contains many local
        minima. We, thus, need to use a global optimization
        scheme. First of all we sample random points in the parameter
        space, evaluate the objective functions at all those sites,
        and, finally, start a well-known and tested local optimization
        routine, e.g. Nelder-Mead, at the best-performing
        combination. The initial point in our parameter space used to
        start the optimization from will be the parameters of the
        provided `model` - either the ones you chose manually or the
        default ones in the :class:`~getml.models.MultirelModel` or
        :class:`~getml.models.RelboostModel` constructors, which we
        will call the base model from here on.

        But on top of having local minima, the objective function has
        a far worse property: it is very expensive to evaluate. Local
        optimization algorithms can easily require over one hundred
        iterations to converge which usually is not an issue
        (e.g. minimizing the negative log-likelihood of a distribution
        function on, let’s say, 1000 data points only takes about 10ms
        on modern computers). But if evaluating the objective function
        involves performing a multi-stage fit of various machine
        learning algorithms to a large amount of data, each iteration
        can take minutes or even longer. In such a scenario even the
        simple task of performing a local minimization very quickly
        becomes computationally infeasible.

        This is where Bayesian hyperparameter optimization enters the
        stage. Its idea is to not fit the negative log-likelihood of
        the objective function directly but, instead, to approximate
        it with a surrogate model - the Gaussian process [Rasmussen06]
        - and to fit the approximation instead. By doing so we trade
        evaluation time - since the surrogate is much more cheap to
        evaluate - in for accuracy - since we are only dealing with an
        approximation of the real objective function.

        The first part of our global optimization scheme (sampling the
        parameter space), becomes a lot more crucial since not just
        the quality of the starting points for the local optimization
        but, even more important, the approximation by the Gaussian
        process does intimately depend on the number and distribution
        of previous evaluations. Without a good coverage of the
        parameter space the Gaussian process will not resemble its
        target properly and the results of the local optimization will
        be poorly.

        Fortunately, we can do better than simply drawing random
        parameter combinations, fitting a single Gaussian process
        afterwards, and returning its minimum. The second core idea of
        the Bayesian hyperparameter optimization is to redesign the
        global optimization for better and more efficient
        performance. The local optimization will be replaced by an
        iterative scheme in which the surrogate is fitted to all
        previous parameter combinations and used to find the most
        promising combination to evaluate next. As a measure of
        quality for the next point to evaluate - also called
        **acquisition function** in the Bayesian optimization
        community - we use the expected information (EI)
        [Villemonteix09]. It measures how much improvement with
        respect to the current minimum of the negative log-likelihood
        function is expected when evaluating a particular additional
        point given all previous evaluations. An immense benefit of
        using the maximum of the EI (or other acquisition functions)
        calculated for the Gaussian process over the raw minimum of
        the surrogate is that they provide a trade-off between
        exploration and exploitation of the parameter space and are
        thus able to efficiently fit the objective function "on their
        own". The EI itself we also have to optimize using a global
        scheme throughout the whole parameter space. But since this is
        done on top of the Gaussian process, it is quite fast.

        To summarize, the optimization starts by drawing a number of
        points within the parameter space at random and using them to
        fit and score the model. Next, a Gaussian process is fitted to
        all parameter combinations/calculated score pairs. Using it
        the most likely position of the optimal parameter combination
        can be determined by optimizing the EI. The model
        corresponding to this combination is fitted and scored by the
        getML engine and, again, a Gaussian process is fitted to all
        evaluations. This procedure will be continued until the
        maximum number of iterations `n_iter` is reached. As a result
        you get a list of all fitted variants of the base `model` as
        well as their calculated scores. Note, however, that the final
        parameter combination calculated based on the models in the
        provided list will not be returned. Since the EI is a
        trade-off between exploration and exploitation, the last
        combination does not have to be the optimal one and we only
        keep those models we know the performance (score) of.

        The algorithm occasionally does evaluate quite a number of
        evaluations (sometimes several dozen) in what appears to be
        the global minimum while in reality it got stuck in a local
        one. The possibility for such an event to happen is
        particularly high for high-dimensional spaces or/and too short
        burn-in periods. In time the algorithm will be able to escape
        the local minima and approach the global one. But instead of
        increasing the number of surrogate evaluation, we recommend to
        perform a more thorough burn-in period instead.

    References:

        - `Carl Edward Rasmussen and Christopher K. I. Williams, MIT
          Press, 2006 <http://www.gaussianprocess.org/gpml/>`_

        - `Julien Villemonteix, Emmanuel Vazquez, and Eric Walter, 2009
          <https://arxiv.org/pdf/cs/0611143.pdf>`_

    """
    
    def __init__(self, 
                 model, 
                 param_space = None, 
                 session_name = '', 
                 n_iter = 100, 
                 ratio_iter = 0.75, 
                 optimization_algorithm = 'nelderMead',
                 optimization_burn_in_algorithm = 'latinHypercube',
                 optimization_burn_ins = 15,
                 seed = None,
                 surrogate_burn_in_algorithm = 'latinHypercube',
                 gaussian_kernel = 'matern52',
                 gaussian_optimization_algorithm = 'nelderMead',
                 gaussian_optimization_burn_in_algorithm = 'latinHypercube',
                 gaussian_optimization_burn_ins = 50):
        
	# ------------------------------------------------------------
        
        super().__init__(
            model = model, param_space = param_space)
        
        ## -----------------------------------------------------------
    
        # Add parameters provided by the user.
        self.n_iter = n_iter
        self.ratio_iter = ratio_iter
        self.optimization_algorithm = optimization_algorithm
        self.optimization_burn_in_algorithm = optimization_burn_in_algorithm
        self.optimization_burn_ins = optimization_burn_ins
        self.seed = seed
        self.surrogate_burn_in_algorithm = surrogate_burn_in_algorithm
        self.gaussian_kernel = gaussian_kernel
        self.gaussian_optimization_algorithm = gaussian_optimization_algorithm
        self.gaussian_optimization_burn_in_algorithm = gaussian_optimization_burn_in_algorithm
        self.gaussian_optimization_burn_ins = gaussian_optimization_burn_ins
        
        # -----------------------------------------------------------

        # If an empty string was provided as `session_name`, default
        # to a name based on the current datetime.
        self.session_name = session_name or datetime.datetime.now().isoformat().split(".")[0].replace(':', '-')\
            + "-hyperopt-gaussian" + "-" + self.model_type.lower()
        
	# ------------------------------------------------------------
        
        self.validate()

    # ----------------------------------------------------------------

    def __str__(self):
        
        result = "GaussianHyperparameterSearch:\n" + super(GaussianHyperparameterSearch, self).__str__()
        
	# ------------------------------------------------------------
	
        return result
