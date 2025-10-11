import os
import logging
from datetime import datetime
from typing import Dict, List, Tuple

import requests
from dotenv import load_dotenv
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, ContextTypes, CallbackQueryHandler
)

# ---------------- ЛОГИРОВАНИЕ ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("rates-bot")

# ---------------- НАСТРОЙКИ ----------------
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_CURRENCY = os.getenv("BASE_CURRENCY", "TJS").upper()
TARGETS = set(os.getenv("TARGETS", "USD,EUR,KZT,RUB").replace(" ", "").upper().split(","))
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

SUBSCRIBERS_FILE = "subscribers.txt"


# ---------------- УТИЛИТЫ ----------------
def get_subscribers() -> List[int]:
    if not os.path.exists(SUBSCRIBERS_FILE):
        return []
    with open(SUBSCRIBERS_FILE, "r") as f:
        return [int(x.strip()) for x in f if x.strip().isdigit()]


def add_subscriber(user_id: int):
    subs = set(get_subscribers())
    subs.add(user_id)
    with open(SUBSCRIBERS_FILE, "w") as f:
        for s in subs:
            f.write(f"{s}\n")


def remove_subscriber(user_id: int):
    subs = set(get_subscribers())
    subs.discard(user_id)
    with open(SUBSCRIBERS_FILE, "w") as f:
        for s in subs:
            f.write(f"{s}\n")


# ---------------- API ----------------
def fetch_rates(base: str, symbols: List[str]) -> Tuple[Dict[str, float], str]:
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base}"
    resp = requests.get(url, timeout=10)
    data = resp.json()

    if data.get("result") != "success":
        raise ValueError(f"Ошибка API: {data.get('error-type', 'неизвестная')}")

    rates = data["conversion_rates"]
    updated = data.get("time_last_update_utc", "неизвестно")
    return {s: rates[s] for s in symbols if s in rates}, updated


# ---------------- МЕНЮ ----------------
def main_menu_keyboard(is_admin=False):
    keyboard = [
        [InlineKeyboardButton("📊 Курсы валют", callback_data="show_rates")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")],
        [
            InlineKeyboardButton("📬 Подписаться", callback_data="subscribe"),
            InlineKeyboardButton("🚫 Отписаться", callback_data="unsubscribe"),
        ],
        [InlineKeyboardButton("💬 Помощь", callback_data="help")]
    ]
    if is_admin:
        keyboard.append([InlineKeyboardButton("🛠 Админ-панель", callback_data="admin_panel")])
    return InlineKeyboardMarkup(keyboard)


def settings_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🇺🇸 USD", callback_data="base_USD"),
            InlineKeyboardButton("🇪🇺 EUR", callback_data="base_EUR"),
            InlineKeyboardButton("🇹🇯 TJS", callback_data="base_TJS"),
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


def admin_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📋 Подписчики", callback_data="admin_subs")],
        [InlineKeyboardButton("📤 Разослать курсы", callback_data="admin_sendnow")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)


# ---------------- ОБРАБОТЧИКИ ----------------
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = (
        "👋 <b>Привет!</b>\n"
        "Я валютный бот. Узнавай актуальные курсы и получай рассылку 📬"
    )
    is_admin = (user_id == ADMIN_ID)
    await update.message.reply_text(msg, parse_mode="HTML", reply_markup=main_menu_keyboard(is_admin))


async def rates_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        rates, updated = fetch_rates(BASE_CURRENCY, list(TARGETS))
        text = f"📊 <b>Курсы к {BASE_CURRENCY}</b>\n🕓 Обновлено: {updated}\n\n"
        for s, v in rates.items():
            text += f"💰 1 <b>{s}</b> = <b>{v:.4f}</b> {BASE_CURRENCY}\n"
        await query.edit_message_text(text, parse_mode="HTML", reply_markup=main_menu_keyboard(query.from_user.id == ADMIN_ID))
    except Exception as e:
        await query.edit_message_text(f"⚠️ Ошибка: {e}", reply_markup=main_menu_keyboard(query.from_user.id == ADMIN_ID))


async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"⚙️ Текущая базовая валюта: <b>{BASE_CURRENCY}</b>\nВыберите новую:", parse_mode="HTML", reply_markup=settings_menu_keyboard())


async def set_base_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BASE_CURRENCY
    query = update.callback_query
    await query.answer()
    BASE_CURRENCY = query.data.split("_")[1]
    await query.edit_message_text(f"✅ Базовая валюта изменена на <b>{BASE_CURRENCY}</b>", parse_mode="HTML", reply_markup=main_menu_keyboard(query.from_user.id == ADMIN_ID))


async def subscribe_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    add_subscriber(query.from_user.id)
    await query.answer("Подписка активна ✅")
    await query.edit_message_text("📬 Теперь вы будете получать рассылку.", reply_markup=main_menu_keyboard(query.from_user.id == ADMIN_ID))


async def unsubscribe_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    remove_subscriber(query.from_user.id)
    await query.answer("Вы отписались ❌")
    await query.edit_message_text("🚫 Рассылка отключена.", reply_markup=main_menu_keyboard(query.from_user.id == ADMIN_ID))


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "💬 <b>Помощь:</b>\n\n"
        "📊 Курсы валют — показать актуальные курсы.\n"
        "⚙️ Настройки — выбрать базовую валюту.\n"
        "📬 Подписка — получать уведомления.\n"
        "🛠 Админ-панель — только для администратора."
    )
    await query.edit_message_text(text, parse_mode="HTML", reply_markup=main_menu_keyboard(query.from_user.id == ADMIN_ID))


# ---------------- АДМИН ----------------
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_ID:
        await query.answer("🚫 Нет доступа", show_alert=True)
        return
    text = "🛠 <b>Админ-панель</b>\n\nВыберите действие:"
    await query.edit_message_text(text, parse_mode="HTML", reply_markup=admin_menu_keyboard())


async def admin_show_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subs = get_subscribers()
    if subs:
        msg = f"👥 Подписчиков: {len(subs)}\n\n" + "\n".join([f"• {s}" for s in subs])
    else:
        msg = "❌ Пока нет подписчиков."
    await query.edit_message_text(msg, reply_markup=admin_menu_keyboard())


async def admin_sendnow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Рассылка запущена ✅")

    subs = get_subscribers()
    if not subs:
        await query.edit_message_text("❌ Нет подписчиков для рассылки.", reply_markup=admin_menu_keyboard())
        return

    try:
        rates, updated = fetch_rates(BASE_CURRENCY, list(TARGETS))
        text = f"📢 <b>Рассылка</b>\n🕓 {updated}\n\n"
        for s, v in rates.items():
            text += f"💰 1 <b>{s}</b> = <b>{v:.4f}</b> {BASE_CURRENCY}\n"
        for uid in subs:
            try:
                await context.bot.send_message(chat_id=uid, text=text, parse_mode="HTML")
            except Exception as e:
                logger.warning(f"Не удалось отправить пользователю {uid}: {e}")
        await query.edit_message_text("📤 Рассылка выполнена.", reply_markup=admin_menu_keyboard())
    except Exception as e:
        await query.edit_message_text(f"⚠️ Ошибка рассылки: {e}", reply_markup=admin_menu_keyboard())


# ---------------- ЗАПУСК ----------------
def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не найден")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start_handler))

    # Кнопки
    app.add_handler(CallbackQueryHandler(rates_handler, pattern="show_rates"))
    app.add_handler(CallbackQueryHandler(settings_handler, pattern="settings"))
    app.add_handler(CallbackQueryHandler(set_base_handler, pattern="base_"))
    app.add_handler(CallbackQueryHandler(subscribe_handler, pattern="subscribe"))
    app.add_handler(CallbackQueryHandler(unsubscribe_handler, pattern="unsubscribe"))
    app.add_handler(CallbackQueryHandler(help_handler, pattern="help"))
    app.add_handler(CallbackQueryHandler(admin_panel, pattern="admin_panel"))
    app.add_handler(CallbackQueryHandler(admin_show_subs, pattern="admin_subs"))
    app.add_handler(CallbackQueryHandler(admin_sendnow, pattern="admin_sendnow"))
    app.add_handler(CallbackQueryHandler(start_handler, pattern="back_main"))

    # 💤 Временно без авто-рассылки (JobQueue отключён)
    logger.info("🕓 Автоматическая рассылка временно отключена (JobQueue не используется).")

    logger.info("🚀 Бот запущен с админ-панелью.")
    app.run_polling()


if __name__ == "__main__":
    main()
