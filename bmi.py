# bmi.py - Contains BMI calculation logic
# bmi.py - Contains BMI calculation and category logic

from constants import BMI_CATEGORIES


def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """
    Calculate BMI using the formula: BMI = weight (kg) / [height (m)]²
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def classify_bmi(bmi: float) -> str:
    """
    Classify BMI value into a category using BMI_CATEGORIES.
    """
    for lower, upper, category in BMI_CATEGORIES:
        if lower <= bmi <= upper:
            return category
    return "Unknown"
