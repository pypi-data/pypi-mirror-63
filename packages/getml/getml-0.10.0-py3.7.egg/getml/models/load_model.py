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

import getml.communication as comm

from getml import predictors

import json

from getml.data import (
        Placeholder,
        _decode_placeholder,
        _decode_joined_tables
)

from .loss_functions import _decode_loss_function
from .multirel_model import MultirelModel
from .relboost_model import RelboostModel

# --------------------------------------------------------------------
	
def load_model(name):
    """Returns a handler for a model in the engine.

    The model has to be held in memory and thus be present in the
    current project. :func:`~getml.models.list_models` can be used to
    list all of them. In order to load a model from a different
    project, you have to switch projects first. See
    :func:`~getml.engine.set_project` and :mod:`~getml.models` for
    more details about the lifecycles of the models.

    Args:
        name (str): Name of a model in the current project.

    Raises:
        KeyError: If the model loaded from the engine is ill-formatted
            (should not be happen. Please report such a problem.)
        IOError: If the response of the engine did not contain a valid
            model.
        TypeError: If `name` is not of type str or its value does not
            correspond to the class name of a model in `getml.models`.

    Returns:
        Union[:class:`~getml.models.MultirelModel`, :class:`~getml.models.RelboostModel`]:
            Handler for the model called `name`.

    """
    
    if type(name) is not str:
        raise TypeError("'name' must be of type str")

    # ----------------------------------------------------------------
    # Obtaining the particular command required to load the model.
    
    cmd_get_model = dict()
    cmd_get_model["type_"] = "get_model"
    cmd_get_model["name_"] = name

    s_get_model = comm.send_and_receive_socket(cmd_get_model)

    msg_get_model = comm.recv_string(s_get_model)

    # Make sure everything went well and close
    # connection.
    s_get_model.close()
    if msg_get_model != "MultirelModel" and msg_get_model != "RelboostModel":
        comm.engine_exception_handler(msg, "Unknown model class: "+msg)
    
    # Constructing the actual loading command.
    cmd_load_model = dict()
    
    if msg_get_model == "MultirelModel":
        cmd_load_model["type_"] = "MultirelModel.refresh"
    else:
        cmd_load_model["type_"] = "RelboostModel.refresh"
        
    cmd_load_model["name_"] = name
        
    # ----------------------------------------------------------------
    # Loading a JSON representing the model.
    
    s_load_model = comm.send_and_receive_socket(cmd_load_model)

    msg_load_model = comm.recv_string(s_load_model)

    # Make sure everything went well and close
    # connection.
    s_load_model.close()
    if msg_load_model[0] != '{':
        comm.engine_exception_handler(msg, "Message to load model does not contain a proper JSON: "+msg)

    # ----------------------------------------------------------------
    # Parse results and construct the resulting model.
    
    json_obj = json.loads(msg_load_model)
    
    # ----------------------------------------------------------------

    if len(json_obj["peripheral_"]) != len(json_obj["peripheral_schema_"]):
        ValueError("Mismatch in the information concerning the peripheral tables")

    # ----------------------------------------------------------------

    # The engine splits of the schema information of the population
    # table in the 'population_schema_' and the relational information
    # in the 'placeholder_' key.
    population = _decode_placeholder(json_obj["population_schema_"])

    # Before assigning the relational information all placeholders in
    # its 'joined_tables_' must be converted to proper
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

    # ----------------------------------------------------------------

    # Since we are dealing with a list of peripheral placeholders and
    # not just a single dict, we have to be careful.
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

    peripheral = peripheral_placeholders

    # ----------------------------------------------------------------
    
    # Construct the baseline model whos parameter will be filled
    # during the remainder of the function.
    if json_obj['type_'] == "MultirelModel":
        model = MultirelModel(name = name,
                              population = population,
                              peripheral = peripheral
        )
    elif json_obj['type_'] == "RelboostModel":
        model = RelboostModel(name = name,
                              population = population,
                              peripheral = peripheral
        )
    else:
        raise KeyError("Unknown model class in loaded model!")
        
    # ----------------------------------------------------------------

    # Assign those parameters defined as fundamental types. All class
    # objects will be reconstructed and assigned afterwards.
    for kkey in json_obj["hyperparameters_"]:

        # Exclude the more complex parameters.
        if kkey not in ['feature_selector_', 'loss_function_', 
                    'peripheral_', 'peripheral_schema_', 
                    'placeholder_', 'population_schema_', 
                    'predictor_']:

            # Remove the trailing underscore in the parameter keys.
            model.__dict__[kkey[:len(kkey) - 1]] = json_obj["hyperparameters_"][kkey]

    # ----------------------------------------------------------------

    if "predictor_" in json_obj["hyperparameters_"]:
        model.predictor = predictors._decode_predictor(json_obj["hyperparameters_"]["predictor_"])

    # ----------------------------------------------------------------

    if "feature_selector_" in json_obj["hyperparameters_"]:
        model.feature_selector = predictors._decode_predictor(json_obj["hyperparameters_"]["feature_selector_"])

    # ----------------------------------------------------------------

    model.loss_function = _decode_loss_function(json_obj["hyperparameters_"]["loss_function_"])
        
    # ----------------------------------------------------------------

    # If any of the ML subclasses is set to be multithreaded, the
    # results won't be reproducible and the seed will be disregarded
    # to make this fact transparent to the user.
    multithreaded = False

    if model.num_threads > 1:
        multithreaded = True
    if model.predictor is not None and (isinstance(model.predictor, predictors.XGBoostClassifier) or isinstance(model.predictor, predictors.XGBoostRegressor)) and model.predictor.n_jobs > 1:
        multithreaded = True
    if model.feature_selector is not None and (isinstance(model.feature_selector, predictors.XGBoostClassifier) or isinstance(model.feature_selector, predictors.XGBoostRegressor)) and model.feature_selector.n_jobs > 1:
        multithreaded = True

    if multithreaded:
        model.seed = None


    # ----------------------------------------------------------------    
	
    return model

# --------------------------------------------------------------------
