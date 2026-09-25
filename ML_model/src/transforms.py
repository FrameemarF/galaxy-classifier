import cv2
import numpy as np
import torch

# для обучения модели
def resize_image(img_array, target_size=(64, 64)):
    return cv2.resize(img_array, target_size, interpolation=cv2.INTER_LANCZOS4)

def preprocess_image(image):
    img_resized = resize_image(image)
    img_float = img_resized.astype(np.float32) / 255.0
    img_tensor = torch.from_numpy(img_float).permute(2, 0, 1)
    return img_tensor

#для обработки изображений от пользователя
def preprocess_image_api(image):
    img_resized = resize_image(image)
    img_float = img_resized.astype(np.float32) / 255.0
    img_tensor = torch.from_numpy(img_float).permute(2, 0, 1)
    return (img_tensor, img_resized)