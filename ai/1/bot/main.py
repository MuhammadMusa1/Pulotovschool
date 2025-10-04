import os
import logging
from datetime import datetime, timezone
from typing import Dict, List, Tuple

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Логирование ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("rates-bot")

# --- Загружаем переменные ---
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_CURRENCY = os.getenv("BASE_CURRENCY", "TJS").upper()
TARGETS = set(os.getenv("TARGETS", "USD,EUR,KZT,RUB").replace(" ", "").upper().split(","))

# --- Функция получения курсов ---
def fetch_rates(base: str, symbols: List[str]) -> Tuple[Dict[str, float], str]:
    url = "https://api.exchangerate.host/latest"
    params = {"base": base, "symbols": ",".join(symbols)}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if not data or "rates" not in data:
        raise ValueError("Ошибка получения данных")

    rates = {}
    for s in symbols:
        val = data["rates"].get(s)
        if val:
            rates[s] = val
    updated = data.get("date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    return rates, updated


# --- Команды Telegram ---

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = (
        f"👋 Привет! Я валютный бот.\n"
        f"Базовая валюта: {BASE_CURRENCY}\n"
        f"Отслеживаю: {', '.join(TARGETS)}\n\n"
        f"Доступные команды:\n"
        f"/rates – показать курсы\n"
        f"/setbase <валюта> – сменить базовую валюту\n"
        f"/add <валюта> – добавить валюту в список\n"
        f"/remove <валюта> – удалить валюту из списка\n"
        f"/list – показать настройки\n"
        f"/help – список команд"
    )
    await update.message.reply_text(msg)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📌 Список команд:\n"
        "/start – приветствие и помощь\n"
        "/rates – курсы валют\n"
        "/setbase <валюта> – изменить базовую валюту\n"
        "/add <валюта> – добавить валюту\n"
        "/remove <валюта> – удалить валюту\n"
        "/list – список настроек"
    )


async def list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"⚙️ Настройки:\n"
        f"Базовая валюта: {BASE_CURRENCY}\n"
        f"Отслеживаемые валюты: {', '.join(TARGETS)}"
    )


async def rates_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        rates, updated = fetch_rates(BASE_CURRENCY, list(TARGETS))
        lines = [f"📊 Курсы к {BASE_CURRENCY} (обновлено {updated}):"]
        for s, val in rates.items():
            lines.append(f"1 {s} = {val:.4f} {BASE_CURRENCY}")
        await update.message.reply_text("\n".join(lines))
    except Exception as e:
        logger.exception("Ошибка получения курсов")
        await update.message.reply_text(f"⚠️ Ошибка: {e}")


async def setbase_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global BASE_CURRENCY
    if not context.args:
        await update.message.reply_text("❌ Используйте: /setbase <валюта>")
        return
    BASE_CURRENCY = context.args[0].upper()
    await update.message.reply_text(f"✅ Базовая валюта изменена на {BASE_CURRENCY}")


async def add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global TARGETS
    if not context.args:
        await update.message.reply_text("❌ Используйте: /add <валюта>")
        return
    TARGETS.add(context.args[0].upper())
    await update.message.reply_text(f"✅ Добавлена {context.args[0].upper()}")


async def remove_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global TARGETS
    if not context.args:
        await update.message.reply_text("❌ Используйте: /remove <валюта>")
        return
    cur = context.args[0].upper()
    if cur in TARGETS:
        TARGETS.remove(cur)
        await update.message.reply_text(f"✅ Удалена {cur}")
    else:
        await update.message.reply_text(f"⚠️ {cur} не найдена в списке")


# --- Основная функция ---
def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не задан. Проверьте .env")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("list", list_handler))
    app.add_handler(CommandHandler("rates", rates_handler))
    app.add_handler(CommandHandler("setbase", setbase_handler))
    app.add_handler(CommandHandler("add", add_handler))
    app.add_handler(CommandHandler("remove", remove_handler))

    logger.info("Бот запущен 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()
