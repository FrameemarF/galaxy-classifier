import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import Optimizer

def train_one_epoch(model: nn.Module, loader: DataLoader, optimizer: Optimizer, criterion: nn.Module) -> tuple[float, float]:
    model.train()
    total_loss = 0.0
    correct_predictions = 0
    total_labels = 0

    for images, labels in loader:
        optimizer.zero_grad()
        output = model(images)
        loss = criterion(output, labels)
        total_loss += loss.item()
        loss.backward()
        optimizer.step()

        predictions = torch.argmax(output, dim=1)
        correct_predictions += (predictions == labels).sum().item()
        total_labels += labels.size(0)

    avg_loss = total_loss / len(loader)
    accuracy = correct_predictions / total_labels
    return avg_loss, accuracy

def evaluate(model: nn.Module, loader: DataLoader, criterion: nn.Module) -> tuple[float, float]:
    model.eval()
    total_loss = 0.0
    correct_predictions = 0
    total_labels = 0

    with torch.no_grad():
        for images, labels in loader:
            output = model(images)
            loss = criterion(output, labels)
            total_loss += loss.item()

            predictions = torch.argmax(output, dim=1)
            correct_predictions += (predictions == labels).sum().item()
            total_labels += labels.size(0)


    avg_loss = total_loss / len(loader)
    accuracy = correct_predictions / total_labels
    return avg_loss, accuracy