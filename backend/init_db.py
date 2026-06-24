import pandas as pd
import sqlite3

# load CSV
df = pd.read_csv("backend/data/nutrition.csv")

# koneksi DB
conn = sqlite3.connect("backend/nutrition.db")

# simpan ke tabel
df.to_sql("foods", conn, if_exists="replace", index=False)

print("✅ Data berhasil masuk database")