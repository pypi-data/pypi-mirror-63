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

"""A :class:`~getml.data.role` determines if and how
:mod:`~getml.data.columns` are handled during the construction of the
data model (see :ref:`data_model`) and used by the feature engineering
(FE) algorithm (see :ref:`feature_engineering`).

Upon construction (via :func:`~getml.data.DataFrame.from_csv`,
:func:`~getml.data.DataFrame.from_pandas`,
:func:`~getml.data.DataFrame.from_db`, and
:func:`~getml.data.DataFrame.from_json`) a
:class:`~getml.data.DataFrame` will only consist of
:mod:`~getml.data.columns` holding either the role
:const:`~getml.data.role.unused_float` or
:const:`~getml.data.role.unused_string` depending on the underlying
data type. This tells the getML software to neither use these columns
during the creation of the data model, the feature engineering, or the
training of the machine learning (ML) algorithms.

To make use of the uploaded data, you have to tell the getML suite how
you intend to use it by assigning another
:class:`~getml.data.role`. This can be done by either using the
:meth:`~getml.data.DataFrame.set_role` method of the
:class:`~getml.data.DataFrame` containing the particular column or by
providing a dictionary in the constructor function.

Each column must have at have a single role. But what if you e.g. want
to use a column to both create relations in your data model and to be
the basis of new features? You have to add it twice and assign
each of them a different role.
"""


categorical = "categorical"
"""Marks categorical ingredients for future features

This role tells the getML engine to include the associated
:class:`~getml.data.columns.StringColumn` during the feature
engineering.

It should be used for all data with no inherent ordering, even if the
categories are encoded as integer instead of strings in your provided
data set.
"""
    
join_key = "join_key"
"""Marks relations in the data model

Role required to establish a relation between two
:class:`~getml.data.Placeholder`, the abstract representation of the
:class:`~getml.data.DataFrame`, by using the
:meth:`~getml.data.Placeholder.join` method (see
:ref:`data_model`). See chapter :ref:`data_model` for details.
	 
The content of this column is allowed to contain NULL values. But
beware, columns with NULL in their join keys won't be matched to
anything, not even to NULL in other join keys.

:mod:`~getml.data.columns` of this role will *not* be handled by
the feature engineering algorithm.

"""

numerical = "numerical"
"""Marks numerical ingredients for future features

This role tells the getML engine to include the associated
:class:`~getml.data.columns.FloatColumn` during the feature
engineering.

It should be used for all data with an inherent ordering, regardless
if it's a sampled from a continuous quantity, like passed time or the
total amount of rainfall, or a discrete one, like the number of sugary
mulberries one has eaten since lunch.
"""

target = "target"
"""
Numerical response predicted using the resulting features

The associated :mod:`~getml.data.columns` do contain the variables we
intend to describe and predict in our data science project. They are
neither included in the data model nor in the feature engineering
algorithm (since they will be unknown in all future events). But they
are such an important part of the analysis that their presence - at
least one - is required in every population table (see
:ref:`data_model_tables`). They are allowed to be
present in peripheral tables too, but won't be considered during the
fitting.

The actual content of the columns needs to be numerical. For regression
problems this is straight forward by providing the numerical target
variable. In classification, however, all possible values must be
encoded as numbers. But don't worry, the getML engine does not assume
an internal ordering for this kind of data. In addition, no `NULL`
values are allowed within the associated columns.

:class:`~getml.models.MultirelModel` does support multiple targets out
of the box. For :class:`~getml.models.RelboostModel`, on the other
hand, you can only train on one at a time. If you have several
targets, you need to train separate models (either by providing unique
names or using the time-based default names) and specify the
corresponding ``target_num`` instance variable of
:class:`~getml.models.RelboostModel`. Which number is associated to
which target is determined by their ordering in the ``target_names``
instance variable in the :class:`~getml.data.DataFrame`.
"""

time_stamp = "time_stamp"
"""
Ensures causality in the data model and marks time column as numerical ingredient

Role required to establish a relation between two
:class:`~getml.data.Placeholder`, the abstract representation
of the :class:`~getml.data.DataFrame`, by using the
:meth:`~getml.data.Placeholder.join` method (see
:ref:`data_model`). See chapter :ref:`data_model` for details.
	 
This role ensures causality by incorporating only those rows of a
second :class:`~getml.data.Placeholder` in the
:meth:`~getml.data.Placeholder.join` operation for which the time
stamp is at most as recent as the one of the associated column. Since
usually it’s the peripheral table that is joined on the population
table (see :ref:`data_model_tables`), this ensures no
information from the future is considered during
training.
	 
:mod:`~getml.data.columns` of this role will be handled by the feature
engineering algorithm the same way as
:ref:`annotating_roles_numerical` are.

Please note that getML does **not** handle **UNIX time stamps** but,
instead, encodes time as multiples and fractions of days since the
01.01.1970 (`1970-01-01T00:00:00`). For example
:math:`7.334722222222222 = 7 + 6/24 + 2/(24*60)` would be interpreted
`1970-01-08T06:02:00`.
"""

unused_float = "unused_float"
"""Marks a :class:`~getml.data.column.FloatColumn` as unused

The associated :mod:`~getml.data.column` will be neither used in the
data model nor during the features engineering or prediction.
"""

unused_string = "unused_string"
"""Marks a :class:`~getml.data.column.StringColumn` as unused

The associated :mod:`~getml.data.column` will be neither used in the
data model nor during the features engineering or prediction.
"""
