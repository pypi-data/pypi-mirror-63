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

import random
import string

# --------------------------------------------------------------------

def _make_random_name():
    """Temporary name created for a :class:`pandas.DataFrame` during
    :meth:`~getml.models.MultirelModel._convert_population_table` and
    :meth:`~getml.models.MultirelModel._convert_peripheral_tables`.

    Returns:
        str:
            String consisting of "temp-" and 15 random ASCII letters.
    """
    return "temp-" + ''.join(
        random.choice(string.ascii_letters) for i in range(15)
    )

# --------------------------------------------------------------------

def _print_time_taken(begin, end, msg):
    """Prints time required to fit a model.

    Args:
        begin (float): :func:`time.time` output marking the beginning
            of the training.
        end (float): :func:`time.time` output marking the end of the
            training.
        msg (str): Message to display along the duration.

    Raises:
        TypeError: If any of the input is not of proper type.

    """
    
    if type(begin) is not float:
        raise TypeError("'begin' must be a float as returned by time.time().")
    if type(end) is not float:
        raise TypeError("'end' must be a float as returned by time.time().")
    if type(msg) is not str:
        raise TypeError("'msg' must be a str.")
    
    # ----------------------------------------------------------------
	
    seconds = end - begin
    
    hours = int(seconds / 3600)
    seconds -= float(hours * 3600)

    minutes = int(seconds / 60)
    seconds -= float(minutes * 60)

    seconds = round(seconds, 6)

    print(
        msg + str(hours) + "h:" +
        str(minutes) + "m:" + str(seconds)
    )

    print("")

# --------------------------------------------------------------------

