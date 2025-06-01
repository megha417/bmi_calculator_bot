# constants.py - Static texts, thresholds, and categories
# constants.py - Static texts, thresholds, and messages for the BMI Bot

# Start and help messages
WELCOME_MESSAGE = (
    "👋 Welcome to the *BMI Calculator Bot*! \n\n"
    "Use /calculate to check your BMI. "
    "I'll guide you step-by-step and store your history.\n\n"
    "Available commands:\n"
    "/start - Welcome message\n"
    "/calculate - Begin BMI calculation\n"
    "/history - View your BMI records\n"
    "/clear - Clear your BMI history\n"
    "/export - Export your BMI data (CSV)\n"
    "/help - Show this help message"
)

HELP_MESSAGE = (
    "ℹ️ This bot helps calculate your *Body Mass Index (BMI)*.\n"
    "You'll be asked for:\n"
    "• Gender (male/female)\n"
    "• Age\n"
    "• Height (cm)\n"
    "• Weight (kg)\n"
    "And I’ll calculate your BMI and save your results!\n\n"
    "Use /calculate to begin."
)

INVALID_INPUT_MESSAGE = (
    "⚠️ Invalid input. Please enter a valid numeric value."
)

NO_HISTORY_MESSAGE = (
    "📭 No BMI history found. Use /calculate to start logging."
)

HISTORY_HEADER = ["Date", "Gender", "Age", "Height(cm)", "Weight(kg)", "BMI", "Category"]

# BMI thresholds based on WHO guidelines
BMI_CATEGORIES = [
    (0, 18.4, "Underweight"),
    (18.5, 24.9, "Normal weight"),
    (25.0, 29.9, "Overweight"),
    (30.0, 34.9, "Obese Class I"),
    (35.0, 39.9, "Obese Class II"),
    (40.0, float("inf"), "Obese Class III")
]
