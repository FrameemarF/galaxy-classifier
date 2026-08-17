import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import Optimizer

def train_one_epoch(model: nn.Module, loader: DataLoader, optimizer: Optimizer, criterion: nn.Module) -> float:
    model.train()
    total_loss = 0.0

    for images, labels in loader:
        optimizer.zero_grad()
        output = model(images)
        loss = criterion(output, labels)
        total_loss += loss.item()
        loss.backward()
        optimizer.step()

    avg_loss = total_loss / len(loader)
    return avg_loss

def evaluate(model: nn.Module, loader: DataLoader, criterion: nn.Module) -> float:
    model.eval()
    total_loss = 0.0

    with torch.no_grad():
        for images, labels in loader:
            output = model(images)
            loss = criterion(output, labels)
            total_loss += loss.item()

    avg_loss = total_loss / len(loader)
    return avg_loss