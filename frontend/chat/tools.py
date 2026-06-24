from langchain_core.tools import tool

@tool
def calculate_bmi(height: float, weight: float) -> dict:
    """
    Calculate BMI from height (meters) and weight (kg).
    """

    bmi = weight / (height ** 2)

    if bmi < 18.5:
        category = "Insufficient_Weight"
    elif bmi < 25:
        category = "Normal_Weight"
    elif bmi < 27.5:
        category = "Overweight_Level_I"
    elif bmi < 30:
        category = "Overweight_Level_II"
    elif bmi < 35:
        category = "Obesity_Type_I"
    elif bmi < 40:
        category = "Obesity_Type_II"
    else:
        category = "Obesity_Type_III"

    return {
        "bmi": round(bmi, 2),
        "category": category
    }

@tool
def target_weight(height: float, weight: float) -> dict:
    """
    Calculate ideal weight range and target weight.

    Parameters:
    - height: height in meters
    - weight: current weight in kg
    """

    min_ideal_weight = 18.5 * (height ** 2)
    max_ideal_weight = 24.9 * (height ** 2)

    target_bmi = 22
    target_weight = target_bmi * (height ** 2)

    difference = target_weight - weight

    if difference > 0:
        recommendation = (
            f"Need to gain approximately {abs(difference):.2f} kg"
        )
    elif difference < 0:
        recommendation = (
            f"Need to lose approximately {abs(difference):.2f} kg"
        )
    else:
        recommendation = (
            "Current weight is already at the target weight"
        )

    return {
        "current_weight": round(weight, 2),
        "ideal_weight_range": {
            "min": round(min_ideal_weight, 2),
            "max": round(max_ideal_weight, 2)
        },
        "target_weight": round(target_weight, 2),
        "weight_difference": round(difference, 2),
        "recommendation": recommendation
    }
