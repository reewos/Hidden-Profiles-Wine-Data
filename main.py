### Import libraries
import os
import numpy as np
import pandas as pd
from utils import *

from sklearn.preprocessing import (StandardScaler,
                                   MinMaxScaler)
from sklearn.decomposition import PCA
from sklearn.cluster import (AgglomerativeClustering,
                             AffinityPropagation,
                             SpectralClustering,
                             DBSCAN,
                             KMeans)

# Load dataset
df = pd.DataFrame(get_data())
print("First 5 rows of Wine Data")
print(df.head())

# Null Verification
print("Number of null")
print(df.isnull().sum())

# Statistical summary
print("Statistical summary of columns")
print(df.describe())

