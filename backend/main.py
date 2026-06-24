from fastapi import FastAPI
from routes import nutrition, prediction, chat

app = FastAPI(title="NutriGen.AI API 🚀")

app.include_router(nutrition.router)
app.include_router(prediction.router)
app.include_router(chat.router)

@app.get("/")
def home():
    return {"message": "NutriGen API Ready 🚀"}