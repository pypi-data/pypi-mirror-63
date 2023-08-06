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
import os

import numpy as np

import getml.communication as comm

# --------------------------------------------------------------------

def _is_numerical_type(coltype):
    return coltype in [
        int, 
        float, 
        np.int_, 
        np.int8, 
        np.int16, 
        np.int32, 
        np.int64, 
        np.uint8, 
        np.uint16, 
        np.uint32, 
        np.uint64,
        np.float_, 
        np.float16, 
        np.float32, 
        np.float64]

# --------------------------------------------------------------------

def _is_typed_list(some_list, types):
    
    if type(types) is not list:
        types = [types]
    
    is_typed_list = type(some_list) is list 
    
    is_typed_list = is_typed_list and all(
            [type(ll) in types for ll in some_list])
    
    return is_typed_list 
    
# --------------------------------------------------------------------

def _is_non_empty_typed_list(some_list, types):
    return _is_typed_list(some_list, types) and len(some_list) > 0 

# --------------------------------------------------------------------

def _update_sniffed_roles(sniffed_roles, roles):
   
    # -------------------------------------------------------

    if not isinstance(roles, dict):
        raise TypeError("roles must be a dict!")

    if not isinstance(sniffed_roles, dict):
        raise TypeError("sniffed_roles must be a dict!")
    
    for role in list(roles.keys()):
        if not _is_typed_list(roles[role], str):
            raise TypeError("Entries in roles must be lists of str!")
    
    for role in list(sniffed_roles.keys()):
        if not _is_typed_list(sniffed_roles[role], str):
            raise TypeError("Entries in sniffed_roles must be lists of str!")
    
    # -------------------------------------------------------
    
    for new_role in list(roles.keys()):
        
        for colname in roles[new_role]:
            
            for old_role in list(sniffed_roles.keys()):
                if colname in sniffed_roles[old_role]:
                    sniffed_roles[old_role].remove(colname)
                    break

            if new_role in sniffed_roles:
                sniffed_roles[new_role] += [colname]
            else:
                sniffed_roles[new_role] = [colname]
    
    # -------------------------------------------------------
    
    return sniffed_roles

# --------------------------------------------------------------------

def _sniff_csv(
    fnames,
    num_lines_sniffed=1000,
    quotechar='"',
    sep=',',
    skip=0):
    """Sniffs a list of CSV files and returns the result as a dictionary of
    roles.

    Args:
        fnames (List[str]): The list of CSV file names to be read.

        num_lines_sniffed (int, optional):

            Number of lines analysed by the sniffer.

        quotechar (str, optional):

            The character used to wrap strings.

        sep (str, optional):

            The character used for separating fields.

        skip (int, optional):
            Number of lines to skip at the beginning of each file.

    Raises:
        IOError:

            If an error in the communication with the getML engine
            occurred.


    Returns:
        dict: Keyword arguments (kwargs) that can be used to construct
              a DataFrame.
    """
    # ----------------------------------------------------------------
    # Transform paths
    fnames_ = [os.path.abspath(_) for _ in fnames]

    # ----------------------------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Database.sniff_csv"

    cmd["dialect_"] = "python"
    cmd["fnames_"] = fnames_
    cmd["header_"] = True
    cmd["num_lines_sniffed_"] = num_lines_sniffed
    cmd["quotechar_"] = quotechar
    cmd["sep_"] = sep
    cmd["skip_"] = skip

    # ----------------------------------------------------------------
    # Send JSON command to engine.

    s = comm.send_and_receive_socket(cmd)

    # ----------------------------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(s)

    if msg != "Success!":
        s.close()
        raise IOError(msg)

    # ----------------------------------------------------------------

    roles = comm.recv_string(s)

    s.close()

    return json.loads(roles)

# --------------------------------------------------------------------

def _sniff_db(table_name):
    """
    Sniffs a table in the database and returns a dictionary of roles.

    Args:
        table_name (str): Name of the table to be sniffed. 

    Returns:
        dict: Keyword arguments (kwargs) that can be used to construct
              a DataFrame.
    """

    # ----------------------------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = table_name
    cmd["type_"] = "Database.sniff_table"

    # ----------------------------------------------------------------
    # Send JSON command to engine.

    s = comm.send_and_receive_socket(cmd)

    # ----------------------------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(s)

    if msg != "Success!":
        s.close()
        raise Exception(msg)

    # ----------------------------------------------------------------

    roles = comm.recv_string(s)

    s.close()

    return json.loads(roles)

# --------------------------------------------------------------------

def _sniff_json(json_str):
    """Sniffs a JSON str and returns the result as a dictionary of
    roles.

    Args:
        json_str (str): The JSON string to be sniffed.

    Returns:
        dict: Roles that can be used to construct a DataFrame.
    """
    json_dict = json.loads(json_str)
    
    roles = dict()
    roles["unused_float"] = []
    roles["unused_string"] = []

    for cname, col in json_dict.items():
        if _is_numerical_type(np.array(col).dtype):
            roles["unused_float"].append(cname)
        else:
            roles["unused_string"].append(cname)

    return roles

# --------------------------------------------------------------------

def _sniff_pandas(pandas_df):
    """Sniffs a pandas.DataFrame and returns the result as a dictionary of
    roles.

    Args:
        pandas_df (pandas.DataFrame): The pandas.DataFrame to be sniffed.

    Returns:
        dict: Roles that can be used to construct a DataFrame.
    """
    roles = dict()
    roles["unused_float"] = []
    roles["unused_string"] = []

    colnames = pandas_df.columns
    coltypes = pandas_df.dtypes

    for cname, ctype in zip(colnames, coltypes):
        if _is_numerical_type(ctype):
            roles["unused_float"].append(cname)
        else:
            roles["unused_string"].append(cname)

    return roles

# --------------------------------------------------------------------
