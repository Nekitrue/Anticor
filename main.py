import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ВАШИ ДАННЫЕ
TOKEN = '8311024618:AAHvEmWzlMwBeStlsPOXud6yowzrA350HRo'
ADMIN_ID = 8311024618 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Логирование (чтобы видеть ошибки в консоли)
logging.basicConfig(level=logging.INFO)

@dp.message(CommandStart())
async def start_command(message: types.Message):
    # Кнопка открытия приложения
    web_app = types.WebAppInfo(url="https://nekitrue.github.io/anticor-bot/")
    
    # Создаем кнопку в меню (Reply Keyboard)
    kb = [
        [types.KeyboardButton(text="🚗 ЗАПИСАТЬСЯ НА АНТИКОР", web_app=web_app)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        "✨ <b>Добро пожаловать в Anticor Pro!</b>\n\n"
        "Воспользуйтесь кнопкой ниже, чтобы рассчитать стоимость "
        "защиты вашего авто и записаться к нам.",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(lambda message: message.web_app_data)
async def handle_order(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        
        # Текст для вас
        admin_text = (
            f"🔔 <b>НОВЫЙ ЗАКАЗ!</b>\n\n"
            f"🚘 Авто: {data['model']}\n"
            f"📐 Класс: {data['car']}\n"
            f"🛠 Пакет: {data['package']}\n"
            f"📅 Дата: {data['date']}\n"
            f"💰 Сумма: {data['total']} ₽\n\n"
            f"👤 Клиент: @{message.from_user.username or 'скрыт'}"
        )

        # Кнопка связи
        builder = InlineKeyboardBuilder()
        link = f"https://t.me/{message.from_user.username}" if message.from_user.username else f"tg://user?id={message.from_user.id}"
        builder.row(types.InlineKeyboardButton(text="💬 Написать клиенту", url=link))

        # Отправка админу
        await bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML", reply_markup=builder.as_markup())
        
        # Ответ клиенту
        await message.answer("✅ <b>Заявка принята!</b>\nМастер свяжется с вами в ближайшее время.", parse_mode="HTML")
        
    except Exception as e:
        logging.error(f"Ошибка: {e}")

async def main():
    print("Бот успешно запущен и слушает команды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")
