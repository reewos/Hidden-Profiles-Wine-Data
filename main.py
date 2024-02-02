### Import libraries
import warnings

# Ignore all deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import pandas as pd
from utils import *
from class_model import ModelClusterVoting

# Load dataset
df = pd.DataFrame(get_data())
print("* First 5 rows of Wine Data")
print(df.head())

# Null Verification
print("\n\n* Number of null")
print(df.isnull().sum())

# Statistical summary
print("\n\n* Statistical summary of columns")
print(df.describe())

# Correlation Matrix
print("\n\n* Correlation Matrix")
print(df.corr())

print("----------------------")


# Init model
model = ModelClusterVoting()

#Train and predict
df['Clusters_Voting'] = model.fit_predict(df)

print("\n\n* First 5 rows of Wine Data after prediction")
print(df.head())
print("\n\n")


# os.chmod('./models', 0o766)
# os.chmod('./datasets', 0o766)
#Save model

path_model = './models/voting_model.pkl'
model.save_model(path_model)
print(f"Saved model in {path_model}")

#Save results
path_results = './datasets/results.csv'
df.to_csv(path_results, index=False)
print(f"Saved results in {path_results}")
