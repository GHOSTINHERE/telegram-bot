import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

# ---- CONFIG ----
BOT_TOKEN = "YOUR_BOT_TOKEN_FROM_BOTFATHER"
OWNER_CHAT_ID = 123456789  # your own Telegram numeric ID
# ----------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey! Write your anonymous message below and I'll deliver it."
    )


async def relay_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    forward_text = (
        f"📩 New anonymous message\n\n"
        f"From: {user.first_name} (@{user.username})\n"
        f"User ID: {user.id}\n\n"
        f"Message:\n{text}"
    )
    await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=forward_text)

    await update.message.reply_text("Sent anonymously! ✅")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, relay_message))

    app.run_polling()


if __name__ == "__main__":
    main()
