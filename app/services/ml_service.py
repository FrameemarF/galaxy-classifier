from ML_model.src.model import SimpleGalaxyCNN
from ML_model import config as ml_config
import torch

def load_model():
    model = SimpleGalaxyCNN()
    model.load_state_dict(torch.load(ml_config.MODELS_DIR/"best_model.pt"))
    model.eval()
    return model

def predict(model, image_tensor: torch.Tensor):
    image_tensor = image_tensor.unsqueeze(0)
    with torch.no_grad():
        logits = model(image_tensor)
        probabilities = torch.softmax(logits, dim=1)
        response = torch.max(probabilities, dim=1)
    return (response.values.item(), response.indices.item())