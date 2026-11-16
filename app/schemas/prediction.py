from pydantic import BaseModel, ConfigDict
from datetime import datetime

class GalaxyClass(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    description: str

class Prediction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    confidence: float
    created_at: datetime
    image_path: str | None
    galaxy_class: GalaxyClass