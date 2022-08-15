import numpy as np
import pandas as pd

train = pd.read_csv("train.csv")
# get the parameter values and survivorship
train_survived = train.iloc[:, 0]
train_param = train.iloc[:, 1:]
data = np.asarray(train_param).astype("float64")
print(data)
