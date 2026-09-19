import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import ML_model.config as config
import numpy as np
import h5py
from ML_model.src.transforms import resize_image

with h5py.File(config.RAW_H5_PATH, 'r') as src:
    images = src['images'][:]
    ans = src['ans'][:]
    
    n = images.shape[0]
    resized_images = np.zeros((n, 64, 64, 3), dtype='uint8')
    
    for i in range(n):
        resized_images[i] = resize_image(images[i])
    
    save_path = config.PROCESSED_H5_PATH
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    with h5py.File(save_path, 'w') as dst:
        dst.create_dataset('images', data=resized_images)
        dst.create_dataset('ans', data=ans)