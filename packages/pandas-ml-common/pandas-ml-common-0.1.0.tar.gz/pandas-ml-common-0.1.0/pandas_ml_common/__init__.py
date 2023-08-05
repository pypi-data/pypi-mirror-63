"""Augment pandas DataFrame with methods for machine learning"""
__version__ = '0.1.0'

import logging
import numpy as np
import pandas as pd

from pandas_ml_common.df.ml import ML


_log = logging.getLogger(__name__)
_log.debug(f"numpy version {np.__version__}")
_log.debug(f"pandas version {pd.__version__}")


setattr(pd.DataFrame, "ml", property(lambda self: ML(self)))