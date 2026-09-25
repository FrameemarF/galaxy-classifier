import cv2
import numpy as np
import os
import uuid
import app.database.crud as crud
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Request
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from ML_model.src.transforms import preprocess_image_api
from ML_model.src.model import SimpleGalaxyCNN
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.database.database import get_session
from app.services.ml_service import predict

load_dotenv()
router = APIRouter(prefix="/predictions")

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE = 5 * 1024 * 1024
IMAGES_PATH = Path(os.getenv("IMAGES_DIR"))

def is_image(data: bytes) -> bool:
    try:
        img = Image.open(BytesIO(data))
        img.verify()
        return True
    except (UnidentifiedImageError, OSError):
        return False


@router.post("/upload")
async def upload_image(request: Request, file: UploadFile = File(...), session: Session = Depends(get_session)):
    # 1. Быстрый фильтр по content_type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "unsupported type")

    # 2. Прочитать байты
    data = await file.read()

    # 3. Проверить размер
    if len(data) > MAX_SIZE:
        raise HTTPException(413, "too large")

    # 4. Проверить, что это картинка
    if not is_image(data):
        raise HTTPException(400, "not an image")

    # 5. Декодировать в cv2 → RGB
    arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(400, "cannot decode")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 6. Обработка (сжатие) изображения для модели
    tensor, img_resized = preprocess_image_api(img)

    name = f"{uuid.uuid4().hex}.jpg"
    path = IMAGES_PATH / name
    bgr = cv2.cvtColor(img_resized, cv2.COLOR_RGB2BGR)
    ok, buf = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
    if not ok:
        raise HTTPException(500, "failed to encode thumbnail")

    path.write_bytes(buf.tobytes())

    # 7. ...прогон через модель, вернуть ответ
    model: SimpleGalaxyCNN = request.app.state.model
    confidence, class_index = predict(model=model, image_tensor=tensor)
    galaxy_entry = crud.take_galaxy_entry(session=session, model_index=class_index)

    crud.create_prediction_entry(session=session, galaxy_id=galaxy_entry.id, confidence=confidence, image_path=name)    

    return {"galaxy_type_name": galaxy_entry.name, "galaxy_type_description": galaxy_entry.description, "confidence": confidence, "thumb": name}