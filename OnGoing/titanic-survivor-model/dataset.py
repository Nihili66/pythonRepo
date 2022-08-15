import numpy as np
from torch.utils.data import Dataset

class CustomTrainSet(Dataset):
    def __init__(self, param, survived=None, transforms=None):
        self.X = param
        self.y = survived
        self.transforms = transforms

    def __len__(self):
        return (len(self.X))

    def __getitem__(self, i):
        data = np.asarray(self.X[i, :]).astype(float)

        if self.transforms:
            data = self.transforms(data)

        if self.y is not None:
            return (data, self.y[i])
        else:
            return data
