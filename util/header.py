# generic header used by all scripts
import sys
import os
import os.path as op
sys.path.append(op.abspath("."))

import util.slope_model as slm
import util.slopes as sl
from util.fn import logit, ilogit, otop, cilower, ciupper
import util.sample_stats as ss
from util import regress
import util.regress_setup as setup

import pandas as pd
import numpy as np
import datetime
