import asyncio
import os
from datetime import datetime
import openpyxl
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv

# 1. Загрузка переменных
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 876876919))  # Чтение ADMIN_ID из .env или дефолт

# Сброс прокси
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['ALL_PROXY'] = ''

bot = Bot(token=TOKEN)
dp = Dispatcher()

EXCEL_FILE = "orders.xlsx"


# Функция сохранения в Excel с датой и статусом
def save_to_excel(user_name, user_id, text):
    try:
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not os.path.exists(EXCEL_FILE):
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Заявки"
            ws.append(["Дата и время", "Имя", "ID пользователя", "Текст заявки", "Статус"])
            wb.save(EXCEL_FILE)

        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active
        ws.append([date_now, user_name, user_id, text, "Новая"])
        wb.save(EXCEL_FILE)
        return True
    except PermissionError:
        print(f"ОШИБКА: Файл {EXCEL_FILE} открыт в Excel!")
        return False


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text="📝 Оставить заявку")

    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я бот для приёма заявок. Нажми кнопку ниже или просто напиши свою заявку текстом!",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(F.text == "📝 Оставить заявку")
async def btn_click(message: types.Message):
    await message.answer("Напиши текстом, какую услугу ты хочешь заказать:")


@dp.message()
async def handle_order(message: types.Message):
    user_name = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "нет юзернейма"
    user_id = message.from_user.id
    order_text = message.text

    saved = save_to_excel(user_name, user_id, order_text)

    # Клавиатура с inline-кнопкой для администратора
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Отметить выполненной",
                    callback_data=f"done_{user_id}",
                )
            ]
        ]
    )

    admin_text = (
        f"🔔 **НОВАЯ ЗАЯВКА!**\n\n"
        f"👤 **От кого:** {user_name} ({username})\n"
        f"🆔 **ID:** `{user_id}`\n\n"
        f"📝 **Текст заявки:**\n{order_text}\n\n"
        f"📌 **Статус:** 🟡 В обработке"
    )

    try:
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")

    if saved:
        await message.answer(f"✅ Спасибо, {user_name}! Твоя заявка принята и передана менеджеру.")
    else:
        await message.answer("⚠️ Заявка отправлена менеджеру, но пока не записана в Excel (файл открыт у администратора).")


# Обработчик нажатия на Inline-кнопку
@dp.callback_query(F.data.startswith("done_"))
async def mark_as_done(callback: types.CallbackQuery):
    target_user_id = callback.data.split("_")[1]

    # Обновляем текст сообщения админу
    new_text = callback.message.text.replace("📌 Статус: 🟡 В обработке", "📌 Статус: ✅ Выполнено")

    # Убираем кнопку, чтобы нельзя было нажать дважды
    await callback.message.edit_text(text=f"{new_text}\n\n🎉 *Заявка успешно закрыта!*", parse_mode="Markdown")

    # Отправляем уведомление пользователю
    try:
        await bot.send_message(
            chat_id=target_user_id,
            text="🎉 Твоя заявка успешно обработана и выполнена!",
        )
    except Exception as e:
        print(f"Не удалось отправить статус пользователю: {e}")

    await callback.answer("Статус обновлен!")


async def main():
    print("Бот запущен и ждёт сообщений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())