import os
import scipy as sc
import math

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style=("whitegrid"))

import time
from tqdm import tqdm

from pandas_profiling import ProfileReport

def create_report(df, filename=None):
    profile = ProfileReport(df, title='Pandas Profiling Report')

    if filename:
        profile.to_file(output_file = filename)
    else:
        return profile.to_notebook_iframe()
