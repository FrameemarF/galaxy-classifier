from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent  # папка, где лежит сам config.py
DATA_DIR = PROJECT_ROOT / "data"
RAW_H5_PATH = DATA_DIR / "raw" / "Galaxy10_DECals.h5"
PROCESSED_DIR = DATA_DIR / "processed"
SPLIT_INDICES_PATH = PROCESSED_DIR / "indices_split.json"
MODELS_DIR = PROJECT_ROOT / "models"
PROCESSED_H5_PATH = PROCESSED_DIR / "galaxy10_64x64.h5"