import pandas as pd
import os
from dotenv import load_dotenv
from qdrant_manage_new import create_collections, load_knowledge_to_qdrant

def build_documents():

    load_dotenv()

    obesity_df = pd.read_csv(os.getenv("OBESITY_PATH"))
    foods_df = pd.read_csv(os.getenv("FOODS_PATH"))

    print("OBESITY COLUMNS:", obesity_df.columns.tolist())

    obesity_df["text"] = obesity_df.apply(
        lambda x: f"""
Age: {x['Age']}
Gender: {x['Gender']}
Height: {x['Height']}
Weight: {x['Weight']}

FAF: {x['FAF']}
TUE: {x['TUE']}
CH2O: {x['CH2O']}
SMOKE: {x['SMOKE']}
CALC: {x['CALC']}

FAVC: {x['FAVC']}
FCVC: {x['FCVC']}
NCP: {x['NCP']}
CAEC: {x['CAEC']}

Family History: {x['family_history_with_overweight']}
Obesity Level: {x['NObeyesdad']}
""",
        axis=1
    )

    obesity_docs = [
        {
            "page_content": row["text"],
            "metadata": {
                "source": "obesity",
                "label": row["NObeyesdad"]
            }
        }
        for _, row in obesity_df.iterrows()
    ]

    def create_food_chunks(row):
        food = row["Menu"]

        return [
            ("nutrition_macro", f"""
Food: {food}
CATEGORY: MACRO
Energy: {row['Energy (kJ)']} kJ
Protein: {row['Protein (g)']} g
Fat: {row['Fat (g)']} g
Carbs: {row['Carbohydrates (g)']} g
Fiber: {row['Dietary Fiber (g)']} g
"""),

            ("nutrition_vitamin", f"""
Food: {food}
CATEGORY: VITAMINS
Vitamin C: {row['Vitamin C (mg)']} mg
Vitamin A: {row['Vitamin A (mg)']} mg
Vitamin B1: {row['Vitamin B1 (mg)']} mg
Vitamin B2: {row['Vitamin B2 (mg)']} mg
Vitamin B6: {row['Vitamin B6 (mg)']} mg
Vitamin E: {row['Vitamin E (eq.) (mg)']} mg
Folic Acid: {row['Total Folic Acid (µg)']} µg
"""),

            ("nutrition_mineral", f"""
Food: {food}
CATEGORY: MINERALS
Sodium: {row['Sodium (mg)']} mg
Potassium: {row['Potassium (mg)']} mg
Calcium: {row['Calcium (mg)']} mg
Magnesium: {row['Magnesium (mg)']} mg
Iron: {row['Iron (mg)']} mg
Zinc: {row['Zinc (mg)']} mg
""")
        ]

    food_docs = []

    for _, row in foods_df.iterrows():
        for chunk_type, text in create_food_chunks(row):
            food_docs.append({
                "page_content": text,
                "metadata": {
                    "source": "nutrition",
                    "food": row["Menu"],
                    "chunk_type": chunk_type
                }
            })

    return obesity_docs + food_docs

def initialize_knowledge_base():
    print("Ingesting...")

    # 1. pastikan collection ada
    create_collections()

    # 2. build documents (chunking)
    documents = build_documents()

    # 3. upload ke qdrant
    load_knowledge_to_qdrant(documents)

    print("Knowledge Base ready!")


initialize_knowledge_base()