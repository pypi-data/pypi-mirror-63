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

"""Loss functions used by the feature engineering algorithm.

Right now the getML Python API provides to different loss
functions. We recommend the usage of
:class:`~getml.models.loss_functions.SquareLoss` for regression problems and
:class:`~getml.models.loss_functions.CrossEntropyLoss` for classification
problems.

Please note that these cost functions will only be used by the feature
engineering algorithm and not by the :mod:`~getml.predictors`.
"""

# ------------------------------------------------------------------------------


class _LossFunction(object):
    """
    Base class. Should not ever be directly initialized!
    """

    # ----------------------------------------------------------------

    def __eq__(self, other):
        """Compares the current instance with another one.

        Raises:
            TypeError: If `other` is not a loss function.

        Returns:
            bool: Indicating whether the current instance and `other`
                are the same.

        """
        
        if not isinstance(other, _LossFunction):
            raise TypeError("A loss function can only compared to another loss function!")

	# ------------------------------------------------------------
    
        # Check whether both objects have the same number of instance
        # variables.
        if len(set(self.__dict__.keys())) != len(set(other.__dict__.keys())):
            return False
    
	# ------------------------------------------------------------
        
        for kkey in self.__dict__:
            
            if kkey not in other.__dict__:
                return False
            
            if self.__dict__[kkey] != other.__dict__[kkey]:
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
        
	# ------------------------------------------------------------
	
        for kkey, vvalue in self.__dict__.items():
            result += "\n" + indent1 + kkey + ": " + str(vvalue)
        
	# ------------------------------------------------------------
	
        return result

    # ----------------------------------------------------------------

    def _getml_deserialize(self):
        return self.type 

# --------------------------------------------------------------------


class CrossEntropyLoss(_LossFunction):
    """Cross entropy loss

    The cross entropy between two probability distributions
    :math:`p(x)` and :math:`q(x)` is a combination of the information
    contained in :math:`p(x)` and the additional information stored in
    :math:`q(x)` with respect to :math:`p(x)`. In technical terms: it
    is the entropy of :math:`p(x)` plus the Kullback-Leibler
    divergence - a distance in probability space - from :math:`q(x)`
    to :math:`p(x)`.

    .. math::

        H(p,q) = H(p) + D_{KL}(p||q)

    For discrete probability distributions the cross entropy loss can
    be calculated by

    .. math::

        H(p,q) = - \\sum_{x \\in X} p(x) \\log q(x)

    and for continuous probability distributions by

    .. math::

        H(p,q) = - \\int_{X} p(x) \\log q(x) dx

    with :math:`X` being the support of the samples and :math:`p(x)`
    and :math:`q(x)` being two discrete or continuous probability
    distributions over :math:`X`.

    Note:
        Recommended loss function for classification problems.

    """

    # ----------------------------------------------------------------
	
    def __init__(self):
        self.type = "CrossEntropyLoss"
    
    # ----------------------------------------------------------------
    
    def __str__(self):
        
        result = "CrossEntropyLoss:" + super(CrossEntropyLoss, self).__str__()
        
	# ------------------------------------------------------------
	
        return result

# --------------------------------------------------------------------


class SquareLoss(_LossFunction):
    """Square loss (aka mean squared error (MSE))

    Measures the loss by calculating the average of all squared
    deviations of the predictions :math:`\\hat{y}` from the observed
    (given) outcomes :math:`y`. Depending on the context this measure
    is also known as mean squared error (MSE) or mean squared
    deviation (MSD).  deviation (MSD).

    .. math::

        L(y,\\hat{y}) = \\frac{1}{n} \\sum_{i=1}^{n} (y_i -\\hat{y}_i)^2

    with :math:`n` being the number of samples, :math:`y` the observed
    outcome, and :math:`\\hat{y}` the estimate.

    Note:
        Recommended loss function for regression problems.

    """

    # ----------------------------------------------------------------
	
    def __init__(self):
        self.type = "SquareLoss"

    # ----------------------------------------------------------------
    
    def __str__(self):
        
        result = "SquareLoss:" + super(SquareLoss, self).__str__()
        
	# ------------------------------------------------------------
	
        return result

# --------------------------------------------------------------------

def _decode_loss_function(rawStr):
    """A custom decoder function for :mod:`~getml.models.loss_functions`.

    Note that this funcion is just a convenience function to handle
    the serialization of the derivatives of
    :class:`~getml._LossFunction` like all the other
    classes defined in the getml package.

    Args:
        rawStr (str): string contained in the ``type`` instance variable
            of the loss function and specifying its class name.

    Raises:
        TypeError: If `rawStr` is not of type :py:class:`str`.
        ValueError: If `rawStr` does not represent a valid loss 
            function class.

    Returns:
        Union[:class:`~getml.loss_function.CrossEntropyLoss`, :class:`~getml.loss_function.SquareLoss`]

    Examples:
        Create a :class:`~getml.models.loss_functions.CrossEntropyLoss`,
        serialize it, and deserialize it again.

    .. code-block:: python

            s = getml.models.loss_functions.SquareLoss()
            s_serialized = json.dumps(s, cls = getml.communication._GetmlEncoder)
            s2 = getml.models.loss_functions._decode_loss_function(s_serialized)
            s == s2

    """
    
    # ----------------------------------------------------------------
	
    if type(rawStr) is not str:
        raise TypeError("_decode_loss_function is expecting a str as input")

    # ----------------------------------------------------------------
    
    # Make sure the value is not enclosed in quotation marks
    rawStr = rawStr.lstrip("\"").rstrip("\"")

    # ----------------------------------------------------------------
	
    if rawStr == "SquareLoss":
        return SquareLoss()
        
    elif rawStr == "CrossEntropyLoss":
        return CrossEntropyLoss()
        
    else:
        raise ValueError("Unknown loss functions class: " + rawStr)

# --------------------------------------------------------------------
