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

# ------------------------------------------------------------------------------

class Placeholder(object):
    """Schematic representation of tables and their relations

    This classes provides a light weight representation of the
    :class:`~getml.data.DataFrame` including both its general
    structure and its relations to other
    :class:`~getml.data.DataFrame`. The actual data, however, is not
    contained.

    Examples:

        Although you can directly use the constructor of
        :class:`~getml.data.Placeholder` to replicate the
        structure of a :class:`~getml.data.DataFrame`, we highly
        recommend to use the
        :meth:`getml.data.DataFrame.to_placeholder` method to generate
        them automatically.

        .. code-block:: python

            # Creates some DataFrames
            population_table, peripheral_table = getml.datasets.make_numerical()

            # Derives Placeholder from them
            population_placeholder = population_table.to_placeholder()
            peripheral_placeholder = peripheral_table.to_placeholder()

        With your :class:`~getml.data.Placeholder` in place you
        can use the :meth:`~getml.data.Placeholder.join` method
        to construct the data model (required to construct the
        :mod:`~getml.models` later on).

        .. code-block:: python

            population_placeholder.join(peripheral_placeholder,
                                        join_key="join_key",
                                        time_stamp="time_stamp"
            )

    Args:
        name (str):

            Name of the corresponding :class:`~getml.data.DataFrame`
            the :class:`~getml.data.Placeholder` is being
            modelled on.

        categorical (List[str], optional):

            Names of the :mod:`~getml.data.columns` of the
            :class:`~getml.data.DataFrame`, which are of role
            :const:`~getml.data.roles.categorical`.

        numerical (List[str], optional):

            Names of the :mod:`~getml.data.columns` of the
            :class:`~getml.data.DataFrame`, which are of role
            :const:`~getml.data.roles.numerical`.

        join_keys (List[str], optional):

            Names of the :mod:`~getml.data.columns` of the
            :class:`~getml.data.DataFrame`, which are of role
            :const:`~getml.data.roles.join_key`.

        time_stamps (List[str], optional):

            Names of the :mod:`~getml.data.columns` of the
            :class:`~getml.data.DataFrame`, which are of role
            :const:`~getml.data.roles.time_stamp`.

        targets (List[str], optional):

            Names of the :mod:`~getml.data.columns` of the
            :class:`~getml.data.DataFrame`, which are of role
            :const:`~getml.data.roles.target`.

    Raises:
        TypeError:
            If any of the input arguments is of wrong type.

    Note:
    
        The input argument `categorical`, `numerical`, `join_keys`,
        `time_stamps`, and `targets` do represent the general
        structure of the corresponding
        :class:`~getml.data.DataFrame`. Its relations to other
        :class:`~getml.data.DataFrame` - stored in the instance
        variables ``join_keys_used``, ``other_join_keys_used``,
        ``time_stamps_used``, ``other_time_stamps_used``,
        ``upper_time_stamps_used``, and ``joined_tables`` - , however,
        are not set using the constructor but in
        :meth:`~getml.data.Placeholder.set_relations`
        method. It will be called internally when invoking
        :meth:`~getml.data.Placeholder.join` and is only
        exported as a public method to allow more sophisticated
        scripting.

    """

    # ----------------------------------------------------------------
    
    _num_placeholders = 0
    """Index keeping track of the number of Placeholders
    constructed. Every call to the `__init__` method will assign a
    unique index to the constructed instance and increment the
    number.
    """
    
    # ----------------------------------------------------------------
	
    def __init__(
        self,
        name,
        categorical=None,
        numerical=None,
        join_keys=None,
        time_stamps=None,
        targets=None
    ):
        
        if categorical is None:
            categorical = []
        if numerical is None:
            numerical = []
        if join_keys is None:
            join_keys = []
        if time_stamps is None:
            time_stamps = []
        if targets is None:
            targets = []
        
	# ------------------------------------------------------------
        
        if type(name) is not str:
            raise TypeError("'name' must be of type str")
        # The following arguments are allowed to be either an empty
        # list or a list of str.
        if type(categorical) != list or not (len(categorical) == 0 or all([type(ll) == str for ll in categorical])):
            raise TypeError("'categorical' must be an empty list or a list of str")
        if type(numerical) != list or not (len(numerical) == 0 or all([type(ll) == str for ll in numerical])):
            raise TypeError("'numerical' must be an empty list or a list of str")
        if type(join_keys) != list or not (len(join_keys) == 0 or all([type(ll) == str for ll in join_keys])):
            raise TypeError("'join_keys' must be an empty list or a list of str")
        if type(targets) != list or not (len(targets) == 0 or all([type(ll) == str for ll in targets])):
            raise TypeError("'targets' must be an empty list or a list of str")
        if type(time_stamps) != list or not (len(time_stamps) == 0 or all([type(ll) == str for ll in time_stamps])):
            raise TypeError("'time_stamps' must be an empty list or a list of str")
        
	# ------------------------------------------------------------
        
        self.name = name
        
        # Column information about the getml.DataFrame the represented
        # by this class instance.
        self.categorical = categorical
        self.numerical = numerical
        self.join_keys = join_keys
        self.targets = targets
        self.time_stamps = time_stamps

        # Column information about all getml.DataFrames joined onto
        # this class instance. Right now it is not possible to
        # initialize a Placeholder with some established joins present
        # yet (to ensure the consistency schema).
        self.join_keys_used = []
        self.other_join_keys_used = []
        self.time_stamps_used = []
        self.other_time_stamps_used = []
        self.upper_time_stamps_used = []
        self.joined_tables = []

        # Unique ID of the placeholder. Will not be included in the
        # print of comparison.
        self.num = Placeholder._num_placeholders

        # Keep track of the global number of placeholders by
        # incrementing a module-level variable.
        Placeholder._num_placeholders += 1

    # ----------------------------------------------------------------

    def __eq__(self, other):
        """Compares the current instance with another one.
        """
        
        if not isinstance(other, Placeholder):
            raise TypeError("A placeholder can only compared to another placeholder!")
        
	# ------------------------------------------------------------
    
        # Check whether both objects have the same number of instance
        # variables.
        if len(set(self.__dict__.keys())) != len(set(other.__dict__.keys())):
            return False
    
	# ------------------------------------------------------------
        
        # Except of `name` all instance variables are lists of
        # strings. As far as I can tell these objects can be compared
        # directly.
        for kkey in self.__dict__:
            
            if kkey not in other.__dict__:
                return False
            
            # Each Placeholder does have a different num value, which
            # is _not_ relevant for comparison (and also not included
            # when converting the Placeholder to string).
            if kkey == "num":
                continue
            
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
	
        result += "Placeholder:"
        
	# ------------------------------------------------------------
        
        for kkey, vvalue in self.__dict__.items():
            
            # --------------------------------------------------------
            # Some of the fields need special treatment 
            
            if kkey == "joined_tables":

                # The peripheral key is a list of Placeholder and does
                # require special care.
                result += "\n" + indent1 + "joined_tables (list):"
                
                
	        # ----------------------------------------------------
	
                if len(vvalue) == 0:
                    result += " []"
                else:
                    for pplaceholder in vvalue:
                        result += "\n" + indent2 + str(pplaceholder).replace("\n", "\n" + indent2)
                    
	        # ----------------------------------------------------
            
            elif kkey == "num":
                
                # This variable is for internal use only and not
                # included in the print or comparison.
                continue
                    
	        # ----------------------------------------------------

            else:
                result += "\n" + indent1 + kkey + ": " + str(vvalue)
        
	# ------------------------------------------------------------
	
        return result

    # ----------------------------------------------------------------
    
    def _getml_deserialize(self):

        # To ensure the getML can handle all keys, we have to add
        # a trailing underscore.
        encodingDict = dict()
        
        for kkey in self.__dict__:
            
            if kkey == "num":
                # Some keys are only used in the Python API and
                # will not be transmitted to the engine.
                continue
            
            #     # ------------------------------------------------
            
            elif kkey in ["categorical", "numerical"]:
                # Due to historical reasons a couple of variables
                # have to have slightly different names in order
                # to be read by the engine.
                encodingDict[kkey+"s_"] = self.__dict__[kkey]
                
                # ------------------------------------------------
    
            else:
                encodingDict[kkey+"_"] = self.__dict__[kkey]
            
        # --------------------------------------------------------
    
        return encodingDict
        
    # ----------------------------------------------------------------
    
    def join(
        self,
        other,
        join_key,
        time_stamp="",
        other_join_key="",
        other_time_stamp="",
        upper_time_stamp="",
    ):

        """Establish a relation between two
        :class:`~getml.data.Placeholder`

        In order for the feature engineering algorithm to craft
        sophisticated features, it has to know about the general
        structure of your relational data at hand. This structure, the
        data model, is composed out of both the schematic
        representations of the involved :class:`~getml.data.DataFrame`
        and their relations to each other. The latter is introduced
        using this method.

        Examples:

            .. code-block:: python

                population_table, peripheral_table = getml.datasets.make_numerical()
                population_placeholder = population_table.to_placeholder()
                peripheral_placeholder = peripheral_table.to_placeholder()

                population_placeholder.join(peripheral_placeholder,
                                            join_key="join_key",
                                            time_stamp="time_stamp"
                )
        
            The example above will construct a data model in which the
            'population_table' depends on the 'peripheral_table' via
            the 'join_key' column. In addition, only those columns in
            'peripheral_table' which 'time_stamp' is small than the
            'time_stamp' in 'population_table' are considered.

        Args:
            other (:class:`~getml.data.Placeholder`):

                :class:`~getml.data.Placeholder` the current
                instance will depend on.

            join_key (str):

                Name of the :class:`~getml.data.columns.StringColumn` in
                the corresponding :class:`~getml.data.DataFrame` used
                to establish a relation between the current instance
                and `other`.

                The provided string must be contained in the
                ``join_keys`` instance variable.

                If `other_join_key` is an empty string, `join_key`
                will be used to determine the column of `other` too.

            time_stamp (str, optional):

                Name of the :class:`~getml.data.columns.FloatColumn` in
                the corresponding :class:`~getml.data.DataFrame` used
                to ensure causality.

                The provided string must be contained in the
                ``time_stamps`` instance variable.

                If `other_time_stamp` is an empty string, `time_stamp`
                will be used to determine the column of `other` too.

            other_join_key (str, optional):

                Name of the :class:`~getml.data.columns.StringColumn` in
                the :class:`~getml.data.DataFrame` represented by
                `other` used to establish a relation between the
                current instance and `other`.

                If an empty string is provided, `join_key` will be
                used instead.

            other_time_stamp (str, optional):

                Name of the :class:`~getml.data.columns.FloatColumn` in
                the :class:`~getml.data.DataFrame` represented by
                `other` used to ensure causality.

                If an empty string is provided, `time_stamp` will be
                used instead.

            upper_time_stamp (str, optional):

                Optional additional time stamp in the `other` that
                will limit the number of joined rows to a certain
                point in the past. This is useful for data with
                limited correlation length.

                Expressed as SQL code, this will add the condition

                .. code-block:: sql
                
                    t1.time_stamp < t2.upper_time_stamp OR
                    t2.upper_time_stamp IS NULL

                to the feature.

                If an empty string is provided, all values in the past
                will be considered.

        Raises:
            TypeError:
                If any of the input arguments is of wrong type.
            Exception:
                If `other` was created earlier (temporally) than the
                current instance.

        Note:

            The task of the `time_stamp` is a crucial one. It ensures
            causality by incorporating only those rows of `other` in
            the join operation for which the time stamp in
            `other_time_stamp` is at most as recent as the one in the
            corresponding row of `time_stamp` in the current
            instance. Since usually it's the population table you call
            this method on and it's the peripheral table you provide
            as `other` (see :ref:`data_model_tables`), this ensures no
            information from the future is considered during
            training. `upper_time_stamp` is used to additionally limit
            the joined rows up to a certain point in the past.

            In terms of SQL syntax this method does correspond to a
            LEFT_JOIN.

            `other` must be created (temporally) after the current
            instance. This was implemented as measure to prevent
            circular dependencies in the data model.

        """

        if not isinstance(other, Placeholder):
            raise TypeError("'other' must be a getml.data.Placeholder!")
        if type(join_key) is not str:
            raise TypeError("'join_key' must be of type str")
        if type(time_stamp) is not str:
            raise TypeError("'time_stamp' must be of type str")
        if type(other_join_key) is not str:
            raise TypeError("'other_join_key' must be of type str")
        if type(other_time_stamp) is not str:
            raise TypeError("'other_time_stamp' must be of type str")
        if type(upper_time_stamp) is not str:
            raise TypeError("'upper_time_stamp' must be of type str")
        
	# ------------------------------------------------------------
	
        if other.num <= self.num:
            raise Exception(
                """You cannot join a placeholder that was created
                before the placeholder it is joined to.
                This is to avoid circular dependencies.
                Please reverse the order in which the placeholders '""" +
                other.name + "' and '" + self.name + "' are created!")

        if time_stamp == "" and other_time_stamp != "":
            raise ValueError("""If time_stamp is an empty string, then"""  
                    """ other_time_stamp must be empty as well.""")

        other_join_key = other_join_key or join_key

        other_time_stamp = other_time_stamp or time_stamp

	# ------------------------------------------------------------
	
        self.join_keys_used.append(join_key)

        self.other_join_keys_used.append(other_join_key)

        self.time_stamps_used.append(time_stamp)

        self.other_time_stamps_used.append(other_time_stamp)

        self.upper_time_stamps_used.append(upper_time_stamp)

        self.joined_tables.append(other)

# --------------------------------------------------------------------

    def set_relations(
            self,
            join_keys_used=None,
            other_join_keys_used=None,
            time_stamps_used=None,
            other_time_stamps_used=None,
            upper_time_stamps_used=None,
            joined_tables=None):
        """Set all relational instance variables not exposed in the
        constructor.

        The reason to split of the setting of the instance variables
        in two different functions, this one and the constructor, is
        due to their distinct nature. While the input arguments of the
        latter are concerned with the structure of the particular
        :class:`~getml.data.DataFrame` the current instance is
        representing, the arguments of this function cover the
        relations of that table to all the other
        :class:`~getml.data.DataFrame`.

        The intended usage during a data science project is to first
        construct the :class:`~getml.data.Placeholder` for all
        :class:`~getml.data.DataFrame` and later on join them
        together/define their relations using
        :meth:`~getml.data.Placeholder.join`. Letting this
        method managing the relational instances variables instead of
        requiring them during the construction of the
        :class:`~getml.data.Placeholder` makes the code much
        less error-prone. But at some points, like in deserialization
        or extended scripting, it might be still required to
        initialize the whole instance in one (well, two) step which is
        where this method comes into play.

        The ordering within the provided arguments is important. It is
        assumed that all of them are of the same length and all
        keys/time stamps at a certain position define the relation of
        the table this instance resembles with another one represented
        by the :class:`~getml.data.Placeholder` in the same
        position of the `joined_tables` argument.

        Args:
            join_keys_used (List[str]): Elements in
                `join_keys` used to define the relations to the other
                tables provided in `joined_tables`. 
            other_join_keys_used (List[str]): `join_keys` of the
                :class:`~getml.data.Placeholder` in
                `joined_tables` used to define a relation with the
                current instance. Note that the `join_keys` instance
                variable is *not* contained in the `joined_tabled`.
            time_stamps_used (List[str]): Elements in `time_stamps` used
                to define the relations to the other tables provided
                in `joined_tables`.
            other_time_stamps_used (List[str]): `time_stamps` of the
                :class:`~getml.data.Placeholder` in
                `joined_tables` used to define a relation with the
                current instance. Note that the `time_stamps` instance
                variable is *not* contained in the `joined_tabled`.
            upper_time_stamps_used (List[str]): `time_stamps` of the
                :class:`~getml.data.Placeholder` in
                `joined_tables` used as 'upper_time_stamp' to define a
                relation with the current instance. For details please
                see the :meth:`~getml.data.Placeholder.join`
                method. Note that the `time_stamps` instance variable
                is *not* contained in the `joined_tabled`.
            joined_tables (List[:class:`~getml.data.Placeholder`]):
                List of all other 
                :class:`~getml.data.Placeholder` the current 
                instance is joined on.

        Raises:
            TypeError: If any of the input arguments is of wrong type.
            ValueError: If the input arguments are not of same length.

        """
        
        # Assign default parameters if None was provided.
        if join_keys_used is None:
            join_keys_used=[]
        if other_join_keys_used is None:
            other_join_keys_used = []
        if time_stamps_used is None:
            time_stamps_used = []
        if other_time_stamps_used is None:
            other_time_stamps_used = []
        if upper_time_stamps_used is None:
            upper_time_stamps_used = []
        if joined_tables is None:
            joined_tables = []
        
	# ------------------------------------------------------------
        
        # Type checking. All arguments must either be empty lists or
        # lists of only a particular type.
        if type(join_keys_used) is not list or not (len(join_keys_used) == 0 or all([type(ll) is str for ll in join_keys_used])):
            raise TypeError("'join_keys_used' must be an empty list or a list of str")
        if type(other_join_keys_used) is not list or not (len(other_join_keys_used) == 0 or all([type(ll) is str for ll in other_join_keys_used])):
            raise TypeError("'other_join_keys_used' must be an empty list or a list of str")
        if type(time_stamps_used) is not list or not (len(time_stamps_used) == 0 or all([type(ll) is str for ll in time_stamps_used])):
            raise TypeError("'time_stamps_used' must be an empty list or a list of str")
        if type(other_time_stamps_used) is not list or not (len(other_time_stamps_used) == 0 or all([type(ll) is str for ll in other_time_stamps_used])):
            raise TypeError("'other_time_stamps_used' must be an empty list or a list of str")
        if type(upper_time_stamps_used) is not list or not (len(upper_time_stamps_used) == 0 or all([type(ll) is str for ll in upper_time_stamps_used])):
            raise TypeError("'upper_time_stamps_used' must be an empty list or a list of str")
        if type(joined_tables) is not list or not (len(joined_tables) == 0 or all([isinstance(ll, Placeholder) for ll in joined_tables])):
            raise TypeError("'joined_tables' must be an empty list or a list of getml.data.Placeholder")
        
	# ------------------------------------------------------------
	
        # Further sanity checking.
        
        # Check whether all provided lists feature the same length.
        if len(set([len(join_keys_used), len(other_join_keys_used), len(time_stamps_used), len(other_time_stamps_used), len(upper_time_stamps_used), len(joined_tables)])) != 1:
            raise ValueError("Mismatching length of the provided lists")

	# ------------------------------------------------------------
	    
        self.join_keys_used = join_keys_used
        self.other_join_keys_used = other_join_keys_used
        self.time_stamps_used = time_stamps_used
        self.other_time_stamps_used = other_time_stamps_used
        self.upper_time_stamps_used = upper_time_stamps_used
        self.joined_tables = joined_tables

# --------------------------------------------------------------------

def _decode_joined_tables(rawList):
    """Recursive helper function to deserialize the
    :class:`~getml.data.Placeholder`.  

    The :class:`~getml.data.Placeholder` is provided by the engine
    in a format like 

    .. code-block:: json

        {"name_": "placebert", "categoricals_": ["cat1", "cat2"],
        "numericals_": [], "join_keys_": ["J1", "J2", "J3"],
        "targets_": [], "time_stamps_": ["t1"], "join_keys_used_":
        ["J1"], "other_join_keys_used_": ["J1"], "time_stamps_used_":
        ["t1"], "other_time_stamps_used_": ["t1"],
        "upper_time_stamps_used_": [""], "joined_tables_": [{"name_":
        "joinbert", "categoricals_": ["jupa1", "jupa2"],
        "numericals_": [], "join_keys_": ["J1"], "targets_": [],
        "time_stamps_": ["t1"], "join_keys_used_": [],
        "other_join_keys_used_": [], "time_stamps_used_": [],
        "other_time_stamps_used_": [], "upper_time_stamps_used_": [],
        "joined_tables_": []}]}

    Note that the "joined_tables_" field consists of a list of other
    :class:`~getml.data.Placeholder`, which themselves can hold
    yet another list of :class:`~getml.data.Placeholder` and so
    on.  Why not using :func:`~getml.data._decode_placeholder` for
    all of them?  Because the it is not intended to be a recursive
    function.

    Providing and empty list as `rawList` will terminate the recursive
    call.

    Args:

        rawList(Union[List[str],List[:class:`~getml.data.Placeholder`): 
            "joined_tables_" field of a serialized
            :class:`~getml.data.Placeholder` or the
            :class:`~getml.data.Placeholder` itself.

    Returns:
        List(:class:`~getml.data.Placeholder`): Deserialized
            version of all placeholders present in `rawList`. If
            `rawList` is empty, the returned list will be empty as
            well.

    Raises:
        TypeError: If `rawList` is not a :py:class:`list`.

    """
    
    if type(rawList) is not list:
        raise TypeError("'rawList' must be a list.")
    
    # ----------------------------------------------------------------
	
    # Criterion exit the recursive decoding.
    if len(rawList) == 0:
        return []
    
    # ----------------------------------------------------------------
    
    placeholderList = list()
	
    for jj in rawList:
        
        if isinstance(jj, Placeholder):
            placeholderList.append(jj)
            
        else:
            pplaceholder = Placeholder(
                name = jj["name_"],
                categorical = jj["categoricals_"],
                numerical = jj["numericals_"],
                join_keys = jj["join_keys_"],
                time_stamps = jj["time_stamps_"],
                targets = jj["targets_"]
            )
            pplaceholder.set_relations(
                join_keys_used = jj["join_keys_used_"],
                other_join_keys_used = jj["other_join_keys_used_"],
                time_stamps_used = jj["time_stamps_used_"],
                other_time_stamps_used = jj["other_time_stamps_used_"],
                upper_time_stamps_used = jj["upper_time_stamps_used_"],
                joined_tables = _decode_joined_tables(jj["joined_tables_"])
            )

            # ------------------------------------------------------------

            placeholderList.append(pplaceholder)

    return placeholderList

# --------------------------------------------------------------------

def _decode_placeholder(rawDict):
    """A custom decoder function for
    :class:`~getml.data.Placeholder`.

    Args:
        rawDict (dict):

            dict naively deserialized from the JSON message provided
            by the getML engine.

    Raises:
        KeyError: If the ``type`` key in `rawDict` is either not present
            or of unknown type.
        ValueError: If not all keys in `rawDict` have a trailing
            underscore.
        TypeError: If `rawDict` is not of type :py:class:`dict`.

    Returns: 
        :class:`~getml.data.Placeholder`

    Examples:

        Create a :class:`~getml.data.Placeholder`, serialize
        it, and deserialize it again.

        .. code-block:: python
        
            p = getml.data.Placeholder(name = "placebert")
            p_serialized = json.dumps(p, cls = getml.communication._GetmlEncoder)
            p2 = json.loads(p_serialized, object_hook = getml.placeholders._decode_placeholder)
            p == p2

    """
    
    # ----------------------------------------------------------------
	
    if type(rawDict) is not dict:
        raise TypeError("_decode_placeholder is expecting a dict as input")

    # ----------------------------------------------------------------
    
    # In order to use the keys in the JSON string as input in the
    # constructor of the placeholder class, we have to remove their
    # trailing underscores.
    decodingDict = dict()
    
    # The relational information will be treated separately and added
    # via the .set_relation method.
    relationDict = dict()
    for kkey in rawDict:

        if kkey[len(kkey) - 1] != "_":
            raise ValueError("All keys in the JSON must have a trailing underscore.")
            
	    # --------------------------------------------------------
	
        elif kkey == "joined_tables_":
            # The joined tables contain proper Placeholder themselves
            # and will be deserialized separately.
            relationDict[kkey[:-1]] = _decode_joined_tables(rawDict[kkey])
            
        elif kkey in ["join_keys_used_", "other_join_keys_used_", "time_stamps_used_", "other_time_stamps_used_", "upper_time_stamps_used_"]:
            relationDict[kkey[:-1]] = rawDict[kkey]

            # --------------------------------------------------------
            
        elif kkey in ["categoricals_", "numericals_"]:
            # Due to historical reasons some of the keys in the engine
            # are inconstistent and have to be adjusted manually in
            # here (in order to provide the same interface to the
            # Placeholder and DataFrames). (a trailing 's' must be
            # replaced too).
            decodingDict[kkey[:-2]] = rawDict[kkey]
	
        else:
            decodingDict[kkey[:-1]] = rawDict[kkey]


    # ----------------------------------------------------------------
    # Temporary fix until the final pipeline is in place
    # TODO: Remove this temporary fix once the final pipeline is there
    
    if "discretes" in decodingDict:
        decodingDict["numerical"] += decodingDict["discretes"]
        del decodingDict["discretes"]
 
    # ----------------------------------------------------------------
    
    p = Placeholder(**decodingDict)
    
    p.set_relations(**relationDict)
    
    # ----------------------------------------------------------------
    
    return p

# --------------------------------------------------------------------
