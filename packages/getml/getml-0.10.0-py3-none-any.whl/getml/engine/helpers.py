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
import os
import platform
import socket
import time
import getml

import getml.communication as comm

# --------------------------------------------------------------------


def delete_project(name):
    """Deletes a project.

    Args:
        name (str): Name of your project.

    Raises:
        TypeError: If any of the input arguments is of wrong type.

    Note:

        All data and models contained in the project directory will be
        permanently lost.

    """
    
    if type(name) is not str:
        raise TypeError("'name' must be of type str")
    
    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "delete_project"
    cmd["name_"] = name

    comm.send(cmd)

# -----------------------------------------------------------------------------

def is_alive():
    """Checks if the getML engine is running.

    Raises:
        ConnectionRefusedError: If unable to connect to engine

    Returns:
        bool:

            True if the getML engine is running and ready to accept
            commands and False otherwise.

    Note:

        The function will return False if no user has logged into the
        running engine too.

        There is a latency of 1-2 seconds in which the function still
        returns True while the getML monitor has already established
        the connection.

    """

    ## ---------------------------------------------------------------
    
    cmd = dict()
    cmd["type_"] = "is_alive"
    cmd["name_"] = ""

    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )
    try:
        s.connect(('localhost', getml.port))
    except ConnectionRefusedError:
        return False

    comm.send_string(s, json.dumps(cmd))

    s.close()

    return True

# -----------------------------------------------------------------------------

def list_projects():
    """
    List all projects on the getML engine.

    Raises:
        IOError:

            If an error in the communication with the getML engine
            occurred.

    Returns:
        List[str]: Lists the name all of the projects. 
    """

    cmd = dict()
    cmd["type_"] = "list_projects"
    cmd["name_"] = ""
    
    s = comm.send_and_receive_socket(cmd)

    msg = comm.recv_string(s)

    if msg != "Success!":
        comm.engine_exception_handler(msg)
    
    json_str = comm.recv_string(s) 
    
    s.close() 

    return json.loads(json_str)["projects"]

# -----------------------------------------------------------------------------

def set_project(name):
    """Creates a new or loads an existing project.

    If there is no project holding `name` present on the engine, a new one will
    be created. See the :ref:`User guide <the_getml_engine_projects>` for more
    information.

    Args:
        name (str): Name of the new project.

    Raises:
        ConnectionRefusedError: If unable to connect to engine
        TypeError: If any of the input arguments is of wrong type.

    Note:

        All data frame objects and models in the getML engine are
        bundled in projects. When loading an existing project, the
        current memory of the engine will be flushed and all changes
        applied to :class:`~getml.data.DataFrame` instances after
        calling their :meth:`~getml.data.DataFrame.save` method will
        be lost. Afterwards, all :class:`~getml.models.RelboostModel`
        and :class:`~getml.models.MultirelModel` will be loaded into
        memory automatically. The data frame objects, on the other
        hand, won't be loaded since they consume significantly more
        memory than the models and can be access manually using
        :func:`~getml.data.load_data_frame` or
        :meth:`~getml.data.DataFrame.load`.


        See also: :func:`~getml.engine.delete_project` and
        :func:`list_projects`.

    """
    
    if type(name) is not str:
        raise TypeError("'name' must be of type str")
    if not is_alive():
        raise ConnectionRefusedError("""
        Cannot connect to getML engine. 
        Make sure the engine is running on port '"""+str(getml.port)+"""' and you are logged in.
        See `help(getml.engine)`.""")
    
    # ----------------------------------------------------------------
    
    # Get a list of available projects first to know whether the
    # command will create a new or loads an existing one.
    available_projects = list_projects()

    cmd = dict()
    cmd["type_"] = "set_project"
    cmd["name_"] = name

    comm.send(cmd)
    
    # ----------------------------------------------------------------
    
    if name in available_projects:
        print("Loading existing project '"+name+"'")
    else:
        print("Creating new project '"+name+"'")

# -----------------------------------------------------------------------------


def shutdown():
    """Shuts down the getML engine.

    Raises:
        ConnectionRefusedError: If unable to connect to engine

    Note:

        All changes applied to the :class:`~getml.data.DataFrame`
        after calling their :meth:`~getml.data.DataFrame.save`
        method will be lost.

    """

    cmd = dict()
    cmd["type_"] = "shutdown"
    cmd["name_"] = "all"

    ## In case of the shutdown there will be no returned message to
    ## check the success.
    s = comm.send_and_receive_socket(cmd)

    s.close()
    
# -----------------------------------------------------------------------------
