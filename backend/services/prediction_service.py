import os
import pickle

# ambil path aman
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "model", "health_model.pkl")

# load model
with open(model_path, "rb") as f:
    model = pickle.load(f)


def predict_health(data):
    try:
        umur = data["umur"]
        bmi = data["bmi"]

        # model prediksi
        result = model.predict([[umur, bmi]])

        return {
            "umur": umur,
            "bmi": bmi,
            "risiko": int(result[0])  # 0 / 1
        }

    except Exception as e:
        return {"error": str(e)}