import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../nutrition.db")

conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

def get_nutrition_data(food_name):
    keyword = food_name.lower()

    cursor.execute("""
        SELECT * FROM foods 
        WHERE LOWER(name) LIKE ?
    """, ('%' + keyword + '%',))

    rows = cursor.fetchall()

    if not rows:
        return {"error": "Makanan tidak ditemukan"}

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "calories": r[1],
            "proteins": r[2],
            "fat": r[3],
            "carbohydrate": r[4],
            "name": r[5],
            "image": r[6]
        })

    return result