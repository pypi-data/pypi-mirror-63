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

import json

import getml.communication as comm 
import getml.models as models

from .hyperopt import (
    RandomSearch,
    LatinHypercubeSearch,
    GaussianHyperparameterSearch
)

# --------------------------------------------------------------------

def _decode_hyperopt(rawStr):
    """A custom decoder function for
    :class:`~getml.hyperopt.RandomSearch`,
    :class:`~getml.hyperopt.LatinHypercubeSearch`, and
    :class:`~getml.hyperopt.GaussianHyperparameterSearch`.

    Args:
        rawStr (str): string containing a valid JSON message.

    Raises:
        KeyError: If not all required fields are present in `rawStr`
            to reconstruct a hyperparameter optimization search.
        ValueError: If not all keys in `rawStr` have a trailing
            underscore.
        TypeError: If `rawStr` is not of type :py:class:`dict`.

    Returns: 
        Union[:class:`~getml.hyperopt.RandomSearch`,:class:`~getml.hyperopt.LatinHypercubeSearch`,:class:`~getml.hyperopt.GaussianHyperparameterSearch`]
    """
    
    # ----------------------------------------------------------------
	
    if type(rawStr) is not str:
        raise TypeError("_decode_hyperopt is expecting a str containing a valid JSON as input")
    
    rawDict = json.loads(rawStr)
    
    # ----------------------------------------------------------------

    # Check whether all required fields are present in the dict.
    requiredFields = {'name_', 'param_space_', 'session_name_',
                      'n_iter_', 'ratio_iter_',
                      'optimization_algorithm_',
                      'optimization_burn_in_algorithm_',
                      'optimization_burn_ins_',
                      'seed_',
                      'surrogate_burn_in_algorithm_',
                      'gaussian_kernel_',
                      'gaussian_optimization_algorithm_',
                      'gaussian_optimization_burn_in_algorithm_',
                      'gaussian_optimization_burn_ins_'}

    if set(rawDict.keys()).intersection(requiredFields) != requiredFields:
        raise KeyError("Not enough information contained in the response to reconstruct the hyperparameter optimization: "+str(rawDict.keys()))

    # ----------------------------------------------------------------
    
    # In order to use the keys in the JSON string as input in the
    # constructor of the hyperparameter optimization class, we have to
    # remove their trailing underscores.
    decodingDict = dict()
    
    for kkey in rawDict:

        if kkey[len(kkey) - 1] != "_":
            raise ValueError("All keys in the JSON must have a trailing underscore.")
            
	    # --------------------------------------------------------
	
        elif kkey == "name_":
            # The model field does just contain the name of a model
            # already present in the engine. We will load it
            # (construct a handler for it) and assign it instead.
            
            decodingDict['model'] = models.load_model(rawDict[kkey])
            
	    # --------------------------------------------------------
	
        elif kkey == "param_space_":
            # Remove all trailing underscores from the individual
            # dimensions of the parameter space as well.
            param_space = dict()
            
            for ddimension in rawDict[kkey]:
                param_space[ddimension[:len(ddimension) - 1]] = rawDict[kkey][ddimension]
            
            decodingDict['param_space'] = param_space
            
	    # --------------------------------------------------------
            
        elif kkey in ["peripheral_names_", "population_training_name_", "population_validation_name_"]:
            # Some fields are only interesting for the engine and will
            # not be considered during reconstruction.
            pass
	
        else:
            decodingDict[kkey[:len(kkey) - 1]] = rawDict[kkey]

    # ----------------------------------------------------------------
    
    # Based on the resulting values we have to decide which class to
    # reconstruct. If the requirements of a more specialized class are
    # fulfilled, it is reconstructed instead of the more general one.
    if decodingDict['ratio_iter'] == 1 and decodingDict['surrogate_burn_in_algorithm'] == 'latinHypercube':
        h = LatinHypercubeSearch(model = decodingDict['model'],
                                          param_space = decodingDict['param_space'],
                                          seed = decodingDict['seed'],
                                          session_name = decodingDict['session_name'],
                                          n_iter = decodingDict['n_iter'])
        
    elif decodingDict['ratio_iter'] == 1 and decodingDict['surrogate_burn_in_algorithm'] == 'random':
        h = RandomSearch(model = decodingDict['model'],
                                  param_space = decodingDict['param_space'],
                                  seed = decodingDict['seed'],
                                  session_name = decodingDict['session_name'],
                                  n_iter = decodingDict['n_iter'])
        
    else:
        h = GaussianHyperparameterSearch(model = decodingDict['model'],
                                                  param_space = decodingDict['param_space'],
                                                  session_name = decodingDict['session_name'],
                                                  ratio_iter = decodingDict['ratio_iter'],
                                                  n_iter = decodingDict['n_iter'],
                                                  optimization_algorithm = decodingDict['optimization_algorithm'],
                                                  optimization_burn_in_algorithm = decodingDict['optimization_burn_in_algorithm'],
                                                  optimization_burn_ins = decodingDict['optimization_burn_ins'],
                                                  seed = decodingDict['seed'],
                                                  surrogate_burn_in_algorithm = decodingDict['surrogate_burn_in_algorithm'],
                                                  gaussian_kernel = decodingDict['gaussian_kernel'],
                                                  gaussian_optimization_algorithm = decodingDict['gaussian_optimization_algorithm'],
                                                  gaussian_optimization_burn_in_algorithm = decodingDict['gaussian_optimization_burn_in_algorithm'],
                                                  gaussian_optimization_burn_ins = decodingDict['gaussian_optimization_burn_ins'])
    
    # ----------------------------------------------------------------
    
    # The score is not part of the constructor and will only be
    # assigned after invoking the .fit() method.
    if 'score' in decodingDict:
        h.score = decodingDict['score']
    
    # ----------------------------------------------------------------
    
    return h



# -------------------------------------------------------------------

def load_hyperopt(session_name):
    """Loads a hyperparameter optimization run into the Python API.

    Args:
        session_name (string): Unique identifier of a particular
            hyperparameter optimization run.

    Returns:
        Union[:class:`~getml.hyperopt.RandomSearch`, :class:`~getml.hyperopt.LatinHypercubeSearch`, :class:`~getml.hyperopt.GaussianHyperparameterSearch`]

    Raises:
        IOError: If the messages received from the engine is not a
            valid JSON.
        TypeError: if `session_name` is not a string.
        ValueError: if `session_name` is an empty string.

    """
    
    if type(session_name) is not string:
        raise TypeError("Only strings are allowed as session_name!")
    
    if session_name == '':
        raise ValueError("The session_name must not be empty!")
    
    ## ---------------------------------------------------------------
    
    print("Not supported yet!")
    return
        
    cmd = dict()
    cmd["type_"] = "Hyperopt.load_hyperopt"
    cmd["name_"] = session_name
    
    sock = comm.send_and_receive_socket(cmd)

    # ----------------------------------------------------------------
    
    msg = comm.recv_string(sock)

    # Make sure everything went well and close
    # connection.
    sock.close()
    if msg[0] != '{':
        comm.engine_exception_handler(msg, "Message to load model does not contain a proper JSON: "+msg)

    # ----------------------------------------------------------------
    # Parse results and construct the resulting hyperparameter
    # optimization instance.
    
    h = _decode_hyperopt(msg)
   
    # ------------------------------------------------------------

    # If any of the ML subclasses is set to be multithreaded, the
    # results won't be reproducible and the seed will be
    # disregarded to make this fact transparent to the user.
    multithreaded = False

    if h.model.num_threads > 1:
        multithreaded = True
    if h.model.predictor is not None and (isinstance(h.model.predictor, predictors.XGBoostClassifier) or isinstance(h.model.predictor, predictors.XGBoostRegressor)) and h.model.predictor.n_jobs > 1:
        multithreaded = True
    if h.model.feature_selector is not None and (isinstance(h.model.feature_selector, predictors.XGBoostClassifier) or isinstance(h.model.feature_selector, predictors.XGBoostRegressor)) and h.model.feature_selector.n_jobs > 1:
        multithreaded = True

    if multithreaded:
        h.model.seed = None

