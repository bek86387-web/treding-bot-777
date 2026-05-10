import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

from ai_handler import get_ai_response
from market_data import get_price, get_analysis
from chart import generate_chart
from news import get_news

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom! Men sizning trading botingizman.\n\n"
        "📊 Nima qila olaman:\n"
        "/narx [juftlik] — Narxni ko'rish (masalan: /narx BTCUSDT)\n"
        "/tahlil [juftlik] — Kuchli zonalar tahlili\n"
        "/grafik [juftlik] — Grafik va zonalar\n"
        "/yangilik — So'nggi moliyaviy yangiliklar\n\n"
        "Yoki menga xohlagan savolingizni yozing! 🤖"
    )


async def narx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    symbol = args[0].upper() if args else "BTCUSDT"
    await update.message.reply_text("⏳ Narx olinmoqda...")
    result = get_price(symbol)
    await update.message.reply_text(result)


async def tahlil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    symbol = args[0].upper() if args else "BTCUSDT"
    await update.message.reply_text(f"⏳ {symbol} tahlil qilinmoqda...")
    result = get_analysis(symbol)
    await update.message.reply_text(result, parse_mode="Markdown")


async def grafik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    symbol = args[0].upper() if args else "BTCUSDT"
    await update.message.reply_text(f"⏳ {symbol} grafigi tayyorlanmoqda...")
    img_path = generate_chart(symbol)
    if img_path:
        with open(img_path, "rb") as f:
            await update.message.reply_photo(photo=f, caption=f"📊 {symbol} — Kuchli zonalar")
    else:
        await update.message.reply_text("❌ Grafik yaratishda xato yuz berdi.")


async def yangilik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Yangiliklar olinmoqda...")
    result = get_news()
    await update.message.reply_text(result, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("🤔 Javob tayyorlanmoqda...")
    response = get_ai_response(user_message)
    await update.message.reply_text(response)


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("narx", narx))
    app.add_handler(CommandHandler("tahlil", tahlil))
    app.add_handler(CommandHandler("grafik", grafik))
    app.add_handler(CommandHandler("yangilik", yangilik))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot ishga tushdi...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()