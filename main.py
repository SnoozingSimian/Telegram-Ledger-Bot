import logging
import os
import sys

from utils.delete_transaction import remove_last
from utils.parse_transaction import parse_transaction
from utils.store_transaction import store_transaction

from dotenv import load_dotenv

from telegram import Update
from telegram import __version__ as TG_VER
from telegram.ext import (
    filters,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
)

# securely get the API_KEY
load_dotenv()
API_KEY = os.getenv("API_KEY")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# version
APP_VER = "0.0.2"
PY_VER = sys.version

logging.info(f"PYTHON: {PY_VER}\nTELEGRAM: {TG_VER}\nAPPLICATION VER: {APP_VER}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"This is leger_bot version {APP_VER}\nI hope I can be of use",
    )


async def transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    transaction = parse_transaction(update)
    store = store_transaction(transaction)

    if store == 1:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Thanks for telling me!"
        )
    elif store == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I could not understand that, the format is <item> <price>",
        )


# add support for deleting last entry
async def delete_last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    transaction = parse_transaction(update)
    remove = remove_last(transaction)

    if remove == 1:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Removed last entry."
        )

    elif remove == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Could not remove last entry."
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(API_KEY).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    transaction_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), transaction)
    application.add_handler(transaction_handler)

    remove_handler = CommandHandler("remove", delete_last)
    application.add_handler(remove_handler)

    application.run_polling()
