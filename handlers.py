# handlers.py - Handles Telegram command logic
# handlers.py - Telegram command handlers and conversation flow

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from bmi import calculate_bmi, classify_bmi
from database.database import insert_bmi_record, fetch_user_history, delete_user_history, export_user_history
from constants import *

from tabulate import tabulate

GENDER, AGE, HEIGHT, WEIGHT = range(4)

# start and help

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MESSAGE, parse_mode="Markdown")

#calculate

async def start_bmi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["male", "female"]]
    await update.message.reply_text(
        "Please enter your gender:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return GENDER

async def get_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gender = update.message.text.lower()
    if gender not in ["male", "female"]:
        await update.message.reply_text(INVALID_INPUT_MESSAGE)
        return GENDER
    context.user_data["gender"] = gender
    await update.message.reply_text("Enter your age:", reply_markup=ReplyKeyboardRemove())
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        age = int(update.message.text)
        context.user_data["age"] = age
        await update.message.reply_text("Enter your height in centimeters:")
        return HEIGHT
    except ValueError:
        await update.message.reply_text(INVALID_INPUT_MESSAGE)
        return AGE

async def get_height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        height = float(update.message.text)
        context.user_data["height"] = height
        await update.message.reply_text("Enter your weight in kilograms:")
        return WEIGHT
    except ValueError:
        await update.message.reply_text(INVALID_INPUT_MESSAGE)
        return HEIGHT

async def get_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        weight = float(update.message.text)
        context.user_data["weight"] = weight

        height = context.user_data["height"]
        age = context.user_data["age"]
        gender = context.user_data["gender"]
        user_id = update.effective_user.id

        bmi = calculate_bmi(height, weight)
        category = classify_bmi(bmi)

        insert_bmi_record(user_id, gender, age, height, weight, bmi, category)

        await update.message.reply_text(
            f"✅ Your BMI is *{bmi}* ({category})",
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text(INVALID_INPUT_MESSAGE)
        return WEIGHT
    
    # History and cler

# show history
async def show_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    records = fetch_user_history(user_id)

    if not records:
        await update.message.reply_text(NO_HISTORY_MESSAGE)
    else:
        table = tabulate(records, headers=HISTORY_HEADER, tablefmt="github")
        await update.message.reply_text(f"🗂️ Your BMI History:\n```\n{table}\n```", parse_mode="Markdown")


async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    delete_user_history(user_id)
    await update.message.reply_text("🧹 Your BMI history has been cleared.")

# export

async def export_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    filename = export_user_history(user_id)

    with open(filename, "rb") as file:
        await update.message.reply_document(file, filename=filename)
__all__ = [
    "start", "help_command", "start_bmi", "get_gender", "get_age",
    "get_height", "get_weight", "show_history", "clear_history", "export_history",
    "GENDER", "AGE", "HEIGHT", "WEIGHT"
]
