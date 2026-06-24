import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import os

# contoh dataset sederhana
data = {
    "age": [25, 45, 35, 50, 23, 40],
    "bmi": [22, 30, 25, 28, 21, 27],
    "risk": [0, 1, 0, 1, 0, 1]  # 0 = sehat, 1 = berisiko
}

df = pd.DataFrame(data)

X = df[["age", "bmi"]]
y = df["risk"]

# train model
model = LogisticRegression()
model.fit(X, y)

# simpan ke folder model
os.makedirs("model", exist_ok=True)

with open("model/health_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model berhasil dibuat!")