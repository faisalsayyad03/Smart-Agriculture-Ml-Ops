"""Runtime compatibility helpers for the supported Python environment."""

import _thread
import sys

import six


# Python 3.13 can expose six.moves as the legacy ``moves`` module name.
# python-dateutil imports the thread move through that alias.
six.moves._thread = _thread
sys.modules.setdefault("moves", six.moves)
sys.modules.setdefault("moves._thread", _thread)


def patch_serialized_models():
	"""Bridge the renamed imputer attribute after scientific imports settle."""
	from sklearn.impute import SimpleImputer

	if not hasattr(SimpleImputer, "_fill_dtype"):
		SimpleImputer._fill_dtype = property(lambda estimator: estimator._fit_dtype)
