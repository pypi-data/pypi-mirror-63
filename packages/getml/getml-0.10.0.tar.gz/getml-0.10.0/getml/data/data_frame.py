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

import json
import numbers
import os
import socket

import numpy as np
import pandas as pd

import getml.communication as comm

from .columns import (
    FloatColumn,
    StringColumn,
    _VirtualBooleanColumn,
    _VirtualFloatColumn,
    _VirtualStringColumn 
)

from .helpers import (
    _is_typed_list,
    _is_non_empty_typed_list,
    _is_numerical_type,
    _update_sniffed_roles,
    _sniff_csv,
    _sniff_db,
    _sniff_json,
    _sniff_pandas,
)

from .placeholder import Placeholder

from . import roles

# --------------------------------------------------------------------


class DataFrame(object):
    """Handler for the data stored in the getML engine.

    The :class:`~getml.data.DataFrame` class represents a data frame
    object in the getML engine but does not contain any actual data
    itself. To create such a data frame object, fill it with data via
    the Python API, and to retrieve a handler for it, you can use one
    of the :func:`~getml.data.DataFrame.from_csv`,
    :func:`~getml.data.DataFrame.from_db`,
    :func:`~getml.data.DataFrame.from_json`, or
    :func:`~getml.data.DataFrame.from_pandas` class methods. The
    :ref:`uploading_data` section in the user guide does explain in
    detail particularities of each of those flavors of the unified
    import interface.

    In case the data frame object is already present in the engine -
    either in memory as a temporary object or on disk when
    :meth:`~getml.data.DataFrame.save` was called earlier -, the
    :func:`~getml.data.load_data_frame` function will create a new
    handler without altering the underlying data. For more information
    about the lifecycle of the data in the getML engine and its
    synchronization with the Python API please see the
    :ref:`corresponding user guide<the_getml_python_api_lifecycles>`.

    Args:
        name (str): Unique identifier used to link the handler with
            the underlying data frame object in the engine.

        roles(dict[str, List[str]], optional):

            A dictionary mapping the :mod:`~getml.data.roles` to the
            column names (see :meth:`~getml.data.DataFrame.colnames`).
            
            The `roles` dictionary is expected to have the following format

            .. code-block:: python

                roles = {getml.data.role.numeric: ["colname1", "colname2"], 
                         getml.data.role.target: ["colname3"]}

    Raises:
        TypeError: If any of the input arguments is of wrong type.

        ValueError:
            If one of the provided keys in `roles` does not match a
            definition in :mod:`~getml.data.roles`.

    Examples:

        Creating a new data frame object in the getML engine and uploading
        data is done by one the class functions
        :func:`~getml.data.DataFrame.from_csv`,
        :func:`~getml.data.DataFrame.from_db`,
        :func:`~getml.data.DataFrame.from_json`, or
        :func:`~getml.data.DataFrame.from_pandas`.

        .. code-block:: python

            random = numpy.random.RandomState(7263)

            table = pandas.DataFrame()
            table['column_01'] = random.randint(0, 10, 1000).astype(numpy.str)
            table['join_key'] = numpy.arange(1000)
            table['time_stamp'] = random.rand(1000)
            table['target'] = random.rand(1000)

            df_table = getml.data.DataFrame.from_pandas(table, name = 'table')

        In addition to creating a new data frame object in the getML
        engine and filling it with all the content of `table`, the
        :func:`~getml.data.DataFrame.from_pandas` function does also
        return a :class:`~getml.data.DataFrame` handler to the
        underlying data.

        You don't have to create the data frame objects anew for each
        session. You can use their :meth:`~getml.data.DataFrame.save`
        method to write them to disk, the
        :func:`~getml.data.list_data_frames` function to list all
        available objects in the engine, and
        :func:`~getml.data.load_data_frame` to create a
        :class:`~getml.data.DataFrame` handler for a data set already
        present in the getML engine (see
        :ref:`the_getml_python_api_lifecycles` for details).

        .. code-block:: python

            df_table.save()

            getml.data.list_data_frames()

            df_table_reloaded = getml.data.load_data_frame('table')

    Note:

        Although the Python API does not store the actual data itself,
        you can use the :meth:`~getml.data.DataFrame.to_csv`,
        :meth:`~getml.data.DataFrame.to_db`,
        :meth:`~getml.data.DataFrame.to_json`, and
        :meth:`~getml.data.DataFrame.to_pandas` methods to retrieve
        them.

    """

    _role = roles

    _categorical_roles = [
        roles.categorical,
        roles.join_key,
        roles.unused_string
    ]
    
    _numerical_roles = [
        roles.numerical,
        roles.target,
        roles.time_stamp,
        roles.unused_float
    ]

    _possible_keys = [
        "join_key",
        "time_stamp",
        "categorical",
        "numerical",
        "target",
        "unused_float",
        "unused_string"
    ]

    def __init__(self, name, roles=None):

        # ------------------------------------------------------------
       
        roles = roles or dict()

        if type(name) is not str:
            raise TypeError("'name' must be str.")
        
        if type(roles) is not dict:
            raise TypeError("'roles' must be dict.")
        
        # ------------------------------------------------------------

        self.name = name
         
        # ------------------------------------------------------------
        
        if "join_key" in roles:
            join_keys = roles["join_key"]
        else:
            join_keys = []

        if "time_stamp" in roles:
            time_stamps = roles["time_stamp"]
        else:
            time_stamps = []

        if "categorical" in roles:
            categorical = roles["categorical"]
        else:
            categorical = []

        if "numerical" in roles:
            numerical = roles["numerical"]
        else:
            numerical = []
         
        if "target" in roles:
            targets = roles["target"]
        else:
            targets = []
        
        if "unused_float" in roles:
            unused_floats = roles["unused_float"]
        else:
            unused_floats = []
         
        if "unused_string" in roles:
            unused_strings = roles["unused_string"]
        else:
            unused_strings = []
            
        # ------------------------------------------------------------
        
        if not _is_typed_list(join_keys, str):
            raise TypeError("'join_key' must be None, an empty list, or a list of str.")
        
        if not _is_typed_list(time_stamps, str):
            raise TypeError("'time_stamp' must be None, an empty list, or a list of str.")
        
        if not _is_typed_list(categorical, str):
            raise TypeError("'categorical' must be None, an empty list, or a list of str.")
        
        if not _is_typed_list(numerical, str):
            raise TypeError("'numerical' must be None, an empty list, or a list of str.")
        
        if not _is_typed_list(targets, str):
            raise TypeError("'target' must be None, an empty list, or a list of str.")
         
        if not _is_typed_list(unused_floats, str):
            raise TypeError("'unused_float' must be None, an empty list, or a list of str.")
        
        if not _is_typed_list(unused_strings, str):
            raise TypeError("'unused_string' must be None, an empty list, or a list of str.")
        
        # ------------------------------------------------------------
         
        for kkey in list(roles.keys()):
            if kkey not in self._possible_keys:
                raise ValueError("'" + kkey + """' is not a proper role and will be ignored. Possible roles are:
                    """ + str(self._possible_keys))
            if type(roles[kkey]) is not list or not (len(roles[kkey]) == 0 or all([type(ff) is str for ff in roles[kkey]])):
                raise TypeError("Error for role '"+kkey+"': the corresponding value must be an empty list or a list of str")

        # ------------------------------------------------------------

        self._categorical_columns = []

        for i, name in enumerate(categorical):
            self._categorical_columns.append(
                StringColumn(
                    name=name,
                    role=self._role.categorical,
                    num=i,
                    df_name=self.name
                )
            )

        # ------------------------------------------------------------

        self._join_key_columns = []

        for i, name in enumerate(join_keys):
            self._join_key_columns.append(
                StringColumn(
                    name=name,
                    role=self._role.join_key,
                    num=i,
                    df_name=self.name
                )
            )

        # ------------------------------------------------------------

        self._numerical_columns = []

        for i, name in enumerate(numerical):
            self._numerical_columns.append(
                FloatColumn(
                    name=name,
                    role=self._role.numerical,
                    num=i,
                    df_name=self.name
                )
            )

        # ------------------------------------------------------------

        self._target_columns = []

        for i, name in enumerate(targets):
            self._target_columns.append(
                FloatColumn(
                    name=name,
                    role=self._role.target,
                    num=i,
                    df_name=self.name
                )
            )

        # ------------------------------------------------------------

        self._time_stamp_columns = []

        for i, name in enumerate(time_stamps):
            self._time_stamp_columns.append(
                FloatColumn(
                    name=name,
                    role=self._role.time_stamp,
                    num=i,
                    df_name=self.name
                )
            )
 
        # ------------------------------------------------------------
          
        self._unused_float_columns = []

        for i, name in enumerate(unused_floats):
            self._unused_float_columns.append(
                FloatColumn(
                    name=name,
                    role=self._role.unused_float,
                    num=i,
                    df_name=self.name
                )
            )
             
        # ------------------------------------------------------------
   
        self._unused_string_columns = []
        
        for i, name in enumerate(unused_strings):
            self._unused_string_columns.append(
                StringColumn(
                    name=name,
                    role=self._role.unused_string,
                    num=i,
                    df_name=self.name
                )
            )
         
        # ------------------------------------------------------------
        
        self._check_duplicates()
        
    # ----------------------------------------------------------------

    def __eq__(self, other):
        """Compares the current instance of the
        :class:`~getml.data.DataFrame` with another one.

        Args:
            other (:class:`~getml.data.DataFrame`):

                Another :class:`~getml.data.DataFrame` to compare
                the current instance against.

        Returns:
            bool: Whether the current instance and `other` share the
                same content.

        Raises:
            TypeError: If `other` is not of class
                :class:`~getml.data.DataFrame`

        """

        if not isinstance(other, DataFrame):
            raise TypeError("A DataFrame can only be compared to another getml.data.DataFrame")
        
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
    
    def __len__(self):
        return self.n_rows()
    
    # ----------------------------------------------------------------

    def __repr__(self):
        return str(self)
    
    # ----------------------------------------------------------------

    def __str__(self):
        
        cmd = dict()
        cmd["type_"] = "DataFrame.get_string"
        cmd["name_"] = self.name
        
        s = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(s)
        
        s.close()

        return msg

    # ------------------------------------------------------------

    def _add_categorical_column(self, col, name, role, unit):

        # ------------------------------------------------------------
        # Send command

        cmd = dict()
        cmd["type_"] = "DataFrame.add_categorical_column"
        cmd["name_"] = name

        cmd["col_"] = col.thisptr
        cmd["df_name_"] = self.name
        cmd["role_"] = role
        cmd["unit_"] = unit

        comm.send(cmd)

        # ------------------------------------------------------------

        self.refresh()

    # ------------------------------------------------------------

    def _add_column(self, col, name, role, unit):

        # ------------------------------------------------------------
        # Send command

        cmd = dict()
        cmd["type_"] = "DataFrame.add_column"
        cmd["name_"] = name

        cmd["col_"] = col.thisptr
        cmd["df_name_"] = self.name
        cmd["role_"] = role
        cmd["unit_"] = unit

        comm.send(cmd)

        # ------------------------------------------------------------

        self.refresh()

    # ------------------------------------------------------------
    
    def _add_numpy_array(self, numpy_array, name, role, unit):
        
        if len(numpy_array.shape) != 1:
            raise TypeError(
                """numpy.ndarray needs to be one-dimensional!
                Maybe you can call .ravel().""")
       
        temp_df = pd.DataFrame()
        temp_df[name] = numpy_array
      
        if role is None:
            if _is_numerical_type(temp_df.dtypes[0]):
                role = self._role.unused_float
            else:
                role = self._role.unused_string

        if role in self._numerical_roles:
            col = FloatColumn(
                name=name, role=role, df_name=self.name)
             
            if role == self._role.time_stamp:
                arr = self._transform_timestamps(temp_df)
            
            elif role == self._role.target:
                arr = temp_df[[name]].apply(
                    pd.to_numeric, errors="raise"
                ).values

            else:
                arr = temp_df[[name]].apply(
                    pd.to_numeric, errors="coerce"
                ).values

        else:
            col = StringColumn(
                name=name, role=role, df_name=self.name)
            
            arr = numpy_array.astype(np.str)
        
        del temp_df

        self._send_numpy_array(col, arr)

        self.refresh()

    # ------------------------------------------------------------

    def _check_duplicates(self):
        
        all_colnames = []

        all_colnames = self._check_if_exists(
            self.categorical_names, all_colnames)

        all_colnames = self._check_if_exists(
            self.join_key_names, all_colnames)
        
        all_colnames = self._check_if_exists(
            self.numerical_names, all_colnames)
        
        all_colnames = self._check_if_exists(
            self.target_names, all_colnames)
        
        all_colnames = self._check_if_exists(
            self.time_stamp_names, all_colnames)
        
        all_colnames = self._check_if_exists(
            self.unused_names, all_colnames)
          
    # ----------------------------------------------------------------

    def _append_pandas_df(self, data_frame, sock=None):
        
        if not isinstance(data_frame, pd.DataFrame):
            raise TypeError("'data_frame' must be of type 'pandas.DataFrame'")
        if sock is not None and type(sock) is not socket.socket:
            raise TypeError("'sock' must be either None or a 'socket.socket'")

        # ------------------------------------------------------------

        self._check_plausibility(data_frame)

        # ------------------------------------------------------------
        # Create connection.

        cmd = dict()
        cmd["type_"] = "DataFrame.append"
        cmd["name_"] = self.name

        if sock is None:
            s = comm.send_and_receive_socket(cmd)
        else:
            s = sock
            comm.send_string(s, json.dumps(cmd))

        # ------------------------------------------------------------
        # Send individual matrices to getml engine

        self._send_data(data_frame, s)

        # ------------------------------------------------------------

        self._close(s)
        
        if sock is None:
            s.close()

        return self
    
        # ------------------------------------------------------------
        
    def _check_if_exists(self, colnames, all_colnames):
        
        for col in colnames:
            if col in all_colnames:
                raise ValueError("Duplicate column: '" + col + "'!")
            
            all_colnames.append(col)
            
        return all_colnames
    
        # ------------------------------------------------------------

    def _check_plausibility(self, data_frame):

        self._check_duplicates()

        for col in self.categorical_names:
            if col not in data_frame.columns:
                raise ValueError(
                    "Column named '" + col + "' does not exist!")

        for col in self.join_key_names:
            if col not in data_frame.columns:
                raise ValueError(
                    "Column named '" + col + "' does not exist!")

        for col in self.numerical_names:
            if col not in data_frame.columns:
                raise ValueError(
                    "Column named '" + col + "' does not exist!")

        for col in self.target_names:
            if col not in data_frame.columns:
                raise ValueError(
                    "Column named '" + col + "' does not exist!")

        for col in self.time_stamp_names:
            if col not in data_frame.columns:
                raise ValueError(
                    "Column named '" + col + "' does not exist!")

        for col in self.unused_names:
            if col not in data_frame.columns:
                raise ValueError(
                    "Column named '" + col + "' does not exist!")
            
        # ------------------------------------------------------------

    def _close(self, s):

        cmd = dict()
        cmd["type_"] = "DataFrame.close"
        cmd["name_"] = self.name

        comm.send_string(s, json.dumps(cmd))
        
        msg = comm.recv_string(s)
        
        if msg != "Success!":
            comm.engine_exception_handler(msg)
        
        # ------------------------------------------------------------

    def _extract_shape(self, cmd, name):
        shape = cmd[name + "_shape_"]
        shape = np.asarray(shape).astype(np.int32)
        return shape.tolist()

        # ------------------------------------------------------------

    def _get_column(self, name, columns):
        for col in columns:
            if col.name == name:
                return col
        return None
    
        # ------------------------------------------------------------

    def __getitem__(self, name):

        col = self._get_column(name, self._categorical_columns)
        
        if col is not None:
            return col

        col = self._get_column(name, self._join_key_columns)
        
        if col is not None:
            return col
        
        col = self._get_column(name, self._numerical_columns)
        
        if col is not None:
            return col

        col = self._get_column(name, self._target_columns)
        
        if col is not None:
            return col

        col = self._get_column(name, self._time_stamp_columns)
        
        if col is not None:
            return col
        
        col = self._get_column(name, self._unused_float_columns)
        
        if col is not None:
            return col

        col = self._get_column(name, self._unused_string_columns)
        
        if col is not None:
            return col
        
        raise ValueError("Column named '" + name + "' not found.")

    # ------------------------------------------------------------
    
    def _send_pandas_df(self, data_frame, sock=None):
        
        if not isinstance(data_frame, pd.DataFrame):
            raise TypeError("'data_frame' must be of type 'pandas.DataFrame'")
        if sock is not None and type(sock) is not socket.socket:
            raise TypeError("'sock' must be either None or a 'socket.socket'")

        # ------------------------------------------------------------

        self._check_plausibility(data_frame)

        # ------------------------------------------------------------
        # Send data frame itself

        cmd = dict()
        cmd["type_"] = "DataFrame"
        cmd["name_"] = self.name

        if sock is None:
            s = comm.send_and_receive_socket(cmd)
        else:
            s = sock
            comm.send_string(s, json.dumps(cmd))

        msg = comm.recv_string(s)

        if msg != "Success!":
            comm.engine_exception_handler(msg)
        
        # ------------------------------------------------------------
        # Send individual columns to getml engine

        self._send_data(data_frame, s)

        # ------------------------------------------------------------

        self._close(s)
        
        if sock is None:
            s.close()

        return self
    
    # ------------------------------------------------------------
    
    def _send_numpy_array(self, col, numpy_array, s=None):
 
        # -------------------------------------------
        # Send the columns' JSON command to getml engine
         
        if s is None:
            s = comm.send_and_receive_socket(col.thisptr)
        else:
            cmd = json.dumps(col.thisptr) 
            comm.send_string(s, cmd)
    
        # -------------------------------------------
        # Send data to getml engine

        if col.thisptr["type_"] == "StringColumn":
            comm.send_categorical_matrix(s, numpy_array)

        elif col.thisptr["type_"] == "FloatColumn":
            comm.send_matrix(s, numpy_array)
        
        # -------------------------------------------
        # Make sure everything went well

        msg = comm.recv_string(s)

        if msg != "Success!":
            comm.engine_exception_handler(msg)

    # ------------------------------------------------------------

    def _send_data(self, data_frame, s):
        
        for col in self._categorical_columns:
            self._send_numpy_array(
                col,
                data_frame[[col.name]].values.astype(np.str),
                s
            )
 
        for col in self._join_key_columns:
            self._send_numpy_array(
                col,
                data_frame[[col.name]].values.astype(np.str),
                s
            )

        for col in self._numerical_columns:
            self._send_numpy_array(
                col,
                data_frame[[col.name]].apply(
                    pd.to_numeric, errors="coerce"
                ).values,
                s
            )
             
        for col in self._target_columns:
            self._send_numpy_array(
                col,
                data_frame[[col.name]].apply(
                    pd.to_numeric, errors="raise"
                ).values,
                s
            )
            
        for col in self._time_stamp_columns:
            self._send_numpy_array(
                col,
                self._transform_timestamps(
                    data_frame[[col.name]]
                ),
                s
            )
            
        for col in self._unused_float_columns:
            self._send_numpy_array(
                col,
                data_frame[[col.name]].apply(
                    pd.to_numeric, errors="coerce"
                ).values,
                s
            )
                
        for col in self._unused_string_columns:
            self._send_numpy_array(
                col,
                data_frame[[col.name]].values.astype(np.str),
                s
            )

        # ------------------------------------------------------------

    def _transform_timestamps(self, time_stamps):
        # Transforming a time stamp using to_numeric
        # will result in the number of nanoseconds since
        # the beginning of UNIX time. There are 8.64e+13 nanoseconds
        # in a day.
        transformed = pd.DataFrame()

        for colname in time_stamps.columns:
            if pd.api.types.is_numeric_dtype(time_stamps[colname]):
                transformed[colname] = time_stamps[colname]
            else:
                transformed[colname] = time_stamps[[colname]].apply(
                    pd.to_datetime,
                    errors="coerce"
                ).apply(
                    pd.to_numeric,
                    errors="coerce"
                ).apply(
                    lambda val: val / 8.64e+13
                )[colname]

        return transformed.values

    # ------------------------------------------------------------
    
    def _set_role(
            self, 
            name, 
            role, 
            time_formats):
        
        if not isinstance(name, str):
            raise TypeError("Parameter 'name' must be a string!")

        col = self[name]
        
        self.add(
            col, 
            name=name, 
            role=role, 
            unit=col.unit,
            time_formats=time_formats)
    
    # ------------------------------------------------------------
    
    def _set_unit(self, name, unit, sock=None):
        
        if not isinstance(name, str):
            raise TypeError("Parameter 'name' must be a string!")
 
        col = self[name]

        cmd = dict()

        cmd.update(col.thisptr)

        cmd["type_"] += ".set_unit"
        
        cmd["unit_"] = unit
        
        if sock is None:
            comm.send(cmd)
        else:
            msg = json.dumps(cmd)
            comm.send_string(sock, msg)
            msg = comm.recv_string(sock)
            if msg != "Success!":
                comm.engine_exception_handler(msg)
 
     # ------------------------------------------------------------
        
    def add(self, 
            col, 
            name, 
            role=None, 
            unit="",
            time_formats=[
                "%Y-%m-%dT%H:%M:%s%z", 
                "%Y-%m-%d %H:%M:%S", 
                "%Y-%m-%d"]):
        """Adds a column to the current :class:`~getml.data.DataFrame`.

        Args:
            col (:mod:`~getml.column` or :mod:`numpy.ndarray`): 
                The column or numpy.ndarray to be added.
            
            name (str): Name of the new column.
            
            role (str, optional):

                Role of the new column. Must be one of the following:
        
                * :const:`~getml.data.roles.categorical`
                * :const:`~getml.data.roles.join_key`
                * :const:`~getml.data.roles.numerical`
                * :const:`~getml.data.roles.target`
                * :const:`~getml.data.roles.time_stamp`
                * :const:`~getml.data.roles.unused_float`
                * :const:`~getml.data.roles.unused_string`

            unit (str, optional): Unit of the column.

            time_formats (str, optional): Formats to be used to parse the time stamps.

                This is only necessary, if an implicit conversion from
                a :class:`~getml.data.columns.StringColumn` to a time
                stamp is taking place.

                The formats are allowed to contain the following
                special characters:

                * %w - abbreviated weekday (Mon, Tue, ...)
                * %W - full weekday (Monday, Tuesday, ...)
                * %b - abbreviated month (Jan, Feb, ...)
                * %B - full month (January, February, ...)
                * %d - zero-padded day of month (01 .. 31)
                * %e - day of month (1 .. 31)
                * %f - space-padded day of month ( 1 .. 31)
                * %m - zero-padded month (01 .. 12)
                * %n - month (1 .. 12)
                * %o - space-padded month ( 1 .. 12)
                * %y - year without century (70)
                * %Y - year with century (1970)
                * %H - hour (00 .. 23)
                * %h - hour (00 .. 12)
                * %a - am/pm
                * %A - AM/PM
                * %M - minute (00 .. 59)
                * %S - second (00 .. 59)
                * %s - seconds and microseconds (equivalent to %S.%F)
                * %i - millisecond (000 .. 999)
                * %c - centisecond (0 .. 9)
                * %F - fractional seconds/microseconds (000000 - 999999)
                * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
                * %Z - time zone differential in RFC format (GMT or +NNNN)
                * %% - percent sign
        
        Raises:
            TypeError: If any of the input arguments is of wrong type.

            ValueError:
                If one of the provided keys in `roles` does not match a
                definition in :mod:`~getml.data.roles`.

        """
       
        # ------------------------------------------------------------
        
        if isinstance(col, np.ndarray):
            self._add_numpy_array(col, name, role, unit)
            return
        
        # ------------------------------------------------------------
        
        is_boolean = isinstance(col, _VirtualBooleanColumn)

        is_string = isinstance(
            col, StringColumn) or isinstance(
            col, _VirtualStringColumn)
        
        is_float = isinstance(
            col, FloatColumn) or isinstance(
            col, _VirtualFloatColumn)
        
        # ------------------------------------------------------------
        
        correct_coltype = (is_boolean or is_string or is_float) 
        
        if not correct_coltype:
            raise TypeError(
                """'col' must be an getml column or a numpy.ndarray!""")
        
        # ------------------------------------------------------------
        
        if type(name) is not str:
            raise TypeError("'name' must be of type str")
       
        # ------------------------------------------------------------
         
        allowed_roles = self._categorical_roles + self._numerical_roles

        if role is None:
            if is_float:
                role = self._role.unused_float
            else:
                role = self._role.unused_string

        correct_role = type(role) is str 
        correct_role = correct_role and role in allowed_roles 

        if not correct_role:
            raise ValueError(
                """'role' must be None or of type str and in """ + str(allowed_roles) + ".")
        
        # ------------------------------------------------------------
        
        if type(unit) is not str:
            raise TypeError("'unit' must be of type str")
        
        # ------------------------------------------------------------
       
        if (is_boolean or is_float) and role in self._categorical_roles:
            col = col.as_str()

        elif (is_boolean or is_string) and role in self._numerical_roles:
            if role == self._role.time_stamp:
                col = col.as_ts(time_formats=time_formats) 
            else:
                col = col.as_num()
 
        # ------------------------------------------------------------
        
        is_string = isinstance(
            col, StringColumn) or isinstance(
            col, _VirtualStringColumn)
        
        if is_string:
            self._add_categorical_column(col, name, role, unit)
        else:
            self._add_column(col, name, role, unit)
            
    # ------------------------------------------------------------
    
    @property
    def categorical_names(self):
        """
        List of the names of all categorical columns.

        Returns:
            List[str]:
                List of the names of all categorical columns.
        """
        return [col.name for col in self._categorical_columns]
    
    # ------------------------------------------------------------
    
    @property
    def colnames(self):
        """
        List of the names of all columns.

        Returns:
            List[str]:
                List of the names of all columns.
        """
        colnames = self.categorical_names
        colnames += self.join_key_names
        colnames += self.numerical_names
        colnames += self.target_names
        colnames += self.time_stamp_names
        colnames += self.unused_names
        return colnames 
    
    # ------------------------------------------------------------

    def delete(self, mem_only=False):
        """Deletes the data frame from the getML engine.

        If called with the `mem_only` option set to True, the data
        frame corresponding to the handler represented by the current
        instance can be reloaded using the
        :meth:`~getml.data.DataFrame.load` method.

        Args:
            mem_only (bool, optional): 

                If True, the data frame will not be deleted
                permanently but just from memory (RAM).

        Raises:
            TypeError: If any of the input arguments is of wrong type.

        """
        
        if type(mem_only) is not bool:
            raise TypeError("'mem_only' must be of type bool")

        # ------------------------------------------------------------
        # Send JSON command to getml engine

        cmd = dict()
        cmd["type_"] = "DataFrame.delete"
        cmd["name_"] = self.name
        cmd["mem_only_"] = mem_only

        comm.send(cmd)
 
    # ------------------------------------------------------------
  
    @classmethod
    def from_csv(cls,
                 fnames,
                 name,
                 num_lines_sniffed=1000,
                 quotechar='"',
                 sep=',',
                 skip=0,
                 roles=None,
                 ignore=False,
                 dry=False):
        """Create a DataFrame from CSV files.

        The fastest way to import data into the getML engine is to
        read it directly from CSV files. It will construct a data
        frame object in the engine, fill it with the data read from
        the CSV file(s), and return a corresponding
        :class:`~getml.data.DataFrame` handle.

        Args:
            fnames (List[str]): CSV file paths to be read.
            
            name (str): Name of the data frame to be created.

            num_lines_sniffed (int, optional):
                Number of lines analysed by the sniffer.

            quotechar (str, optional): The character used to wrap strings.
            
            sep (str, optional): The separator used for separating fields.

            skip (int, optional):
                Number of lines to skip at the beginning of each file.
            
            roles(dict[str, List[str]], optional): A dictionary mapping 
                the roles to the column names. If this is not passed, 
                then the roles will be sniffed from the CSV files.
                The roles dictionary should be in the following format:

                >>> roles = {"role1": ["colname1", "colname2"], "role2": ["colname3"]}

            ignore (bool, optional): Only relevant when roles is not None.
                Determines what you want to do with any colnames not 
                mentioned in roles. Do you want to ignore them (True) 
                or read them in as unused columns (False)?
            
            dry (bool, optional): If set to True, then the data 
                will not actually be read. Instead, the method will only 
                return the roles it would have used. This can be used 
                to hard-code roles when setting up a pipeline.

        Raises:
            TypeError: If any of the input arguments is of a wrong type.
            ValueError:
                If one of the provided keys in `roles` does not match a
                definition in :mod:`~getml.data.roles`.

        Returns:
            :class:`~getml.data.DataFrame`:

                Handler of the underlying data.

        Note:

            The created data frame object is only held in memory by
            the getML engine. If you want to use it in later sessions
            or after switching the project, you have to called
            :meth:`~getml.data.DataFrame.save` method.

            It is assumed that the first line of each CSV file
            contains a header with the column names.

            In addition to reading data from a CSV file, you can also
            write an existing :class:`~getml.data.DataFrame` back into
            one using :meth:`~getml.data.DataFrame.to_csv` or
            replace/append to the current instance using the
            :meth:`~getml.data.DataFrame.read_csv` method.

        Examples:
            
            Let's assume you have two CSV files - *file1.csv* and
            *file2.csv* - in the current working directory. You can
            upload their data into the getML engine using.
            
            >>> df_expd = data.DataFrame.from_csv(
            ...     fnames=["file1.csv", "file2.csv"],
            ...     name="MY DATA FRAME",
            ...     sep=';',
            ...     quotechar='"'
            ... )

            However, the CSV format lacks type safety. If you want to 
            build a reliable pipeline, it is a good idea 
            to hard-code the roles:

            >>> roles = {"categorical": ["colname1", "colname2"], "target": ["colname3"]}
            >>> 
            >>> df_expd = data.DataFrame.from_csv(
            ...         fnames=["file1.csv", "file2.csv"],
            ...         name="MY DATA FRAME",
            ...         sep=';',
            ...         quotechar='"',
            ...         roles=roles
            ... )

            If you think that typing out all of the roles by hand is too 
            cumbersome, you can use a dry run:

            >>> roles = data.DataFrame.from_csv(
            ...         fnames=["file1.csv", "file2.csv"],
            ...         name="MY DATA FRAME",
            ...         sep=';',
            ...         quotechar='"',
            ...         dry=True                                     
            ... ) 

            This will return the roles dictionary it would have used. You 
            can now hard-code this.

        """

        if type(fnames) is str:
            fnames = [fnames]

	# ------------------------------------------------------------

        if not _is_non_empty_typed_list(fnames, str):
            raise TypeError("'fnames' must be either a string or a list of str.")
        if type(name) is not str:
            raise TypeError("'name' must be str.")
        if not isinstance(num_lines_sniffed, numbers.Real):
            raise TypeError("'num_lines_sniffed' must be a real number")
        if type(quotechar) is not str:
            raise TypeError("'quotechar' must be str.")
        if type(sep) is not str:
            raise TypeError("'sep' must be str.")
        if not isinstance(skip, numbers.Real):
            raise TypeError("'skip' must be a real number")
        # The content of roles is checked in the class constructor called below.
        if roles is not None and type(roles) is not dict:
            raise TypeError("'roles' must be dict or None.")
        if type(ignore) is not bool:
            raise TypeError("'ignore' must be bool.")
        if type(dry) is not bool:
            raise TypeError("'dry' must be bool.")
            
	# ------------------------------------------------------------
        
        if roles is None or not ignore:
            sniffed_roles = _sniff_csv(
                fnames=fnames,
                num_lines_sniffed=num_lines_sniffed,
                quotechar=quotechar,
                sep=sep,
                skip=skip)
            
            if roles is None:
                roles = sniffed_roles
            else:
                roles = _update_sniffed_roles(
                    sniffed_roles, roles)
        
        if dry:
            return roles 

        df = cls(name, roles) 

        return df.read_csv(
            fnames=fnames,
            append=False,
            quotechar=quotechar,
            sep=sep)

    # ------------------------------------------------------------
   
    @classmethod
    def from_db(
            cls, 
            table_name, 
            name, 
            roles=None, 
            ignore=False, 
            dry=False):
        """Create a DataFrame from a table in a database.

        It will construct a data frame object in the engine, fill it
        with the data read from table `table_name` in the connected
        database (see :mod:`~getml.database`), and return a
        corresponding :class:`~getml.data.DataFrame` handle.

        Args:
            table_name (str): Name of the table to be read.
            
            name (str): Name of the data frame to be created.
            
            roles(dict[str, List[str]], optional): A dictionary mapping 
                the roles to the column names. If this is not passed, 
                then the roles will be sniffed from the table.
                The roles dictionary should be in the following format:

                >>> roles = {"role1": ["colname1", "colname2"], "role2": ["colname3"]}
 
            ignore (bool, optional): Only relevant when roles is not None.
                Determines what you want to do with any colnames not 
                mentioned in roles. Do you want to ignore them (True) 
                or read them in as unused columns (False)?
            
            dry (bool, optional): If set to True, then the data 
                will not actually be read. Instead, the method will only 
                return the roles it would have used. This can be used 
                to hard-code roles when setting up a pipeline.

        Raises:
            TypeError: If any of the input arguments is of a wrong type.
            ValueError:
                If one of the provided keys in `roles` does not match a
                definition in :mod:`~getml.data.roles`.

        Returns:
            :class:`~getml.data.DataFrame`:

                Handler of the underlying data.

        Note:

            The created data frame object is only held in memory by
            the getML engine. If you want to use it in later sessions
            or after switching the project, you have to called
            :meth:`~getml.data.DataFrame.save` method.

            In addition to reading data from a table, you can also
            write an existing :class:`~getml.data.DataFrame` back into
            a new one in the same database using
            :meth:`~getml.data.DataFrame.to_db` or replace/append to
            the current instance using the
            :meth:`~getml.data.DataFrame.read_db` or
            :meth:`~getml.data.DataFrame.read_query` method.
        
        Example:

            .. code-block:: python

                getml.database.connect_mysql(
                    host="relational.fit.cvut.cz",
                    port=3306,
                    dbname="financial",
                    user="guest",
                    password="relational"
                )

                loan = getml.data.DataFrame.from_db(table_name='loan', name='df_loan')

        """
        
        if type(table_name) is not str:
            raise TypeError("'table_name' must be str.")
        if type(name) is not str:
            raise TypeError("'name' must be str.")
        # The content of roles is checked in the class constructor called below.
        if roles is not None and type(roles) is not dict:
            raise TypeError("'roles' must be dict or None.")
        if type(ignore) is not bool:
            raise TypeError("'ignore' must be bool.")
        if type(dry) is not bool:
            raise TypeError("'dry' must be bool.")
        
	# ------------------------------------------------------------

        if roles is None or not ignore:
            sniffed_roles = _sniff_db(table_name)
            
            if roles is None:
                roles = sniffed_roles
            else:
                roles = _update_sniffed_roles(
                    sniffed_roles, roles)
        
        if dry:
            return roles 
        
        df = cls(name, roles) 

        return df.read_db(
            table_name=table_name,
            append=False)

    # --------------------------------------------------------------------

    @classmethod
    def from_dict(
            cls, 
            data, 
            name,
            roles=None, 
            ignore=False, 
            dry=False):
        """Create a new DataFrame from a dict

        Args:
            data (dict): The dict containing the data.
                The data should be in the following format:

                .. code-block:: python

                    data = {'col1': [1.0, 2.0, 1.0], 'col2': ['A', 'B', 'C']}

            name (str): Name of the data frame to be created.

            roles(dict[str, List[str]], optional): A dictionary mapping
                the roles to the column names. If this is not passed,
                then the roles will be sniffed from the string.
                The roles dictionary should be in the following format:

                .. code-block:: python

                    roles = {"role1": ["colname1", "colname2"], "role2": ["colname3"]}

            ignore (bool, optional): Only relevant when roles is not None.
                Determines what you want to do with any colnames not 
                mentioned in roles. Do you want to ignore them (True) 
                or read them in as unused columns (False)?
            
            dry (bool, optional): If set to True, then the data 
                will not actually be read. Instead, the method will only 
                return the roles it would have used. This can be used 
                to hard-code roles when setting up a pipeline.

        Raises:
            TypeError: If any of the input arguments is of a wrong type.
            ValueError:
                If one of the provided keys in `roles` does not match a
                definition in :mod:`~getml.data.roles`.
        
        Returns:
            :class:`~getml.data.DataFrame`:

                Handler of the underlying data.
        """
        
        if type(data) is not dict:
            raise TypeError("'data' must be dict.")
        if type(name) is not str:
            raise TypeError("'name' must be str.")
        # The content of roles is checked in the class constructor called below.
        if roles is not None and type(roles) is not dict:
            raise TypeError("'roles' must be dict or None.")
        if type(ignore) is not bool:
            raise TypeError("'ignore' must be bool.")
        if type(dry) is not bool:
            raise TypeError("'dry' must be bool.")
        
	# ------------------------------------------------------------
    
        return cls.from_json(
                json.dumps(data), 
                name=name, 
                roles=roles,
                ignore=ignore,
                dry=dry)

    # --------------------------------------------------------------------

    @classmethod
    def from_json(
            cls, 
            json_str, 
            name, 
            roles=None, 
            ignore=False, 
            dry=False):
        """Create a new DataFrame from a JSON string.

        It will construct a data frame object in the engine, fill it
        with the data read from the JSON string, and return a
        corresponding :class:`~getml.data.DataFrame` handle.

        Args:
            json_str (str): The JSON string containing the data.
                The json_str should be in the following format:

                .. code-block:: python

                    json_str = "{'col1': [1.0, 2.0, 1.0], 'col2': ['A', 'B', 'C']}"
            
            name (str): Name of the data frame to be created.

            roles(dict[str, List[str]], optional): A dictionary mapping
                the roles to the column names. If this is not passed,
                then the roles will be sniffed from the string.
                The roles dictionary should be in the following format:

                .. code-block:: python

                    roles = {"role1": ["colname1", "colname2"], "role2": ["colname3"]}
            
            ignore (bool, optional): Only relevant when roles is not None.
                Determines what you want to do with any colnames not 
                mentioned in roles. Do you want to ignore them (True) 
                or read them in as unused columns (False)?
            
            dry (bool, optional): If set to True, then the data 
                will not actually be read. Instead, the method will only 
                return the roles it would have used. This can be used 
                to hard-code roles when setting up a pipeline.

        Raises:
            TypeError: If any of the input arguments is of a wrong type.
            ValueError:
                If one of the provided keys in `roles` does not match a
                definition in :mod:`~getml.data.roles`.

        Returns:
            :class:`~getml.data.DataFrame`:

                Handler of the underlying data.

        Note:

            The created data frame object is only held in memory by
            the getML engine. If you want to use it in later sessions
            or after switching the project, you have to called
            :meth:`~getml.data.DataFrame.save` method.

            In addition to reading data from a JSON string, you can
            also write an existing :class:`~getml.data.DataFrame` back
            into one using :meth:`~getml.data.DataFrame.to_json` or
            replace/append to the current instance using the
            :meth:`~getml.data.DataFrame.read_json` method.

        """
        
        if type(json_str) is not str:
            raise TypeError("'json_str' must be str.")
        if type(name) is not str:
            raise TypeError("'name' must be str.")
        # The content of roles is checked in the class constructor called below.
        if roles is not None and type(roles) is not dict:
            raise TypeError("'roles' must be dict or None.")
        if type(ignore) is not bool:
            raise TypeError("'ignore' must be bool.")
        if type(dry) is not bool:
            raise TypeError("'dry' must be bool.")

	# ------------------------------------------------------------
        
        if roles is None or not ignore:
            sniffed_roles = _sniff_json(json_str)

            if roles is None:
                roles = sniffed_roles
            else:
                roles = _update_sniffed_roles(
                    sniffed_roles, roles)
        
        if dry:
            return roles 
        
        df = cls(name, roles)

        return df.read_json(
            json_str=json_str,
            append=False)

    # --------------------------------------------------------------------

    @classmethod
    def from_pandas(
            cls, 
            pandas_df, 
            name, 
            roles=None, 
            ignore=False, 
            dry=False):
        """Create a DataFrame from a :py:class:`pandas.DataFrame`.

        It will construct a data frame object in the engine, fill it
        with the data read from the :py:class:`pandas.DataFrame`, and
        return a corresponding :class:`~getml.data.DataFrame` handle.

        Args:
            pandas_df (:py:class:`pandas.DataFrame`): The table to be read.
            
            name (str): Name of the data frame to be created.
            
            roles(dict[str, List[str]], optional): A dictionary mapping 
                the roles to the column names. If this is not passed, 
                then the roles will be sniffed from the :py:class:`pandas.DataFrame`.
                The roles dictionary should be in the following format:

                .. code-block:: python

                    roles = {"role1": ["colname1", "colname2"], "role2": ["colname3"]}
         
            ignore (bool, optional): Only relevant when roles is not None.
                Determines what you want to do with any colnames not 
                mentioned in roles. Do you want to ignore them (True) 
                or read them in as unused columns (False)?
            
            dry (bool, optional): If set to True, then the data 
                will not actually be read. Instead, the method will only 
                return the roles it would have used. This can be used 
                to hard-code roles when setting up a pipeline.

        Raises:
            TypeError: If any of the input arguments is of a wrong type.
            ValueError:
                If one of the provided keys in `roles` does not match a
                definition in :mod:`~getml.data.roles`.
        
        Returns:
            :class:`~getml.data.DataFrame`:

                Handler of the underlying data.

        Note:

            The created data frame object is only held in memory by
            the getML engine. If you want to use it in later sessions
            or after switching the project, you have to called
            :meth:`~getml.data.DataFrame.save` method.

            In addition to reading data from a
            :py:class:`pandas.DataFrame`, you can also write an
            existing :class:`~getml.data.DataFrame` back into one
            using :meth:`~getml.data.DataFrame.to_pandas` or
            replace/append to the current instance using the
            :meth:`~getml.data.DataFrame.read_pandas` method.

        """
        
        if not isinstance(pandas_df, pd.DataFrame):
            raise TypeError("'pandas_df' must be of type pandas.DataFrame.")
        if type(name) is not str:
            raise TypeError("'name' must be str.")
        # The content of roles is checked in the class constructor called below.
        if roles is not None and type(roles) is not dict:
            raise TypeError("'roles' must be dict or None.")
        if type(ignore) is not bool:
            raise TypeError("'ignore' must be bool.")
        if type(dry) is not bool:
            raise TypeError("'dry' must be bool.")
        
	# ------------------------------------------------------------

        if roles is None or not ignore:
            sniffed_roles = _sniff_pandas(pandas_df)

            if roles is None:
                roles = sniffed_roles
            else:
                roles = _update_sniffed_roles(
                    sniffed_roles, roles)
        
        if dry:
            return roles

        df = cls(name, roles) 

        return df.read_pandas(
            pandas_df=pandas_df,
            append=False)
    
    # ------------------------------------------------------------

    def group_by(self, join_key, name, aggregations):
        """Creates new :class:`~getml.data.DataFrame` by grouping over a
        join key.

        This function split the DataFrame into groups with the same value for
        `join_key`, applies an aggregation function to one or more columns in
        each group, and combines the results into a new DataFrame. The
        aggregation funcion is defined for each column individually. This
        allows applying different aggregations to each column. In pandas this
        is known as `named aggregation
        <https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#named-aggregation>`_.

        Args:
            join_key (str): Name of the join key to group by.
            name (str): Name of the new DataFrame.
            aggregations (List[:class:`~getml.data.columns._Aggregation`]):

                Methods to apply on the groupings.

        Raises:
            TypeError: If any of the input arguments is of wrong type.

        Returns:
            :class:`~getml.data.DataFrame`:

                Handler of the newly generated data frame object.

        Examples:

            Generate example data

            .. code-block:: python

                data = dict(
                    fruit=["banana", "apple", "cherry", "cherry", "melon", "pineapple"],
                    price=[2.4, 3.0, 1.2, 1.4, 3.4, 3.4],
                    join_key=["0", "1", "2", "2", "3", "3"]
                )
                df = getml.data.DataFrame.from_dict(
                    data,
                    name="fruits",
                    roles={"categorical": ["fruit"], "join_key": ["join_key"], "numerical": ["price"]}
                )

                df

            .. code-block:: pycon

                | join_key | fruit       | price     |
                | join key | categorical | numerical |
                --------------------------------------
                | 0        | banana      | 2.4       |
                | 1        | apple       | 3         |
                | 2        | cherry      | 1.2       |
                | 2        | cherry      | 1.4       |
                | 3        | melon       | 3.4       |
                | 3        | pineapple   | 3.4       |


            Group DataFrame using `join_key`. Aggregate the resulting groups by
            averaging and summing over the `price` column and counting the
            distinct entires in the `fruit` column

            .. code-block:: python

                df_grouped = df.group_by("join_key", "fruits_grouped",
                    [df["price"].avg(alias="avg price"),
                    df["price"].sum(alias="total price"),
                    df["fruit"].count_distinct(alias="unique items")])

                df_grouped

            .. code-block:: pycon

                | join_key | avg price | total price | unique items |
                | join key | unused    | unused      | unused       |
                -----------------------------------------------------
                | 3        | 3.4       | 6.8         | 2            |
                | 2        | 1.3       | 2.6         | 1            |
                | 0        | 2.4       | 2.4         | 1            |
                | 1        | 3         | 3           | 1            |
        """
        
        if type(join_key) is not str:
            raise TypeError("'join_key' must be of type str")
        if type(name) is not str:
            raise TypeError("'name' must be of type str")

        # ------------------------------------------------------------
        # Build command

        cmd = dict()
        cmd["name_"] = name
        cmd["type_"] = "DataFrame.group_by"

        cmd["join_key_name_"] = join_key
        cmd["df_name_"] = self.name
        cmd["aggregations_"] = [agg.thisptr for agg in aggregations]

        comm.send(cmd)

        # ------------------------------------------------------------
        # Create handle for new data frame.

        new_df = DataFrame(name)

        return new_df.refresh()

        # ------------------------------------------------------------

    def join(
            self,
            name,
            other,
            join_key,
            other_join_key=None,
            cols=None,
            other_cols=None,
            how="inner",
            where=None):
        """Create a new :class:`~getml.data.DataFrame` by joining the
        current instance with another
        :class:`~getml.data.DataFrame`.

        Args:
            name (str): The name of the new :class:`~getml.data.DataFrame`.
            other (DataFrame): The other :class:`~getml.data.DataFrame`.
            join_key (str):

                Name of the column containing the join key in the
                current instance.

            other_join_key (str, optional):

                Name of the join key in the other
                :class:`~getml.data.DataFrame`. If set to None,
                `join_key` will be used for both the current instance
                and `other`.

            cols (List[Union[:class:`~getml.data.columns.FloatColumn`, :class:`~getml.data.columns.StringFloatColumn`], optional):

                :mod:`~getml.data.columns` in the current instances to be
                included in the resulting
                :class:`~getml.data.DataFrame`. If set to None, all
                columns will be used.

            other_cols (List[Union[:class:`~getml.data.columns.FloatColumn`, :class:`~getml.data.columns.StringColumn`], optional):

                :mod:`~getml.data.columns` in `other` to be included in the
                resulting :class:`~getml.data.DataFrame`. If set to
                None, all columns will be used.

            how (str, optional):

                Type of the join.

                Supported options:

                * 'left'
                * 'inner'
                * 'right'

            where (:class:`~getml.data.columns._VirtualBooleanColumn`, optional):

                Boolean column indicating which rows to be included in
                the resulting :class:`~getml.data.DataFrame`. If set
                to None, all rows will be used.

                If imposes a SQL-like WHERE condition on the join.

        Raises:
            TypeError: If any of the input arguments is of wrong type.

        Returns:
            :class:`~getml.data.DataFrame`:

                Handler of the newly create data frame object.

        Examples:
            Create DataFrame

            .. code-block:: python

                data_df = dict(
                    colors=["blue", "green", "yellow", "orange"],
                    numbers=[2.4, 3.0, 1.2, 1.4],
                    join_key=["0", "1", "2", "3"]
                )

                df = getml.data.DataFrame.from_dict(
                    data_df, name="df_1",
                    roles=dict(join_key=["join_key"], numerical=["numbers"], categorical=["colors"]))

                df

            .. code-block:: pycon

                | join_key | colors      | numbers   |
                | join key | categorical | numerical |
                --------------------------------------
                | 0        | blue        | 2.4       |
                | 1        | green       | 3         |
                | 2        | yellow      | 1.2       |
                | 3        | orange      | 1.4       |
            

            Create other Data Frame

            .. code-block:: python

                data_other = dict(
                    colors=["blue", "green", "yellow", "black", "orange", "white"],
                    numbers=[2.4, 3.0, 1.2, 1.4, 3.4, 2.2],
                    join_key=["0", "1", "2", "2", "3", "4"])

                other = getml.data.DataFrame.from_dict(
                    data_other, name="df_2",
                    roles=dict(join_key=["join_key"], numerical=["numbers"], categorical=["colors"]))

                other

            .. code-block:: pycon

                | join_key | colors      | numbers   |
                | join key | categorical | numerical |
                --------------------------------------
                | 0        | blue        | 2.4       |
                | 1        | green       | 3         |
                | 2        | yellow      | 1.2       |
                | 2        | black       | 1.4       |
                | 3        | orange      | 3.4       |
                | 4        | white       | 2.2       |
            

            Left join the two DataFrames on their join key, while keeping the
            columns 'colors' and 'numbers' from the first one and the column
            'colors' as 'other_color' from the second one. As subcondition only
            rows are selected where the 'number' columns are equal.

            .. code-block:: python

                joined_df = df.join(
                    name="joined_df",
                    other=other,
                    how="left",
                    join_key="join_key",
                    cols=[df["colors"], df["numbers"]],
                    other_cols=[other["colors"].alias("other_color")],
                    where=(df["numbers"] == other["numbers"]))

                joined_df

            .. code-block:: pycon

                | colors      | other_color | numbers   |
                | categorical | categorical | numerical |
                -----------------------------------------
                | blue        | blue        | 2.4       |
                | green       | green       | 3         |
                | yellow      | yellow      | 1.2       |
            
        """
        
        cols = cols or []
        other_cols = other_cols or []
        other_join_key = other_join_key or join_key
        
        if type(name) is not str:
            raise TypeError("'name' must be of type str")
        if not isinstance(other, DataFrame):
            raise TypeError("'other' must be of type getml.data.DataFrame")
        if type(join_key) is not str:
            raise TypeError("'join_key' must be of type str")
        if type(other_join_key) is not str:
            raise TypeError("'other_join_key' must be of type str")
        if not _is_typed_list(cols, [FloatColumn, StringColumn]):
            raise TypeError("""
                'cols' must be either None, an empty list, 
                or a list of getml.data.columns.FloatColumn 
                and getml.data.columns.StringColumn""")
        if not _is_typed_list(other_cols, [FloatColumn, StringColumn]):
            raise TypeError("""
                    'other_cols' must be either None, an empty list, 
                    or a list of getml.data.columns.FloatColumn 
                    and getml.data.columns.StringColumn""")
        if type(how) is not str or how not in ['left', 'inner', 'right']:
            raise TypeError("'how' must be of type str and set to either 'left', 'inner', or 'right'")
        if where is not None and not isinstance(where, _VirtualBooleanColumn):
            raise TypeError("'where' must be either None or of type getml.data.columns._VirtualBooleanColumn")

        # ------------------------------------------------------------
        # Send JSON command to getml engine

        cmd = dict()
        cmd["type_"] = "DataFrame.join"
        cmd["name_"] = name

        cmd["df1_name_"] = self.name
        cmd["df2_name_"] = other.name

        cmd["join_key_used_"] = join_key
        cmd["other_join_key_used_"] = other_join_key

        cmd["cols1_"] = cols
        cmd["cols2_"] = other_cols

        cmd["cols1_"] = [c.thisptr for c in cmd["cols1_"]]
        cmd["cols2_"] = [c.thisptr for c in cmd["cols2_"]]

        cmd["how_"] = how

        if where is not None:
            cmd["where_"] = where.thisptr

        comm.send(cmd)

        # ------------------------------------------------------------

        return DataFrame(name=name).refresh()

        # ------------------------------------------------------------
    
    @property
    def join_key_names(self):
        """
        List of the names of all join keys.

        Returns:
            List[str]:
                List of the names of all columns used as join keys.
        """
        return [col.name for col in self._join_key_columns]
    
        # ------------------------------------------------------------

    def load(self):
        """Loads saved data from disk.

        The data frame object holding the same name as the current
        :class:`~getml.data.DataFrame` instance will be loaded from
        disk into the getML engine and updates the current handler
        using :meth:`~getml.data.DataFrame.refresh`.

        Examples:

            Firstly, we have to create and upload some data sets.

            .. code-block:: python

                d, _ = getml.datasets.make_numerical(population_name = 'test')
                getml.data.list_data_frames()

            In the output of :func:`~getml.data.list_data_frames` we
            can find our underlying data frame object 'test' listed
            under the 'in_memory' key (it was created and uploaded by
            :func:`~getml.datasets.make_numerical`). This means the
            getML engine does only hold it in memory (RAM) yet and we
            still have to :meth:`~getml.data.DataFrame.save` it to
            disk in order to :meth:`~getml.data.DataFrame.load` it
            again or to prevent any loss of information between
            different sessions.

            .. code-block:: python

                d.save()
                getml.data.list_data_frames()
                d2 = getml.data.DataFrame(name = 'test').load()

        Returns:
            :class:`~getml.data.DataFrame`:
                Updated handle the underlying data frame in the getML
                engine.

        Note:

            When invoking :meth:`~getml.data.DataFrame.load` all
            changes of the underlying data frame object that took
            place after the last call to the
            :meth:`~getml.data.DataFrame.save` method will be
            lost. This methods, thus, enables you to undo changes
            applied to the :class:`~getml.data.DataFrame`.

            .. code-block:: python

                d, _ = getml.datasets.make_numerical()
                d.save()

                # Accidental change we want to undo
                d.rm('column_01')

                d.load()

            If :meth:`~getml.data.DataFrame.save` hasn't be called
            on the current instance yet or it wasn't stored to disk in
            a previous session, :meth:`~getml.data.DataFrame.load`
            will throw an exception

                File or directory '../projects/X/data/Y/' not found!

            Alternatively, :func:`~getml.data.load_data_frame`
            offers a more user-friendly way of creating
            :class:`~getml.data.DataFrame` handlers to data in the
            getML engine.

        """

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = "DataFrame.load"
        cmd["name_"] = self.name

        comm.send(cmd)

        # ------------------------------------------------------------

        return self.refresh()

        # ------------------------------------------------------------

    def n_bytes(self):
        """Size of the data stored in the underlying data frame in the getML
        engine.

        Raises:
            Exception:
                If the data frame corresponding to the current
                instance could not be found in the getML engine.

        Returns:
            :py:class:`numpy.uint64`:
                Size of the underlying object in bytes.

        """

        # ------------------------------------------------------------
        # Build and send JSON command

        cmd = dict()
        cmd["type_"] = "DataFrame.nbytes"
        cmd["name_"] = self.name

        s = comm.send_and_receive_socket(cmd)

        # ------------------------------------------------------------
        # Make sure model exists on getml engine

        msg = comm.recv_string(s)

        if msg != "Found!":
            s.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------
        # Receive number of bytes from getml engine

        nbytes = comm.recv_string(s)

        # ------------------------------------------------------------

        s.close()

        return np.uint64(nbytes)

        # ------------------------------------------------------------
    
    @property
    def n_categorical(self):
        """
        Number of categorical columns.

        Returns:
            int:
                Number of categorical columns
        """
        return len(self._categorical_columns)
    
        # ------------------------------------------------------------

    def n_cols(self):
        """
        Number of columns in the current instance.

        Returns:
            int:
                Overall number of columns
        """
        return self.n_categorical + self.n_join_keys + self.n_numerical + \
            self.n_targets + self.n_time_stamps + self.n_unused
 
        # ------------------------------------------------------------
    
    @property
    def n_join_keys(self):
        """
        Number of join keys.

        Returns:
            int:
                Number of columns used as join keys
        """
        return len(self._join_key_columns)
    
        # ------------------------------------------------------------
    
    @property
    def n_numerical(self):
        """
        Number of numerical columns.

        Returns:
            int:
                Number of numerical columns
        """
        return len(self._numerical_columns)
    
        # ------------------------------------------------------------

    def n_rows(self):
        """
        Number of rows in the current instance.

        Raises:
            Exception:
                If the data frame corresponding to the current
                instance could not be found in the getML engine.

        Returns:
            :py:class:`numpy.int32`:
                Overall number of rows
        """

        # ------------------------------------------------------------
        # Build and send JSON command

        cmd = dict()
        cmd["type_"] = "DataFrame.nrows"
        cmd["name_"] = self.name

        s = comm.send_and_receive_socket(cmd)

        # ------------------------------------------------------------
        # Make sure model exists on getml engine

        msg = comm.recv_string(s)

        if msg != "Found!":
            s.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------
        # Receive number of rows from getml engine

        nrows = comm.recv_string(s)

        # ------------------------------------------------------------

        s.close()

        return np.int32(nrows)

        # ------------------------------------------------------------
    
    @property
    def n_targets(self):
        """
        Number of target columns.

        Returns:
            int:
                Number of columns used as targets
        """
        return len(self._target_columns)
    
    # ------------------------------------------------------------
    
    @property
    def n_time_stamps(self):
        """
        Number of time stamps columns.

        Returns:
            int:
                Number of columns used as time stamps
        """
        return len(self._time_stamp_columns)
    
    # ------------------------------------------------------------
    
    @property
    def n_unused(self):
        """
        Number of unused columns. Unused columns will not be used by the 
        feature engineering algorithms.

        Returns:
            int:
                Number of columns that are unused.
        """
        return self.n_unused_floats + self.n_unused_strings
  
    # ------------------------------------------------------------
    
    @property
    def n_unused_floats(self):
        """
        Number of unused float columns. Unused columns will not be used by the 
        feature engineering algorithms.

        Returns:
            int:
                Number of columns that are unused.
        """
        return len(self._unused_float_columns)
    
    # ------------------------------------------------------------
    
    @property
    def n_unused_strings(self):
        """
        Number of unused string columns. Unused columns will not be used by the 
        feature engineering algorithms.

        Returns:
            int:
                Number of columns that are unused.
        """
        return len(self._unused_string_columns)

    # ------------------------------------------------------------

    def num_column(self, value):
        """Generates a float or integer column that consists solely of a
        single entry.

        Args:
            value (float): The value to be used.

        Raises:
            TypeError: If any of the input arguments is of wrong type.

        Returns:
            :class:`~getml.data.columns._VirtualFloatColumn`:
                FloatColumn consisting of the singular entry.

        """
        
        if not isinstance(value, numbers.Number):
            raise ValueError("Value must be a number!")
        
        # ------------------------------------------------------------
        
        col = _VirtualFloatColumn(
            df_name=self.name,
            operator="value",
            operand1=value,
            operand2=None
        )
        return col
    
        # ------------------------------------------------------------
    
    @property
    def numerical_names(self):
        """
        List of the names of all numerical columns.

        Returns:
            List[str]:
                List of the names of all numerical columns.
        """
        return [col.name for col in self._numerical_columns]
    
        # ------------------------------------------------------------

    def random(self, seed=5849):
        """
        Create random column.

        The numbers will uniformly distributed from 0.0 to 1.0. This can be
        used to randomly split a population table into a training and a test
        set

        Args:
            seed (int): Seed used for the random number generator.

        Returns:
            :class:`~getml.data.columns._VirtualFloatColumn`:
                FloatColumn containing random numbers

        Example:

            .. code-block:: python
        
                population = getml.data.DataFrame('population')
                population.add(numpy.zeros(100), 'column_01')
                print(len(population))

            .. code-block:: pycon

                100

            .. code-block:: python

                idx = population.random(seed=42)
                population_train = population.where("population_train", idx > 0.7)
                population_test = population.where("population_test", idx <= 0.7)
                print(len(population_train), len(population_test))

            .. code-block:: pycon

                27 73
        """
        
        if not isinstance(seed, numbers.Real):
            raise TypeError("'seed' must be a real number")
            
        # ------------------------------------------------------------
        
        col = _VirtualFloatColumn(
            df_name=self.name,
            operator="random",
            operand1=None,
            operand2=None
        )
        col.thisptr["seed_"] = seed
        return col

    # -------------------------------------------------------------------------- 
    
    def read_csv(
            self,
            fnames,
            append=False,
            quotechar='"',
            sep=',',
            time_formats=["%Y-%m-%dT%H:%M:%s%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]):
        """Read CSV files.

        It is assumed that the first line of each CSV file contains a
        header with the column names.

        Args:
            fnames (List[str]): CSV file paths to be read.
            append (bool, optional):

                If a data frame object holding the same ``name`` is
                already present in the getML, should the content of of
                the CSV files in `fnames` be appended or replace the
                existing data?

            quotechar (str, optional): The character used to wrap strings.
            sep (str, optional): The separator used for separating fields.
            time_formats (List[str], optional):

                The list of formats tried when parsing time stamps.

                The formats are allowed to contain the following
                special characters:

                * %w - abbreviated weekday (Mon, Tue, ...)
                * %W - full weekday (Monday, Tuesday, ...)
                * %b - abbreviated month (Jan, Feb, ...)
                * %B - full month (January, February, ...)
                * %d - zero-padded day of month (01 .. 31)
                * %e - day of month (1 .. 31)
                * %f - space-padded day of month ( 1 .. 31)
                * %m - zero-padded month (01 .. 12)
                * %n - month (1 .. 12)
                * %o - space-padded month ( 1 .. 12)
                * %y - year without century (70)
                * %Y - year with century (1970)
                * %H - hour (00 .. 23)
                * %h - hour (00 .. 12)
                * %a - am/pm
                * %A - AM/PM
                * %M - minute (00 .. 59)
                * %S - second (00 .. 59)
                * %s - seconds and microseconds (equivalent to %S.%F)
                * %i - millisecond (000 .. 999)
                * %c - centisecond (0 .. 9)
                * %F - fractional seconds/microseconds (000000 - 999999)
                * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
                * %Z - time zone differential in RFC format (GMT or +NNNN)
                * %% - percent sign

        Raises:
            TypeError: If any of the input arguments is of wrong type.

        Returns:
            :class:`~getml.data.DataFrame`:

                Handler of the underlying data.

        """

        if not _is_non_empty_typed_list(fnames, str):
            raise TypeError("'fnames' must be either a string or a list of str")
        if type(append) is not bool:
            raise TypeError("'append' must be bool.")
        if type(quotechar) is not str:
            raise TypeError("'quotechar' must be str.")
        if type(sep) is not str:
            raise TypeError("'sep' must be str.")
        if not _is_non_empty_typed_list(time_formats, str):
            raise TypeError("'time_formats' must be a non-empty list of str")

        # ------------------------------------------------------------
       
        if self.n_cols() == 0:
            raise Exception(
                """Reading data is only possible in a DataFrame with more than zero
                columns. You can pre-define columns during
                initialization of the DataFrame or use the classmethod
                from_csv(...).""")
         
        # ------------------------------------------------------------
               
        if not _is_non_empty_typed_list(fnames, str):
            raise TypeError(
                """'fnames' must be a list containing at 
                least one path to a CSV file""")
 
        # ------------------------------------------------------------
        # Transform paths
        
        fnames_ = [os.path.abspath(_) for _ in fnames]

        # ------------------------------------------------------------
        # Send JSON command to getml engine

        cmd = dict()
        cmd["type_"] = "DataFrame.read_csv"
        cmd["name_"] = self.name

        cmd["fnames_"] = fnames_

        cmd["append_"] = append
        cmd["quotechar_"] = quotechar
        cmd["sep_"] = sep
        cmd["time_formats_"] = time_formats

        cmd["categoricals_"] = self.categorical_names
        cmd["join_keys_"] = self.join_key_names
        cmd["numericals_"] = self.numerical_names
        cmd["targets_"] = self.target_names
        cmd["time_stamps_"] = self.time_stamp_names
        cmd["unused_floats_"] = self.unused_float_names 
        cmd["unused_strings_"] = self.unused_string_names
        
        comm.send(cmd)

        # ------------------------------------------------------------

        return self
    
    # -------------------------------------------------------------------------- 
    
    def read_db(self, table_name, append=False):
        """
        Fill from Database.

        The DataFrame will be filled from a table in the database.
        
        Args:
            table_name(str): Table from which we want to retrieve the data.

            append(bool, optional):

                If a data frame object holding the same ``name`` is
                already present in the getML, should the content of
                `table_name` be appended or replace the existing data?

        Raises:
            TypeError: If any of the input arguments is of wrong type.

        Returns:
            :class:`~getml.data.DataFrame`:

                Handler of the underlying data.
        """

        if type(table_name) is not str:
            raise TypeError("'table_name' must be str.")
        if type(append) is not bool:
            raise TypeError("'append' must be bool.")
        
        # ------------------------------------------------------------
       
        if self.n_cols() == 0:
            raise Exception(
                """Reading data is only possible in a DataFrame with more than zero
                columns. You can pre-define columns during
                initialization of the DataFrame or use the classmethod
                from_db(...).""")

        # ------------------------------------------------------------
        # Send JSON command to getml engine

        cmd = dict()
        cmd["type_"] = "DataFrame.from_db"
        cmd["name_"] = self.name
        cmd["table_name_"] = table_name

        cmd["categoricals_"] = self.categorical_names
        cmd["join_keys_"] = self.join_key_names
        cmd["numericals_"] = self.numerical_names
        cmd["targets_"] = self.target_names
        cmd["time_stamps_"] = self.time_stamp_names
        cmd["unused_floats_"] = self.unused_float_names
        cmd["unused_strings_"] = self.unused_string_names 
        
        cmd["append_"] = append
        
        comm.send(cmd)

        # ------------------------------------------------------------

        return self

    # -------------------------------------------------------------------------- 
    
    def read_json(
        self, 
        json_str, 
        append=False, 
        time_formats=[
            "%Y-%m-%dT%H:%M:%s%z", 
            "%Y-%m-%d %H:%M:%S", 
            "%Y-%m-%d"]):
        """Fill from JSON

        Fills the data frame with data from a JSON string. 

        Args:
            json_str (str): The JSON string containing the data.
            append (bool, optional):

                If a data frame object holding the same ``name`` is
                already present in the getML, should the content of
                `json_str` be appended or replace the existing data?

            time_formats (List[str], optional):

                The list of formats tried when parsing time stamps.

                The formats are allowed to contain the following
                special characters:

                * %w - abbreviated weekday (Mon, Tue, ...)
                * %W - full weekday (Monday, Tuesday, ...)
                * %b - abbreviated month (Jan, Feb, ...)
                * %B - full month (January, February, ...)
                * %d - zero-padded day of month (01 .. 31)
                * %e - day of month (1 .. 31)
                * %f - space-padded day of month ( 1 .. 31)
                * %m - zero-padded month (01 .. 12)
                * %n - month (1 .. 12)
                * %o - space-padded month ( 1 .. 12)
                * %y - year without century (70)
                * %Y - year with century (1970)
                * %H - hour (00 .. 23)
                * %h - hour (00 .. 12)
                * %a - am/pm
                * %A - AM/PM
                * %M - minute (00 .. 59)
                * %S - second (00 .. 59)
                * %s - seconds and microseconds (equivalent to %S.%F)
                * %i - millisecond (000 .. 999)
                * %c - centisecond (0 .. 9)
                * %F - fractional seconds/microseconds (000000 - 999999)
                * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
                * %Z - time zone differential in RFC format (GMT or +NNNN)
                * %% - percent sign

        Raises:
            TypeError: If any of the input arguments is of wrong type.

        Returns:
            :class:`~getml.data.DataFrame`:

                Handler of the underlying data.

        """
        
        # ------------------------------------------------------------
       
        if self.n_cols() == 0:
            raise Exception(
                """Reading data is only possible in a DataFrame with more than zero
                columns. You can pre-define columns during
                initialization of the DataFrame or use the classmethod
                from_json(...).""")
        
        # ------------------------------------------------------------
        
        if type(json_str) is not str:
            raise TypeError("'json_str' must be of type str")

        if type(append) is not bool:
            raise TypeError("'append' must be of type bool")
 
        if not _is_non_empty_typed_list(time_formats, str):
            raise TypeError(
                """'time_formats' must be a list of strings 
                containing at least one time format""")

        # ------------------------------------------------------------
        # Send JSON command to getml engine

        cmd = dict()
        cmd["type_"] = "DataFrame.from_json"
        cmd["name_"] = self.name

        cmd["categoricals_"] = self.categorical_names
        cmd["join_keys_"] = self.join_key_names
        cmd["numericals_"] = self.numerical_names
        cmd["targets_"] = self.target_names
        cmd["time_stamps_"] = self.time_stamp_names
        cmd["unused_floats_"] = self.unused_float_names 
        cmd["unused_strings_"] = self.unused_string_names
        
        cmd["append_"] = append
        cmd["time_formats_"] = time_formats

        s = comm.send_and_receive_socket(cmd)

        # ------------------------------------------------------------
        # Send the JSON string

        comm.send_string(s, json_str)

        # ------------------------------------------------------------
        # Make sure everything went well and close
        # connection

        msg = comm.recv_string(s)

        s.close()

        if msg != "Success!":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        return self
    
    # -------------------------------------------------------------------------- 

    def read_pandas(self, pandas_df, append=False):
        """Uploads a :class:`pandas.DataFrame`.

        Replaces the actual content of the underlying data frame in
        the getML engine with `pandas_df`.

        Args:
            pandas_df (:class:`pandas.DataFrame`):

                Data the underlying data frame object in the getML
                engine should obtain.

            append (bool, optional):

                If a data frame object holding the same ``name`` is
                already present in the getML engine, should the content in
                `query` be appended or replace the existing data?
        
        Raises:
            TypeError: If any of the input arguments is of wrong type.

        Returns:
            :class:`~getml.data.DataFrame`:
                Current instance.

        Note:
            For columns containing :class:`pandas.Timestamp` there can
            occur small inconsistencies in the order to microseconds
            when sending the data to the getML engine. This is due to
            the way the underlying information is stored.
        """
        
        if not isinstance(pandas_df, pd.DataFrame):
            raise TypeError("'pandas_df' must be of type pandas.DataFrame.")
        if type(append) is not bool:
            raise TypeError("'append' must be bool.")
        
        # ------------------------------------------------------------
       
        if self.n_cols() == 0:
            raise Exception(
                """Reading data is only possible in a DataFrame with more than zero
                columns. You can pre-define columns during
                initialization of the DataFrame or use the classmethod
                from_pandas(...).""")
        
        # ------------------------------------------------------------

        if append:
            self._append_pandas_df(pandas_df)
        else:
            self._send_pandas_df(pandas_df)
        
        # ------------------------------------------------------------
        
        return self
    
    # -------------------------------------------------------------------------- 

    def read_query(self, query, append=False):
        """Fill from query

        Fills the data frame with data from a table in the database.

        Args:
            query (str): The query used to retrieve the data. 
            append (bool, optional):
                If a data frame object holding the same ``name`` is
                already present in the getML engine, should the content in
                `query` be appended or replace the existing data?

        Raises:
            TypeError: If any of the input arguments is of wrong type.

        Returns:
            :class:`~getml.data.DataFrame`:

                Handler of the underlying data.
        """
        
        # ------------------------------------------------------------
       
        if self.n_cols() == 0:
            raise Exception(
                """Reading data is only possible in a DataFrame with more than zero
                columns. You can pre-define columns during
                initialization of the DataFrame or use the classmethod
                from_db(...).""")
        
        # ------------------------------------------------------------
        
        if type(query) is not str:
            raise TypeError("'query' must be of type str")
        if type(append) is not bool:
            raise TypeError("'append' must be of type bool")

        # ------------------------------------------------------------
        # Send JSON command to getml engine

        cmd = dict()
        cmd["type_"] = "DataFrame.from_query"
        cmd["name_"] = self.name
        cmd["query_"] = query

        cmd["categoricals_"] = self.categorical_names
        cmd["join_keys_"] = self.join_key_names
        cmd["numericals_"] = self.numerical_names
        cmd["targets_"] = self.target_names
        cmd["time_stamps_"] = self.time_stamp_names
        cmd["unused_floats_"] = self.unused_float_names 
        cmd["unused_strings_"] = self.unused_string_names
        
        cmd["append_"] = append
        
        comm.send(cmd)

        # ------------------------------------------------------------

        return self
     
    # -------------------------------------------------------------------------- 

    def refresh(self):
        """Aligns meta-information of the current instance with the
        corresponding data frame in the getML engine.

        This method can be used to avoid encoding conflicts. Note that
        :meth:`~getml.data.DataFrame.load` as well as several other
        methods automatically calls
        :meth:`~getml.data.DataFrame.refresh`.

        Raises:
            Exception:

                If the getML engine does not respond with a valid
                :class:`~getml.data.DataFrame` (which just a
                precaution and not the expected behavior).

        Returns:
            :class:`~getml.data.DataFrame`:

                Updated handle the underlying data frame in the getML
                engine.

        """

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = "DataFrame.refresh"
        cmd["name_"] = self.name

        s = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(s)

        s.close()

        if msg[0] != "{":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        roles = json.loads(msg)

        # ------------------------------------------------------------
        # Reconstruct data frame

        self.__init__(name=self.name, roles=roles)

        # ------------------------------------------------------------

        return self

        # ------------------------------------------------------------

    def rowid(self):
        """
        Get the row numbers of the table.

        Returns:
            :class:`~getml.data.columns._VirtualFloatColumn`:
                (numerical) column containing the row id, starting with 0
        """
        return _VirtualFloatColumn(
            df_name=self.name,
            operator="rowid",
            operand1=None,
            operand2=None
        )

        # ------------------------------------------------------------

    def save(self):
        """Writes the underlying data in the getML engine to disk.
        
        To be stored persistently, the corresponding data frame object
        in the getML engine as to be already created (via
        :meth:`~getml.data.DataFrame.send`).
                
        Returns:
            :class:`~getml.data.DataFrame`:
                The current instance.

        """

        cmd = dict()
        cmd["type_"] = "DataFrame.save"
        cmd["name_"] = self.name

        comm.send(cmd)
        
        return self
 
    # ------------------------------------------------------------

    def rm(self, name):
        """Remove a column.

        The column, identified using its `name`, will be removed both
        from the current instance and the underlying data frame object
        in the getML engine.

        To keep the current instance and the underlying object in the
        getML engine in sync, the
        :meth:`~getml.data.DataFrame.refresh` method will be called
        internally.
        
        Args:
            name (str):

                Name of the column to be removed. Must match exactly
                one column in the current instance.
                
        Returns:
            :class:`~getml.data.DataFrame`:
                Updated version of the current instance.

        """

        # ------------------------------------------------------------
        # Send command

        cmd = dict()
        cmd["type_"] = "DataFrame.remove_column"
        cmd["name_"] = name

        cmd["df_name_"] = self.name

        comm.send(cmd)

        # ------------------------------------------------------------

        self.refresh()

    # ------------------------------------------------------------
    
    def set_role(
            self, 
            names, 
            role, 
            time_formats=[
                "%Y-%m-%dT%H:%M:%s%z", 
                "%Y-%m-%d %H:%M:%S", 
                "%Y-%m-%d"]):
        """Assigns a new role to one or more columns. 

        When switching from a role based on type float to a role based on type
        string or vice verse an implicit type conversions will be conducted.
        The :code:`time_formats` argument is used to interpret :ref:`time
        format string <annotating_roles_time_stamp>`. For more information on
        roles please refer to the :ref:`user guide <annotating>`.

        Args:
            names (str or List[str]): The name or names of the column. 

            role (str): The role to be assigned.

            time_formats (str, optional): Formats to be used to parse the time stamps. 
                This is only necessary, if an implicit conversion from a StringColumn to 
                a time stamp is taking place.

        Raises:
            TypeError: If any of the input arguments is of wrong type.

            ValueError:
                If one of the provided `names` does not correspond to
                an existing column.

        Example:

            .. code-block:: python
        
                data_df = dict(
                    animal=["hawk", "parrot", "goose"],
                    votes=[12341, 5127, 65311],
                    date=["04/06/2019", "01/03/2019", "24/12/2018"])
                df = getml.data.DataFrame.from_dict(data_df, "animal_elections")
                df.set_role(['animal'], getml.data.roles.categorical)
                df.set_role(['votes'], getml.data.roles.numerical)
                df.set_role(['date'], getml.data.roles.time_stamp, time_formats=['%d/%m/%Y'])

                df

            .. code-block:: pycon

                | date                        | animal      | votes     |
                | time stamp                  | categorical | numerical |
                ---------------------------------------------------------
                | 2019-06-04T00:00:00.000000Z | hawk        | 12341     |
                | 2019-03-01T00:00:00.000000Z | parrot      | 5127      |
                | 2018-12-24T00:00:00.000000Z | goose       | 65311     |
        """
        if isinstance(names, str):
            names = [names]

        if type(names) is not list or not (len(names) > 0 and all([type(nn) is str for nn in names])):
            raise TypeError("'names' must be either a string or a list of those")
        if not isinstance(role, str):
            raise TypeError("'role' must be str.")
        if type(time_formats) is not list or not (len(time_formats) > 0 and all([type(nn) is str for nn in time_formats])):
            raise TypeError("'time_formats' must be a non-empty list of str")
        
	# ------------------------------------------------------------
        
        for nname in names:
            if nname not in self.colnames:
                raise ValueError("No column called '"+nname+"' found.")
        if role not in self._possible_keys:
            raise ValueError("'role' must be one of the following values: "+str(self._possible_keys))

	# ------------------------------------------------------------
        
        for name in names:
            self._set_role(name, role, time_formats)
    
    # ------------------------------------------------------------
    
    def set_unit(self, names, unit, comparison_only=False):
        """Assigns a new unit to one or more columns. 

        Args:
            names (str or List[str]): The name or names of the column. 

            unit (str): The unit to be assigned.

            comparison_only (bool): Whether you want the column to
                be used for comparison only. This means that the column can 
                only be used in comparison to other columns of the same unit. 
                
                An example might be a bank account number: The number in itself
                is hardly interesting, but it might be useful to know how often 
                we have seen that same bank account number in another table. 
                
                If True, this will append ", comparison only" to the unit. 
                The feature engineering algorithms and the feature selectors will 
                interpret this accordingly.

        Raises:
            TypeError: If any of the input arguments is of wrong type.

            ValueError:
                If one of the provided `names` does not correspond to
                an existing column.

        """
        
        if isinstance(names, str):
            names = [names]

        if type(names) is not list or not (len(names) > 0 and all([type(nn) is str for nn in names])):
            raise TypeError("'names' must be either a string or a list of those")
        if not isinstance(unit, str):
            raise TypeError("Parameter 'unit' must be a str.")
        
	# ------------------------------------------------------------
        
        for nname in names:
            if nname not in self.numerical_names and nname not in self.categorical_names:
                raise ValueError("No column called '"+nname+"' containing either role getml.data.role.numeric or getml.data.role.categorical found.")

	# ------------------------------------------------------------
        
        if comparison_only:
            unit = unit + ", comparison only"

        for name in names:
            self._set_unit(name, unit)
    
    # ------------------------------------------------------------

    @property 
    def shape(self):
        """
        A tuple containing the number of rows and columns of
        the DataFrame.
        """
        self.refresh()
        return (self.n_rows(), self.n_cols())

    # ------------------------------------------------------------

    def string_column(self, value):
        """
        Generates a string column that consists solely of a single entry.

        Args:
            value (str): The value to be used.

        Returns:
            :class:`~getml.data.columns._VirtualStringColumn`:
                Column consisting of the singular entry.

        Raises:
            TypeError: If any of the input arguments is of wrong type.
        """
        if not isinstance(value, str):
            raise TypeError("Value must be a string!")
        col = _VirtualStringColumn(
            df_name=self.name,
            operator="categorical_value",
            operand1=value,
            operand2=None
        )
        return col

        # ------------------------------------------------------------
    
    @property
    def target_names(self):
        """
        List of the names of all target columns.

        Returns:
            List[str]:
                List of the names of all columns used as target.

        """
        return [col.name for col in self._target_columns]

        # ------------------------------------------------------------
    
    @property
    def time_stamp_names(self):
        """
        List of the names of all time stamps.

        Returns:
            List[str]:
                List of the names of all columns used as time stamp.
        """
        return [col.name for col in self._time_stamp_columns]
    
        # ------------------------------------------------------------
    
    def to_csv(self, fname, quotechar='"', sep=','):
        """
        Writes the underlying data into a newly created CSV file.

        Args:
            fname (str): The name of the CSV file.
            quotechar (str, optional):

                The character used to wrap strings.

            sep (str, optional):

                The character used for separating fields.

        Raises:
            TypeError: If any of the input arguments is of wrong type.
        """
        self.refresh()
       
        if type(fname) is not str:
            raise TypeError("'fname' must be of type str")
        if type(quotechar) is not str:
            raise TypeError("'quotechar' must be of type str")
        if type(sep) is not str:
            raise TypeError("'sep' must be of type str")

        # ------------------------------------------------------------
        # Transform path
        
        fname_ = os.path.abspath(fname)
        
        # ------------------------------------------------------------
        # Build command

        cmd = dict()
        cmd["type_"] = "DataFrame.to_csv"
        cmd["name_"] = self.name

        cmd["fname_"] = fname_ 
        cmd["quotechar_"] = quotechar 
        cmd["sep_"] = sep 

        comm.send(cmd)

        # ------------------------------------------------------------
    
    def to_db(self, table_name):
        """Writes the underlying data into a newly created table in the
        database.

        Args:
            table_name (str):

                Name of the table to be created. 
                
                If a table of that name already exists, it will be
                replaced.

        Raises:
            TypeError: If any of the input arguments is of wrong type.

        """
        self.refresh()
        
        if type(table_name) is not str:
            raise TypeError("'table_name' must be of type str")
        
        # ------------------------------------------------------------
        # Build command

        cmd = dict()
        cmd["type_"] = "DataFrame.to_db"
        cmd["name_"] = self.name

        cmd["table_name_"] = table_name 

        comm.send(cmd)
        
        # ------------------------------------------------------------
    
    def to_json(self):
        """Creates a JSON string from the current instance.

        Loads the underlying data from the getML engine and constructs
        a JSON string.

        Returns:
            str:

                JSON string containing the names of the columns of the
                current instance as keys and their corresponding data
                as values.
        """
        return self.to_pandas().to_json()

    # ----------------------------------------------------------------

    def to_pandas(self):
        """Creates a :py:class:`pandas.DataFrame` from the current instance.

        Loads the underlying data from the getML engine and constructs
        a :class:`pandas.DataFrame`.

        Returns:
            :class:`pandas.DataFrame`:
                Pandas equivalent of the current instance including
                its underlying data.

        """
        self.refresh()

        # ------------------------------------------------------------
        # Send JSON command to getml engine

        cmd = dict()
        cmd["type_"] = "DataFrame.get"
        cmd["name_"] = self.name

        # ------------------------------------------------------------
        # Establish communication with getml engine

        s = comm.send_and_receive_socket(cmd)

        # ------------------------------------------------------------
        # Receive all columns

        df = pd.DataFrame()

        for col in self._categorical_columns:
            df[col.name] = col.to_numpy(s)

        for col in self._join_key_columns:
            df[col.name] = col.to_numpy(s)

        for col in self._numerical_columns:
            df[col.name] = col.to_numpy(s)

        for col in self._target_columns:
            df[col.name] = col.to_numpy(s)

        for col in self._time_stamp_columns:
            df[col.name] = col.to_numpy(s)

        for col in self._unused_float_columns:
            df[col.name] = col.to_numpy(s)

        for col in self._unused_string_columns:
            df[col.name] = col.to_numpy(s)

        # ------------------------------------------------------------
        # Close connection

        self._close(s)

        s.close()

        # ------------------------------------------------------------

        return df
    
    # ----------------------------------------------------------------
    
    def to_placeholder(self):

        """Generates a :class:`~getml.data.Placeholder` from the
        current :class:`~getml.data.DataFrame`.

        The :meth:`~getml.data.DataFrame.refresh` method will be
        called internally to assure the resulting
        :class:`~getml.data.Placeholder` does correspond to the
        latest version of the data frame object on the getML engine.

        Returns:
            :class:`~getml.data.Placeholder`:
                Data model representing the current instance.

        """
        self.refresh()
        return Placeholder(
            name=self.name,
            categorical=self.categorical_names,
            numerical=self.numerical_names,
            join_keys=self.join_key_names,
            time_stamps=self.time_stamp_names,
            targets=self.target_names
        )
    
    # ------------------------------------------------------------
   
    @property 
    def unused_float_names(self):
        """List of the names of all unused float columns.
        Unused columns will not be used by the 
        feature engineering algorithms.
        
        Returns:
            List[str]:
                List of the names of all columns that are unused.

        """
        return [col.name for col in self._unused_float_columns]
    
    # ------------------------------------------------------------
     
    @property
    def unused_names(self):
        """List of the names of all unused columns.
        Unused columns will not be used by the 
        feature engineering algorithms.
        
        Returns:
            List[str]:
                List of the names of all columns that are unused.

        """
        return self.unused_float_names + self.unused_string_names
 
    # ------------------------------------------------------------
    
    @property
    def unused_string_names(self):
        """List of the names of all unused string columns.
        Unused columns will not be used by the 
        feature engineering algorithms.
        
        Returns:
            List[str]:
                List of the names of all columns that are unused.

        """
        return [col.name for col in self._unused_string_columns]
    
    # ------------------------------------------------------------

    def where(self, name, condition):
        """Extract a subset of rows.

        Creates a new :class:`~getml.data.DataFrame` as a
        subselection of the current instance. Internally it creates a
        new data frame object in the getML engine containing only a
        subset of rows of the original one and returns a handler to
        this new object.

        Args: 
            name (str):

                Name of the new, resulting
                :class:`~getml.data.DataFrame`.

            condition (:class:`~getml.data.columns._VirtualBooleanColumn`):
                Boolean column indicating the rows you want to select.

        Raises:
            TypeError: If any of the input arguments is of wrong type.

        Returns:
            :class:`~getml.data.DataFrame`:

                Handler of the newly create data frame contain just a
                subset of rows of the current instance.

        Example:

            Generate example data:

            .. code-block:: python

                data = dict(
                    fruit=["banana", "apple", "cherry", "cherry", "melon", "pineapple"],
                    price=[2.4, 3.0, 1.2, 1.4, 3.4, 3.4],
                    join_key=["0", "1", "2", "2", "3", "3"])

                fruits = getml.data.DataFrame.from_dict(data, name="fruits",
                roles={"categorical": ["fruit"], "join_key": ["join_key"], "numerical": ["price"]})

                fruits

            .. code-block:: pycon

                | join_key | fruit       | price     |
                | join key | categorical | numerical |
                --------------------------------------
                | 0        | banana      | 2.4       |
                | 1        | apple       | 3         |
                | 2        | cherry      | 1.2       |
                | 2        | cherry      | 1.4       |
                | 3        | melon       | 3.4       |
                | 3        | pineapple   | 3.4       |
        
            Apply where condition. This creates a new DataFrame called "cherries":

            .. code-block:: python

                cherries = fruits.where(
                    name="cherries", 
                    condition=(fruits["fruit"] == "cherry")
                )

                cherries

            .. code-block:: pycon

                | join_key | fruit       | price     |
                | join key | categorical | numerical |
                --------------------------------------
                | 2        | cherry      | 1.2       |
                | 2        | cherry      | 1.4       |
        """
        
        if type(name) is not str:
            raise TypeError("'name' must be of type str")
        if not isinstance(condition, _VirtualBooleanColumn):
            raise TypeError("'condition' must be of type getml.data.columns._VirtualBooleanColumn")

        # ------------------------------------------------------------
        # Build command

        cmd = dict()
        cmd["type_"] = "DataFrame.where"
        cmd["name_"] = self.name

        cmd["new_df_"] = name
        cmd["condition_"] = condition.thisptr

        comm.send(cmd)

        # ------------------------------------------------------------
        # Create handle for new data frame.

        new_df = DataFrame(name)

        return new_df.refresh()

# --------------------------------------------------------------------

def list_data_frames():
    """Lists all available data frames of the project.

    Examples:

        .. code-block:: python

            d, _ = getml.datasets.make_numerical()
            getml.data.list_data_frames()
            d.save()
            getml.data.list_data_frames()

    Raises:
        IOError:

            If an error in the communication with the getML engine
            occurred.

    Returns:
        dict:

            Dict containing lists of strings representing the names of
            the data frames objects

            * 'in_memory'
                held in memory (RAM).
            * 'in_project_folder'
                stored on disk.

    Note:

        All data listed in 'in_memory' will be lost when switching
        the project using :func:`~getml.engine.set_project` or
        restarting the getML engine whereas those in
        'in_project_folder' is persistent.

    """

    cmd = dict()
    cmd["type_"] = "list_data_frames"
    cmd["name_"] = ""
    
    s = comm.send_and_receive_socket(cmd)

    msg = comm.recv_string(s)

    if msg != "Success!":
        comm.engine_exception_handler(msg)
    
    json_str = comm.recv_string(s) 
    
    s.close() 

    return json.loads(json_str)

# --------------------------------------------------------------------

def load_data_frame(name):
    """Retrieves a :class:`~getml.data.DataFrame` handler of data in the
    getML engine.

    A data frame object can be loaded regardless if it is held in
    memory (accessible through the 'Data Frames' tab in the getML
    monitor) or not. It only has to be present in the current project
    and thus listed in the output of
    :func:`~getml.data.list_data_frames`.

    Args:
        name (str):
            Name of the data frame object present in the getML engine.

    Examples:

        .. code-block:: python

            d, _ = getml.datasets.make_numerical(population_name = 'test')
            d2 = getml.data.load_data_frame('test')


    Raises:
        TypeError: If any of the input arguments is of wrong type.

        ValueError:

            If `name` does not corresponding to a data frame on the
            engine.

    Returns:
        :class:`~getml.data.DataFrame`:
            Handle the underlying data frame in the getML engine.

    Note:

        The getML engine knows to different states of a data frame
        object. Firstly, the current instance in memory (RAM) that
        holds the most recent changes applied via the Python API
        (listed under the 'in_memory' key of
        :func:`~getml.data.list_data_frames`) and, secondly, the
        version stored to disk by calling the
        :meth:`~getml.data.DataFrame.save` method (listed under the
        'in_project_folder' key). If a data frame object corresponding
        to `name` is present in both of them, the most recent version
        held in memory is loaded. To load the one from memory instead,
        you use the :meth:`~getml.data.DataFrame.load` method.

        In order to load a data frame object from a different project,
        you have to switch projects first. Caution: any changes
        applied after the last call to
        :meth:`~getml.data.DataFrame.save` will be lost. See
        :func:`~getml.engine.set_project` and
        :class:`~getml.data.DataFrame` for more details about the
        lifecycles of the models.

    """
        
    if type(name) is not str:
        raise TypeError("'name' must be of type str")
    
    data_frames_available = list_data_frames()
    
    # First, attempt to load a data frame held in memory.
    if name in data_frames_available['in_memory']:
        return DataFrame(name).refresh()
    
    elif name in data_frames_available['in_project_folder']:
        # Next, try to read the data frame from disk.
        return DataFrame(name).load()
    
    else:
        raise ValueError("No data frame holding the name '"+name+"' present on the getML engine")
