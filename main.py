import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Ваши данные
TOKEN = '8311024618:AAHvEmWzlMwBeStlsPOXud6yowzrA350HRo'
ADMIN_ID = 8311024618  # Ваш ID теперь прописан здесь

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    # Ссылка на ваше приложение на GitHub
    web_app = types.WebAppInfo(url="https://nekitrue.github.io/anticor-bot/")
    kb = [[types.KeyboardButton(text="🚗 Записаться на антикор", web_app=web_app)]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Привет! Нажми на кнопку ниже для расчета цены и записи:", reply_markup=keyboard)

@dp.message(lambda message: message.web_app_data)
async def handle_order(message: types.Message):
    # Парсим данные из Mini App
    data = json.loads(message.web_app_data.data)
    user_id = message.from_user.id
    username = message.from_user.username

    # 1. Сообщение для вас (админа)
    admin_text = (
        f"🔔 <b>НОВЫЙ ЗАКАЗ</b>\n\n"
        f"🚘 <b>Авто:</b> {data['model']}\n"
        f"📐 <b>Класс:</b> {data['car']}\n"
        f"🛠 <b>Пакет:</b> {data['package']}\n"
        f"📅 <b>Дата:</b> {data['date']}\n"
        f"💰 <b>Итого:</b> {data['total']} ₽\n\n"
        f"👤 <b>Клиент:</b> @{username or 'скрыт'}\n"
    )

    # Кнопка для быстрой связи
    builder = InlineKeyboardBuilder()
    link = f"https://t.me/{username}" if username else f"tg://user?id={user_id}"
    builder.row(types.InlineKeyboardButton(text="💬 Написать клиенту", url=link))

    # Отправка вам
    await bot.send_message(
        chat_id=ADMIN_ID, 
        text=admin_text, 
        parse_mode="HTML", 
        reply_markup=builder.as_markup()
    )

    # 2. Сообщение клиенту
    client_text = (
        f"✅ <b>Запись успешно создана!</b>\n\n"
        f"Автомобиль: <b>{data['model']}</b>\n"
        f"Пакет: {data['package']}\n\n"
        f"📞 Мастер свяжется с вами для подтверждения.\n"
        f"Наш номер: +79623133313"
    )
    
    await message.answer(text=client_text, parse_mode="HTML")

async def main():
    print("Бот ANTICOR запущен и работает...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
