from fastapi import APIRouter
from services.prediction_service import predict_health

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("/")
def predict(data: dict):
    return predict_health(data)