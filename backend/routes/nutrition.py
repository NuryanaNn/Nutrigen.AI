from fastapi import APIRouter
from services.nutrition_service import get_nutrition_data

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])

@router.get("/{food_name}")
def nutrition(food_name: str):
    return get_nutrition_data(food_name)