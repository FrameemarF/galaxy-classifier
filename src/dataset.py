from torch.utils.data import Dataset
import torch
import h5py

class GalaxyDataset(Dataset):
    def __init__(self, h5_path, indices, transform=None):
        self.h5_path = h5_path
        self.indices = indices
        self.transform = transform

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, index):
        real_index = self.indices[index]
        with h5py.File(self.h5_path, 'r') as F:
            label = torch.tensor(F['ans'][real_index], dtype=torch.long)
            if self.transform is not None:
                image = self.transform(F['images'][real_index])
            else:
                image = F['images'][real_index]
            return (image, label)