import cv2
import numpy as np
import torch

def preprocess_image(image):
    img_resized = cv2.resize(image, (64, 64), interpolation=cv2.INTER_LANCZOS4)
    img_float = img_resized.astype(np.float32) / 255.0
    img_tensor = torch.from_numpy(img_float).permute(2, 0, 1)
    return img_tensor