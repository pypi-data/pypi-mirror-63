# data-science
A set of useful functions for day-to-day python datascience project.

# Description
A few modules who work together to automatize some routine meet each day on a jr_data_science project.

1. decouverte.py : 

  Some functions to find informations around the files you are given.
  You would find here some functions about paths, cleaning paths, and header extracts.
  
2. extra_pandas.py :

  Never dreamed of a panda function able to convert anykind of time-encoded column ? Well, I didn't do it :-/ but I collected a rather long list of type of string I found on my way, and put it on one bigger-and-bigger convert-date columns ;)
  
3. useful_functions.py:

  How to get all the csvs under a dir ? How to compile a multi-worksheet excel file into one big csv ? Here you have some tool to do so !




import pandas as pd
import os
from collections import Counter
import numpy as np; 

import seaborn as sns; 
import matplotlib.dates as mdates
import random
from functools import reduce

np.random.seed(0)
sns.set()
%matplotlib inline
sns.set_style("white")
sns.set_palette("husl")
