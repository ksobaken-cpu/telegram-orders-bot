import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
import openpyxl

os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['ALL_PROXY'] = ''

# Настройки бота
TOKEN = "8746914237:AAG9fKVPxxZ2luRdHawIApDxXi7tlbMFCsk"
ADMIN_ID = 876876919  # Вставьте сюда ваш ID (число)

bot = Bot(token=TOKEN)
dp = Dispatcher()

EXCEL_FILE = "orders.xlsx"


# Функция сохранения с защитой от ошибок открытия файла
def save_to_excel(user_name, user_id, text):
  try:
    if not os.path.exists(EXCEL_FILE):
      wb = openpyxl.Workbook()
      ws = wb.active
      ws.title = "Заявки"
      ws.append(["Имя", "ID пользователя", "Текст заявки"])
      wb.save(EXCEL_FILE)

    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active
    ws.append([user_name, user_id, text])
    wb.save(EXCEL_FILE)
    return True
  except PermissionError:
    print(
        f"ОШИБКА: Файл {EXCEL_FILE} открыт в Excel! Закройте его для сохранения"
        " данных."
    )
    return False


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
  builder = ReplyKeyboardBuilder()
  builder.button(text="📝 Оставить заявку")

  await message.answer(
      f"Привет, {message.from_user.first_name}! 👋\n"
      "Я бот для приёма заявок. Нажми кнопку ниже или просто напиши свою заявку"
      " текстом!",
      reply_markup=builder.as_markup(resize_keyboard=True),
  )


@dp.message(F.text == "📝 Оставить заявку")
async def btn_click(message: types.Message):
  await message.answer("Напиши текстом, какую услугу ты хочешь заказать:")


@dp.message()
async def handle_order(message: types.Message):
  user_name = message.from_user.full_name
  username = (
      f"@{message.from_user.username}"
      if message.from_user.username
      else "нет юзернейма"
  )
  user_id = message.from_user.id
  order_text = message.text

  # 1. Сохраняем в Excel и фиксируем результат в переменной saved
  saved = save_to_excel(user_name, user_id, order_text)

  # 2. Отправляем уведомление администратору
  admin_text = (
      f"🔔 **НОВАЯ ЗАЯВКА!**\n\n"
      f"👤 **От кого:** {user_name} ({username})\n"
      f"🆔 **ID:** `{user_id}`\n\n"
      f"📝 **Текст заявки:**\n{order_text}"
  )

  try:
    await bot.send_message(
        chat_id=ADMIN_ID, text=admin_text, parse_mode="Markdown"
    )
  except Exception as e:
    print(f"Ошибка отправки админу: {e}")

  # 3. Отвечаем пользователю в зависимости от результата записи
  if saved:
    await message.answer(
        f"✅ Спасибо, {user_name}! Твоя заявка принята и передана менеджеру."
    )
  else:
    await message.answer(
        "⚠️ Заявка принята и отправлена менеджеру, но пока не записана в Excel"
        " (файл открыт у администратора)."
    )


async def main():
  print("Бот запущен и ждёт сообщений...")
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())