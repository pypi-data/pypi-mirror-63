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

"""Handlers for 1-d arrays storing the data of an individual variable.

Like the :class:`~getml.data.DataFrame`, the
:mod:`~getml.data.columns` do not contain any actual data themselves
but are only handlers to objects within the getML engine. These
containers store data of a single variable in a one-dimensional array
of an uniform type. The engine differs between two of them: numerical
and everything else. Both are represented in the Python API using the
:class:`~getml.data.columns.FloatColumn` and
:class:`~getml.data.columns.StringColumn` classes. A column, however,
can not live in the engine on its own but always has to be bundled in
a data frame object.

Note:

    All :mod:`~getml.data.columns` are immutable and, thus, their
    content can not be changed directly. All operations altering the
    underlying data will return a new column, which is purely virtual
    and has to be added to the :class:`~getml.data.DataFrame` using
    its :meth:`~getml.data.DataFrame.add` method.

    Each of the classes provides a set of data preparation
    methods. They are still experimental (and, therefore, not covered
    in the main documentation) yet but nevertheless widely tested and
    used internally. Only their signatures might change significantly
    in following releases.

"""

import copy
import json
import numbers

import numpy as np
import pandas as pd

import getml.communication as comm

# ------------------------------------------------------------------------------

class _Column(object):
    """
    Base object not meant to be called directly.
    """

    # -------------------------------------------------------------------------

    def __init__(self):
        self.thisptr = dict()
      
    # -----------------------------------------------------------------------------
    
    def __repr__(self):
        return str(self)
    
    # -------------------------------------------------------------------------
    
    @property
    def name(self):
        """
        The role of this column. 
        """
        return self.thisptr["name_"]
    
    # -------------------------------------------------------------------------
    
    @property
    def role(self):
        """
        The role of this column.
        
        Roles are needed by the feature engineering algorithm so it knows how 
        to treat the columns. 
        """
        return self.thisptr["role_"]
    
    # -------------------------------------------------------------------------
    
    @property 
    def unit(self):
        """
        The unit of this column.

        Units are used to determine which columns can be compared to each other
        by the feature engineering algorithms.
        """
    
        # -------------------------------------------
        # Build command string

        cmd = dict()

        cmd.update(self.thisptr)

        cmd["type_"] += ".get_unit"

        # -------------------------------------------
        # Send JSON command to engine

        s = comm.send_and_receive_socket(cmd)
    
        # -------------------------------------------
        # Make sure everything went well

        msg = comm.recv_string(s)

        if msg != "Success!":
            comm.engine_exception_handler(msg)
        
        # -------------------------------------------
    
        unit = comm.recv_string(s)

        return unit 

# ------------------------------------------------------------------------------

class _Aggregation(object):
    def __init__(
        self,
        alias,
        col,
        type
    ):
        self.thisptr = dict()
        self.thisptr["as_"] = alias
        self.thisptr["col_"] = col.thisptr
        self.thisptr["type_"] = type

    # -----------------------------------------------------------------------------
    
    def __repr__(self):
        return str(self)
    
    # -----------------------------------------------------------------------------
    
    def __str__(self):
        val = self.get()
        return self.thisptr["type_"].upper() + " aggregation, value: " + str(val) + "." 

    # --------------------------------------------------------------------------

    def get(self):
        """
        Receives the value of the aggregation over the column.
        """

        # -------------------------------------------
        # Build command string

        cmd = dict()

        cmd["name_"] = ""
        cmd["type_"] = "FloatColumn.aggregate"

        cmd["aggregation_"] = self.thisptr
        cmd["df_name_"] = self.thisptr["col_"]["df_name_"]

        # -------------------------------------------
        # Create connection and send the command

        s = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(s)

        # -------------------------------------------
        # Make sure everything went well, receive data
        # and close connection

        if msg != "Success!":
            s.close()
            comm.engine_exception_handler(msg)

        mat = comm.recv_matrix(s)

        # -------------------------------------------
        # Close connection.

        s.close()

        # -------------------------------------------

        return mat.ravel()[0]

# -----------------------------------------------------------------------------

class _VirtualBooleanColumn(object):

    def __init__(
        self,
        df_name,
        operator,
        operand1,
        operand2
    ):
        self.thisptr = dict()

        self.thisptr["df_name_"] = df_name

        self.thisptr["type_"] = "VirtualBooleanColumn"

        self.thisptr["operator_"] = operator

        self.thisptr["operand1_"] = self._parse_operand(operand1)

        if operand2 is not None:
            self.thisptr["operand2_"] = self._parse_operand(operand2)

    # -----------------------------------------------------------------------------

    def __and__(self, other):
        return _VirtualBooleanColumn(
            df_name=self.thisptr["df_name_"],
            operator="and",
            operand1=self,
            operand2=other
        )

    # -----------------------------------------------------------------------------

    def __eq__(self, other):
        return _VirtualBooleanColumn(
            df_name=self.thisptr["df_name_"],
            operator="equal_to",
            operand1=self,
            operand2=other
        )

    # -----------------------------------------------------------------------------

    def __or__(self, other):
        return _VirtualBooleanColumn(
            df_name=self.thisptr["df_name_"],
            operator="or",
            operand1=self,
            operand2=other
        )

    # -----------------------------------------------------------------------------

    def __ne__(self, other):
        return _VirtualBooleanColumn(
            df_name=self.thisptr["df_name_"],
            operator="not_equal_to",
            operand1=self,
            operand2=other
        )

    # -----------------------------------------------------------------------------
    
    def __repr__(self):
        return str(self)
    
    # -----------------------------------------------------------------------------
    
    def __str__(self):

        # -------------------------------------------
        # Build command string

        cmd = dict()

        cmd["name_"] = self.thisptr["df_name_"]
        cmd["type_"] = "BooleanColumn.get_string"

        cmd["col_"] = self.thisptr

        # -------------------------------------------
        # Send command to engine
        
        s = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(s)

        # -------------------------------------------
        # Make sure everything went well, receive data
        # and close connection

        if msg != "Success!":
            comm.engine_exception_handler(msg)

        cstring = comm.recv_string(s)
        
        s.close()

        # -------------------------------------------

        return cstring

    # -----------------------------------------------------------------------------

    def __xor__(self, other):
        return _VirtualBooleanColumn(
            df_name=self.thisptr["df_name_"],
            operator="xor",
            operand1=self,
            operand2=other
        )
    
    # -----------------------------------------------------------------------------

    def _parse_operand(self, operand):

        if isinstance(operand, bool):
            return {"type_": "BooleanValue", "value_": operand}

        elif isinstance(operand, str):
            return {"type_": "CategoricalValue", "value_": operand}

        elif isinstance(operand, numbers.Number):
            return {"type_": "Value", "value_": operand}

        else:
            if self.thisptr["operator_"] in ["and", "or", "not", "xor"]:
                if operand.thisptr["type_"] != "VirtualBooleanColumn":
                    raise TypeError("This operator can only be applied to a BooleanColumn!")

        return operand.thisptr
    
    # -----------------------------------------------------------------------------

    def to_numpy(self):
        """
        Transform column to numpy array
        """

        # -------------------------------------------
        # Build command string

        cmd = dict()

        cmd["name_"] = self.thisptr["df_name_"]
        cmd["type_"] = "BooleanColumn.get"

        cmd["col_"] = self.thisptr

        # -------------------------------------------
        # Send command to engine

        s = comm.send_and_receive_socket(cmd)

        msg = comm.recv_string(s)

        # -------------------------------------------
        # Make sure everything went well, receive data
        # and close connection

        if msg != "Found!":
            s.close()
            comm.engine_exception_handler(msg)

        mat = comm.recv_boolean_matrix(s)

        # -------------------------------------------
        # Close connection, if necessary.

        s.close()

        # -------------------------------------------

        return mat.ravel()

    # -----------------------------------------------------------------------------

    def is_false(self):
        """Whether an entry is False - effectively inverts the Boolean column."""
        return _VirtualBooleanColumn(
            df_name=self.thisptr["df_name_"],
            operator="not",
            operand1=self,
            operand2=None
        )

    # -----------------------------------------------------------------------------
    
    def as_num(self):
        """Transforms the boolean column into a numerical column"""
        return _VirtualFloatColumn(
            df_name=self.thisptr["df_name_"],
            operator="boolean_as_num",
            operand1=self,
            operand2=None
        )

# -----------------------------------------------------------------------------

class StringColumn(_Column):
    """Handle for categorical data that is kept in the getML engine

    Args:
        name (str, optional): Name of the categorical column.
        role (str, optional): Role that the column plays.
        num (int, optional): Number of the column.
        df_name (str, optional): 

            ``name`` instance variable of the
            :class:`~getml.data.DataFrame` containing this column.

    Note:

        All :class:`~getml.data.columns.StringColumn` are immutable
        and, thus, their content can not be changed directly. All
        operations altering the underlying data will return a new
        column, which is purely virtual and has to be added to the
        :class:`~getml.data.DataFrame` using its
        :meth:`~getml.data.DataFrame.add` method.

        This class provides a set of data preparation methods. They
        are still experimental (and, therefore, not covered in the
        main documentation) yet but nevertheless widely tested and
        used internally. Only their signatures might change
        significantly in following releases.

    """

    num_categorical_matrices = 0

    def __init__(
        self,
        name="",
        role="categorical",
        num=0,
        df_name=""
    ):

        super(StringColumn, self).__init__()

        StringColumn.num_categorical_matrices += 1
        if name == "":
            name = "StringColumn " + \
                str(StringColumn.num_categorical_matrices)

        self.thisptr = dict()

        self.thisptr["df_name_"] = df_name

        self.thisptr["name_"] = name

        self.thisptr["role_"] = role

        self.thisptr["type_"] = "StringColumn"

# -----------------------------------------------------------------------------

class _VirtualStringColumn(object):

    def __init__(
        self,
        df_name,
        operator,
        operand1,
        operand2
    ):
        self.thisptr = dict()

        self.thisptr["df_name_"] = df_name

        self.thisptr["type_"] = "VirtualStringColumn"

        self.thisptr["operator_"] = operator

        if operand1 is not None:
            self.thisptr["operand1_"] = self._parse_operand(operand1)

        if operand2 is not None:
            self.thisptr["operand2_"] = self._parse_operand(operand2)

    # -----------------------------------------------------------------------------

    def _parse_operand(self, operand):
 
        if isinstance(operand, str):
            return {"type_": "CategoricalValue", "value_": operand}

        else:
            op = self.thisptr["operator_"]
            optype = operand.thisptr["type_"]

            if op == "as_str": 
                wrong_coltype = (optype not in [
                    "FloatColumn",
                    "VirtualFloatColumn",
                    "VirtualBooleanColumn"
                ])  
                if wrong_coltype:
                    raise TypeError(
                        "This operator can only be applied to a FloatColumn or a BooleanColumn!")
            
            else: 
                wrong_coltype = (optype not in [
                    "StringColumn",
                    "VirtualStringColumn"
                ]) 
                if wrong_coltype:
                    raise TypeError(
                        "This operator can only be applied to a StringColumn!")

            return operand.thisptr

    # -----------------------------------------------------------------------------
    
    def __repr__(self):
        return str(self)

# -----------------------------------------------------------------------------


class FloatColumn(_Column):
    """Handler for numerical data in the engine.

    This is a handler for all numerical data in the getML engine,
    including time stamps.

    Args:
        name (str, optional): Name of the categorical column.
        role (str, optional): Role that the column plays.
        num (int, optional): Number of the column.
        df_name (str, optional): 

            ``name`` instance variable of the
            :class:`~getml.data.DataFrame` containing this column.

    Note:

        All :class:`~getml.data.columns.FloatColumn` are immutable
        and, thus, their content can not be changed directly. All
        operations altering the underlying data will return a new
        column, which is purely virtual and has to be added to the
        :class:`~getml.data.DataFrame` using its
        :meth:`~getml.data.DataFrame.add` method.

        This class provides a set of data preparation methods. They
        are still experimental (and, therefore, not covered in the
        main documentation) yet but nevertheless widely tested and
        used internally. Only their signatures might change
        significantly in following releases.

    """

    num_columns = 0

    def __init__(
        self,
        name="",
        role="numerical",
        num=0,
        df_name=""
    ):

        super(FloatColumn, self).__init__()

        FloatColumn.num_columns += 1
        if name == "":
            name = "FloatColumn " + \
                str(FloatColumn.num_columns)

        self.thisptr = dict()

        self.thisptr["df_name_"] = df_name

        self.thisptr["name_"] = name

        self.thisptr["role_"] = role

        self.thisptr["type_"] = "FloatColumn"

# -----------------------------------------------------------------------------

class _VirtualFloatColumn(object):

    def __init__(
        self,
        df_name,
        operator,
        operand1,
        operand2
    ):
        self.thisptr = dict()

        self.thisptr["df_name_"] = df_name

        self.thisptr["type_"] = "VirtualFloatColumn"

        self.thisptr["operator_"] = operator

        if operand1 is not None:
            self.thisptr["operand1_"] = self._parse_operand(operand1)

        if operand2 is not None:
            self.thisptr["operand2_"] = self._parse_operand(operand2)

    # -----------------------------------------------------------------------------

    def _parse_operand(self, operand):

        if isinstance(operand, numbers.Number):
            return {"type_": "Value", "value_": operand}

        else:
            special_ops = ["as_num", "as_ts", "boolean_as_num"]
            op = self.thisptr["operator_"]
            optype = operand.thisptr["type_"]

            if op not in special_ops:
                wrong_coltype = (optype not in [
                    "FloatColumn",
                    "VirtualFloatColumn"
                ])
                if wrong_coltype:
                    raise TypeError(
                        "This operator can only be applied to a FloatColumn!")

            if op in special_ops and op != "boolean_as_num": 
                wrong_coltype = (optype not in [
                    "StringColumn",
                    "VirtualStringColumn"
                ]) 
                if wrong_coltype:
                    raise TypeError(
                        "This operator can only be applied to a StringColumn!")

            if op == "boolean_as_num" and optype != "VirtualBooleanColumn":
                raise TypeError(
                    "This operator can only be applied to a BooleanColumn!")
            
            return operand.thisptr

    # -----------------------------------------------------------------------------
    
    def __repr__(self):
        return str(self)

# -----------------------------------------------------------------------------

def _abs(self):
    """Compute absolute value."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="abs",
        operand1=self,
        operand2=None
    )

FloatColumn.abs = _abs
_VirtualFloatColumn.abs = _abs

# -----------------------------------------------------------------------------

def _acos(self):
    """Compute arc cosine."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="acos",
        operand1=self,
        operand2=None
    )

FloatColumn.acos = _acos
_VirtualFloatColumn.acos = _acos

# -----------------------------------------------------------------------------

def _add(self, other):
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="plus",
        operand1=self,
        operand2=other
    )

FloatColumn.__add__ = _add
FloatColumn.__radd__ = _add

_VirtualFloatColumn.__add__ = _add
_VirtualFloatColumn.__radd__ = _add

# -----------------------------------------------------------------------------

def _alias(self, alias):
    """
    Adds an alias to the column. This is useful for joins.

    Args:
        alias (str): The name of the column as it should appear in the new DataFrame.
    """
    col = copy.deepcopy(self)
    col.thisptr["as_"] = alias
    return col

StringColumn.alias = _alias
FloatColumn.alias = _alias

# -----------------------------------------------------------------------------

def _assert_equal(self, alias="new_column"):
    """
    ASSERT EQUAL aggregation.

    Throws an exception if not all values inserted
    into the aggregation are equal.

    Args:
        alias (str): Name for the new column.
    """
    return _Aggregation(alias, self, "assert_equal")

FloatColumn.assert_equal = _assert_equal
_VirtualFloatColumn.assert_equal = _assert_equal


# -----------------------------------------------------------------------------

def _asin(self):
    """Compute arc sine."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="asin",
        operand1=self,
        operand2=None
    )

FloatColumn.asin = _asin
_VirtualFloatColumn.asin = _asin

# -----------------------------------------------------------------------------

def _atan(self):
    """Compute arc tangent."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="atan",
        operand1=self,
        operand2=None
    )

FloatColumn.atan = _atan
_VirtualFloatColumn.atan = _atan

# -----------------------------------------------------------------------------

def _avg(self, alias="new_column"):
    """
    AVG aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return _Aggregation(alias, self, "avg")

FloatColumn.avg = _avg
_VirtualFloatColumn.avg = _avg

# -----------------------------------------------------------------------------

def _cbrt(self):
    """Compute cube root."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="cbrt",
        operand1=self,
        operand2=None
    )

FloatColumn.cbrt = _cbrt
_VirtualFloatColumn.cbrt = _cbrt


# -----------------------------------------------------------------------------

def _ceil(self):
    """Round up value."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="ceil",
        operand1=self,
        operand2=None
    )

FloatColumn.ceil = _ceil
_VirtualFloatColumn.ceil = _ceil

# -----------------------------------------------------------------------------

def _concat(self, other):
    return _VirtualStringColumn(
        df_name=self.thisptr["df_name_"],
        operator="concat",
        operand1=self,
        operand2=other
    )

def _rconcat(self, other):
    return _VirtualStringColumn(
        df_name=self.thisptr["df_name_"],
        operator="concat",
        operand1=other,
        operand2=self
    )

StringColumn.__add__ = _concat
StringColumn.__radd__ = _rconcat

_VirtualStringColumn.__add__ = _concat
_VirtualStringColumn.__radd__ = _rconcat

# -----------------------------------------------------------------------------

def _contains(self, other):
    """
    Returns a boolean column indicating whether a
    string or column entry is contained in the corresponding
    entry of the other column.
    """
    return _VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="contains",
        operand1=self,
        operand2=other
    )

StringColumn.contains = _contains

_VirtualStringColumn.contains = _contains

# -----------------------------------------------------------------------------

def _cos(self):
    """Compute cosine."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="cos",
        operand1=self,
        operand2=None
    )

FloatColumn.cos = _cos
_VirtualFloatColumn.cos = _cos

# -----------------------------------------------------------------------------

def _count(self, alias="new_column"):
    """
    COUNT aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return _Aggregation(alias, self, "count")

FloatColumn.count = _count
_VirtualFloatColumn.count = _count

# -----------------------------------------------------------------------------

def _count_categorical(self, alias="new_column"):
    """
    COUNT aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return _Aggregation(alias, self, "count_categorical")


StringColumn.count = _count_categorical
_VirtualStringColumn.count = _count_categorical

# -----------------------------------------------------------------------------

def _count_distinct(self, alias="new_column"):
    """
    COUNT DISTINCT aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return _Aggregation(alias, self, "count_distinct")

StringColumn.count_distinct = _count_distinct
_VirtualStringColumn.count_distinct = _count_distinct

# -----------------------------------------------------------------------------

def _day(self):
    """Extract day (of the month) from a time stamp.

    If the column is numerical, that number will be interpreted as the
    number of days since epoch time (January 1, 1970).

    """
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="day",
        operand1=self,
        operand2=None
    )

FloatColumn.day = _day
_VirtualFloatColumn.day = _day

# -----------------------------------------------------------------------------

def _eq(self, other):
    return _VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="equal_to",
        operand1=self,
        operand2=other
    )

FloatColumn.__eq__ = _eq
_VirtualFloatColumn.__eq__ = _eq

StringColumn.__eq__ = _eq
_VirtualStringColumn.__eq__ = _eq

# -----------------------------------------------------------------------------

def _erf(self):
    """Compute error function."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="erf",
        operand1=self,
        operand2=None
    )

FloatColumn.erf = _erf
_VirtualFloatColumn.erf = _erf

# -----------------------------------------------------------------------------

def _exp(self):
    """Compute exponential function."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="exp",
        operand1=self,
        operand2=None
    )

FloatColumn.exp = _exp
_VirtualFloatColumn.exp = _exp

# -----------------------------------------------------------------------------

def _floor(self):
    """Round down value."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="floor",
        operand1=self,
        operand2=None
    )

FloatColumn.floor = _floor
_VirtualFloatColumn.floor = _floor

# -----------------------------------------------------------------------------

def _gamma(self):
    """Compute gamma function."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="tgamma",
        operand1=self,
        operand2=None
    )

FloatColumn.gamma = _gamma
_VirtualFloatColumn.gamma = _gamma

# -----------------------------------------------------------------------------

def _ge(self, other):
    return _VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="greater_equal",
        operand1=self,
        operand2=other
    )

FloatColumn.__ge__ = _ge
_VirtualFloatColumn.__ge__ = _ge

# -----------------------------------------------------------------------------

def _get_float_column_string(self):

    # -------------------------------------------
    # Build command string

    cmd = dict()

    cmd["name_"] = self.thisptr["df_name_"]
    cmd["type_"] = "FloatColumn.get_string"

    cmd["col_"] = self.thisptr

    # -------------------------------------------
    # Send command to engine
    
    s = comm.send_and_receive_socket(cmd)

    msg = comm.recv_string(s)

    # -------------------------------------------
    # Make sure everything went well, receive data
    # and close connection

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    cstring = comm.recv_string(s)
    
    s.close()

    # -------------------------------------------

    return cstring

FloatColumn.__str__ = _get_float_column_string 
_VirtualFloatColumn.__str__ = _get_float_column_string

# -----------------------------------------------------------------------------

def _get_string_column_string(self):

    # -------------------------------------------
    # Build command string

    cmd = dict()

    cmd["name_"] = self.thisptr["df_name_"]
    cmd["type_"] = "StringColumn.get_string"

    cmd["col_"] = self.thisptr

    # -------------------------------------------
    # Send command to engine
    
    s = comm.send_and_receive_socket(cmd)

    msg = comm.recv_string(s)

    # -------------------------------------------
    # Make sure everything went well, receive data
    # and close connection

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    cstring = comm.recv_string(s)
    
    s.close()

    # -------------------------------------------

    return cstring

StringColumn.__str__ = _get_string_column_string 
_VirtualStringColumn.__str__ = _get_string_column_string

# -----------------------------------------------------------------------------

def _gt(self, other):
    return _VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="greater",
        operand1=self,
        operand2=other
    )

FloatColumn.__gt__ = _gt
_VirtualFloatColumn.__gt__ = _gt

# -----------------------------------------------------------------------------

def _hour(self):
    """Extract hour (of the day) from a time stamp.

    If the column is numerical, that number will be interpreted as the
    number of days since epoch time (January 1, 1970).

    """
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="hour",
        operand1=self,
        operand2=None
    )

FloatColumn.hour = _hour
_VirtualFloatColumn.hour = _hour

# -----------------------------------------------------------------------------

def _is_inf(self):
    """Determine whether the value is infinite."""
    return _VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="is_inf",
        operand1=self,
        operand2=None
    )

FloatColumn.is_inf = _is_inf
_VirtualFloatColumn.is_inf = _is_inf

# -----------------------------------------------------------------------------

def _is_nan(self):
    """Determine whether the value is nan."""
    return _VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="is_nan",
        operand1=self,
        operand2=None
    )

FloatColumn.is_nan = _is_nan
_VirtualFloatColumn.is_nan = _is_nan

# -----------------------------------------------------------------------------

def _le(self, other):
    return _VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="less_equal",
        operand1=self,
        operand2=other
    )

FloatColumn.__le__ = _le
_VirtualFloatColumn.__le__ = _le

# -----------------------------------------------------------------------------

def _length(self):
    """The length of the column. 
       This is identical to the result of the nrows() method of the DataFrame
       containing this column.
       Alternatively, you can call len(...).
    """

    # ------------------------------------------------------------
    # Build and send JSON command

    cmd = dict()
    cmd["type_"] = "DataFrame.nrows"
    cmd["name_"] = self.thisptr["df_name_"]

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

_VirtualBooleanColumn.__len__ = _length
_VirtualFloatColumn.__len__ = _length
_VirtualStringColumn.__len__ = _length
FloatColumn.__len__ = _length
StringColumn.__len__ = _length

#  -----------------------------------------------------------------------------

@property
def _length_property(self):
    return len(self)

_VirtualBooleanColumn.length = _length_property
_VirtualFloatColumn.length = _length_property
_VirtualStringColumn.length = _length_property
FloatColumn.length = _length_property
StringColumn.length = _length_property

#  -----------------------------------------------------------------------------

def _lgamma(self):
    """Compute log-gamma function."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="lgamma",
        operand1=self,
        operand2=None
    )

FloatColumn.lgamma = _lgamma
_VirtualFloatColumn.lgamma = _lgamma

# -----------------------------------------------------------------------------

def _log(self):
    """Compute natural logarithm."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="log",
        operand1=self,
        operand2=None
    )

FloatColumn.log = _log
_VirtualFloatColumn.log = _log

# -----------------------------------------------------------------------------

def _lt(self, other):
    return _VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="less",
        operand1=self,
        operand2=other
    )

FloatColumn.__lt__ = _lt
_VirtualFloatColumn.__lt__ = _lt

# -----------------------------------------------------------------------------

def _max(self, alias="new_column"):
    """
    MAX aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return _Aggregation(alias, self, "max")

FloatColumn.max = _max
_VirtualFloatColumn.max = _max

# -----------------------------------------------------------------------------

def _median(self, alias="new_column"):
    """
    MEDIAN aggregation.

    **alias**: Name for the new column.
    """
    return _Aggregation(alias, self, "median")

FloatColumn.median = _median
_VirtualFloatColumn.median = _median

# -----------------------------------------------------------------------------

def _min(self, alias="new_column"):
    """
    MIN aggregation.

    **alias**: Name for the new column.
    """
    return _Aggregation(alias, self, "min")

FloatColumn.min = _min
_VirtualFloatColumn.min = _min

# -----------------------------------------------------------------------------

def _minute(self):
    """Extract minute (of the hour) from a time stamp.

    If the column is numerical, that number will be interpreted as the
    number of days since epoch time (January 1, 1970).

    """
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="minute",
        operand1=self,
        operand2=None
    )

FloatColumn.minute = _minute
_VirtualFloatColumn.minute = _minute

# -----------------------------------------------------------------------------

def _mod(self, other):
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="fmod",
        operand1=self,
        operand2=other
    )

def _rmod(self, other):
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="fmod",
        operand1=other,
        operand2=self
    )

FloatColumn.__mod__ = _mod
FloatColumn.__rmod__ = _rmod

_VirtualFloatColumn.__mod__ = _mod
_VirtualFloatColumn.__rmod__ = _rmod

# -----------------------------------------------------------------------------

def _month(self):
    """
    Extract month from a time stamp.

    If the column is numerical, that number will be interpreted
    as the number of days since epoch time (January 1, 1970).
    """
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="month",
        operand1=self,
        operand2=None
    )

FloatColumn.month = _month
_VirtualFloatColumn.month = _month

# -----------------------------------------------------------------------------

def _mul(self, other):
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="multiplies",
        operand1=self,
        operand2=other
    )

FloatColumn.__mul__ = _mul
FloatColumn.__rmul__ =_mul

_VirtualFloatColumn.__mul__ = _mul
_VirtualFloatColumn.__rmul__ = _mul


# -----------------------------------------------------------------------------

def _ne(self, other):
    return _VirtualBooleanColumn(
        df_name=self.thisptr["df_name_"],
        operator="not_equal_to",
        operand1=self,
        operand2=other
    )

FloatColumn.__ne__ = _ne
_VirtualFloatColumn.__ne__ = _ne

StringColumn.__ne__ = _ne
_VirtualStringColumn.__ne__ = _ne

# -----------------------------------------------------------------------------

def _neg(self):
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="multiplies",
        operand1=self,
        operand2=-1.0
    )

FloatColumn.__neg__ = _neg
_VirtualFloatColumn.__neg__ = _neg

# -----------------------------------------------------------------------------

def _pow(self, other):
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="pow",
        operand1=self,
        operand2=other
    )

def _rpow(self, other):
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="pow",
        operand1=other,
        operand2=self
    )

FloatColumn.__pow__ = _pow
FloatColumn.__rpow__ = _rpow

_VirtualFloatColumn.__pow__ = _pow
_VirtualFloatColumn.__rpow__ = _rpow

# -----------------------------------------------------------------------------

def _round(self):
    """Round to nearest."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="round",
        operand1=self,
        operand2=None
    )

FloatColumn.round = _round
_VirtualFloatColumn.round = _round

# -----------------------------------------------------------------------------

def _second(self):
    """Extract second (of the minute) from a time stamp.

    If the column is numerical, that number will be interpreted as the
    number of days since epoch time (January 1, 1970).

    """
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="second",
        operand1=self,
        operand2=None
    )

FloatColumn.second = _second
_VirtualFloatColumn.second = _second

# -----------------------------------------------------------------------------

def _sin(self):
    """Compute sine."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="sin",
        operand1=self,
        operand2=None
    )

FloatColumn.sin = _sin
_VirtualFloatColumn.sin = _sin

# -----------------------------------------------------------------------------

def _sqrt(self):
    """Compute square root."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="sqrt",
        operand1=self,
        operand2=None
    )

FloatColumn.sqrt = _sqrt
_VirtualFloatColumn.sqrt = _sqrt

# -----------------------------------------------------------------------------

def _stddev(self, alias="new_column"):
    """
    STDDEV aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return _Aggregation(alias, self, "stddev")

FloatColumn.stddev = _stddev
_VirtualFloatColumn.stddev = _stddev

# -----------------------------------------------------------------------------

def _sub(self, other):
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="minus",
        operand1=self,
        operand2=other
    )

def _rsub(self, other):
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="minus",
        operand1=other,
        operand2=self
    )

FloatColumn.__sub__ = _sub
FloatColumn.__rsub__ = _rsub

_VirtualFloatColumn.__sub__ = _sub
_VirtualFloatColumn.__rsub__ = _rsub


# -----------------------------------------------------------------------------

def _substr(self, begin, length):
    """
    Return a substring for every element in the column.

    Args:
        begin (int): First position of the original string.
        length (int): Length of the extracted string.
    """
    col = _VirtualStringColumn(
        df_name=self.thisptr["df_name_"],
        operator="substr",
        operand1=self,
        operand2=None
    )
    col.thisptr["begin_"] = begin
    col.thisptr["len_"] = length
    return col

StringColumn.substr = _substr
_VirtualStringColumn.substr = _substr

# -----------------------------------------------------------------------------

def _sum(self, alias="new_column"):
    """
    SUM aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return _Aggregation(alias, self, "sum")

FloatColumn.sum = _sum
_VirtualFloatColumn.sum = _sum

# -----------------------------------------------------------------------------

def _tan(self):
    """Compute tangent."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="tan",
        operand1=self,
        operand2=None
    )

FloatColumn.tan = _tan
_VirtualFloatColumn.tan = _tan

# -----------------------------------------------------------------------------

def _as_num(self):
    """Transforms a categorical column to a numerical column."""
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="as_num",
        operand1=self,
        operand2=None
    )

StringColumn.as_num = _as_num
_VirtualStringColumn.as_num = _as_num

# -----------------------------------------------------------------------------

def _to_numpy(self, sock=None):
    """
    Transform column to numpy array

    Args:
        sock (optional): Socket connecting the Python API with the getML
            engine.
    """

    # -------------------------------------------
    # Build command string

    cmd = dict()

    cmd["name_"] = self.thisptr["df_name_"]
    cmd["type_"] = "FloatColumn.get"

    cmd["col_"] = self.thisptr

    # -------------------------------------------
    # Establish communication with getml engine

    if sock is None:
        s = comm.send_and_receive_socket(cmd)
    else:
        s = sock
        comm.send_string(s, json.dumps(cmd))

    msg = comm.recv_string(s)

    # -------------------------------------------
    # Make sure everything went well, receive data
    # and close connection

    if msg != "Found!":
        s.close()
        comm.engine_exception_handler(msg)

    mat = comm.recv_matrix(s)

    # -------------------------------------------
    # Close connection.

    if sock is None:
        s.close()

    # -------------------------------------------
    # If this is a time stamp, then transform to
    # pd.Timestamp.

    if self.thisptr["type_"] == "FloatColumn":
        if self.thisptr["role_"] == "time_stamp":
            shape = mat.shape
            mat = [pd.Timestamp(ts_input=ts, unit="D") for ts in mat.ravel()]
            mat = np.asarray(mat)
            mat.reshape(shape[0], shape[1])

    # -------------------------------------------

    return mat.ravel()

    # -------------------------------------------

FloatColumn.to_numpy = _to_numpy
_VirtualFloatColumn.to_numpy = _to_numpy

# -----------------------------------------------------------------------------

def _to_numpy_categorical(self, sock=None):
    """
    Transform column to numpy array

    Args:
        sock (optional): Socket connecting the Python API with the getML
            engine.
    """

    # -------------------------------------------
    # Build command string

    cmd = dict()

    cmd["name_"] = self.thisptr["df_name_"]
    cmd["type_"] = "StringColumn.get"

    cmd["col_"] = self.thisptr

    # -------------------------------------------
    # Send command to engine
    
    if sock is None:
        s = comm.send_and_receive_socket(cmd)
    else:
        s = sock
        comm.send_string(s, json.dumps(cmd))

    msg = comm.recv_string(s)

    # -------------------------------------------
    # Make sure everything went well, receive data
    # and close connection

    if msg != "Found!":
        s.close()
        comm.engine_exception_handler(msg)

    mat = comm.recv_categorical_matrix(s)

    # -------------------------------------------
    # Close connection.
    if sock is None:
        s.close()

    # -------------------------------------------

    return mat.ravel()

StringColumn.to_numpy = _to_numpy_categorical 
_VirtualStringColumn.to_numpy = _to_numpy_categorical

# -----------------------------------------------------------------------------

def _as_str(self):
    """Transforms column to a string."""
    return _VirtualStringColumn(
        df_name=self.thisptr["df_name_"],
        operator="as_str",
        operand1=self,
        operand2=None
    )

FloatColumn.as_str = _as_str
_VirtualFloatColumn.as_str = _as_str

_VirtualBooleanColumn.as_str = _as_str

# -----------------------------------------------------------------------------

def _as_ts(self, time_formats=["%Y-%m-%dT%H:%M:%s%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]):
    """
    Transforms a categorical column to a time stamp.

    Args:
        time_formats (str): Formats to be used to parse the time stamps.
    """
    col = _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="as_ts",
        operand1=self,
        operand2=None
    )
    col.thisptr["time_formats_"] = time_formats
    return col

StringColumn.as_ts = _as_ts
_VirtualStringColumn.as_ts = _as_ts

# -----------------------------------------------------------------------------

def _truediv(self, other):
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="divides",
        operand1=self,
        operand2=other
    )

def _rtruediv(self, other):
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="divides",
        operand1=other,
        operand2=self
    )

FloatColumn.__truediv__ = _truediv
FloatColumn.__rtruediv__ = _rtruediv

_VirtualFloatColumn.__truediv__ = _truediv
_VirtualFloatColumn.__rtruediv__ = _rtruediv

# -----------------------------------------------------------------------------

def _update(self, condition, values):
    """
    Returns an updated version of this column.

    All entries for which the corresponding **condition** is True,
    are updated using the corresponding entry in **values**.

    Args:
        condition (Boolean column): Condition according to which the update is done
        values: Values to update with
    """
    col = _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="update",
        operand1=self,
        operand2=values
    )
    if condition.thisptr["type_"] != "VirtualBooleanColumn":
        raise TypeError("Condition for an update must be a Boolen column.")
    col.thisptr["condition_"] = condition.thisptr
    return col

FloatColumn.update = _update

_VirtualFloatColumn.update = _update

# -----------------------------------------------------------------------------

def _update_categorical(self, condition, values):
    """
    Returns an updated version of this column.

    All entries for which the corresponding **condition** is True,
    are updated using the corresponding entry in **values**.

    Args:
        condition (Boolean column): Condition according to which the update is done
        values: Values to update with
    """
    col = _VirtualStringColumn(
        df_name=self.thisptr["df_name_"],
        operator="update",
        operand1=self,
        operand2=values
    )
    if condition.thisptr["type_"] != "VirtualBooleanColumn":
        raise TypeError("Condition for an update must be a Boolean column.")
    col.thisptr["condition_"] = condition.thisptr
    return col

StringColumn.update = _update_categorical

_VirtualStringColumn.update = _update_categorical

# -----------------------------------------------------------------------------

def _var(self, alias="new_column"):
    """
    VAR aggregation.

    Args:
        alias (str): Name for the new column.
    """
    return _Aggregation(alias, self, "var")

FloatColumn.var = _var
_VirtualFloatColumn.var = _var

# -----------------------------------------------------------------------------

def _weekday(self):
    """Extract day of the week from a time stamp, Sunday being 0.

    If the column is numerical, that number will be interpreted as the
    number of days since epoch time (January 1, 1970).

    """
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="weekday",
        operand1=self,
        operand2=None
    )

FloatColumn.weekday = _weekday
_VirtualFloatColumn.weekday = _weekday

# -----------------------------------------------------------------------------

def _year(self):
    """
    Extract year from a time stamp.

    If the column is numerical, that number will be interpreted
    as the number of days since epoch time (January 1, 1970).
    """
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="year",
        operand1=self,
        operand2=None
    )

FloatColumn.year = _year
_VirtualFloatColumn.year = _year

# -----------------------------------------------------------------------------

def _yearday(self):
    """
    Extract day of the year from a time stamp.

    If the column is numerical, that number will be interpreted
    as the number of days since epoch time (January 1, 1970).
    """
    return _VirtualFloatColumn(
        df_name=self.thisptr["df_name_"],
        operator="yearday",
        operand1=self,
        operand2=None
    )

FloatColumn.yearday = _yearday
_VirtualFloatColumn.yearday = _yearday


# -----------------------------------------------------------------------------
