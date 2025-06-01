# bot.py - Entry point for the BMI Telegram Bot
# bot.py - Main entry point for the BMI Calculator Bot

import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler

from handlers import (
    start, help_command, start_bmi, get_gender, get_age, get_height,
    get_weight, show_history, clear_history, export_history,
    GENDER, AGE, HEIGHT, WEIGHT
)

from database.database import init_db

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def error_handler(update, context):
    logger.warning(f'Update "{update}" caused error "{context.error}"')


def main():
    # Load your bot token here (replace with your token)
    BOT_TOKEN = "7728030002:AAFpCHiQZvDCqQfP8Z2IkaPZ1tVSpa5dxe8"

    # Initialize database
    init_db()

    # Create application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("history", show_history))
    app.add_handler(CommandHandler("clear", clear_history))
    app.add_handler(CommandHandler("export", export_history))

    # Conversation handler for /calculate
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("calculate", start_bmi)],
        states={
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_gender)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_height)],
            WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_weight)],
        },
        fallbacks=[],
    )
    app.add_handler(conv_handler)

    # Log all errors
    app.add_error_handler(error_handler)

    # Start the bot
    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
