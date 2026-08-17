import sys
from pathlib import Path

project_root = Path.cwd().parent
sys.path.append(str(project_root))

from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch
import h5py
import numpy as np
import json


class GalaxyDataset(Dataset):
    def __init__(self, h5_path, indices, transform=None):
        self.h5_path = h5_path
        self.indices = indices
        self.transform = transform
        self.h5_file = None  # пока не открываем

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, index):
        if self.h5_file is None:
            self.h5_file = h5py.File(self.h5_path, 'r')

        real_index = self.indices[index]
        label = torch.tensor(self.h5_file['ans'][real_index], dtype=torch.long)
        if self.transform is not None:
            image = self.transform(self.h5_file['images'][real_index])
        else:
            image = self.h5_file['images'][real_index]
        return (image, label)

def create_dataloaders(h5_path, split_indices_path, transform, batch_size=32):
    
    with open(split_indices_path, 'r') as f:
        split_data = json.load(f)

    train_idx = np.array(split_data['train'])
    val_idx = np.array(split_data['val'])
    test_idx = np.array(split_data['test'])

    train_dataset = GalaxyDataset(h5_path, train_idx, transform)
    val_dataset = GalaxyDataset(h5_path, val_idx, transform)
    test_dataset = GalaxyDataset(h5_path, test_idx, transform)

    train_loader = DataLoader(train_dataset, batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size, shuffle=False)

    return (train_loader, val_loader, test_loader)