import os
import time
from bs4 import BeautifulSoup
import openpyxl
import requests

os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["ALL_PROXY"] = ""

# Создаем файл Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Книги"
ws.append(["Название книги", "Цена"])

total_books = 0

# Проходим циклом по страницам с 1 по 50
for page in range(1, 51):
  url = f"http://books.toscrape.com/catalogue/page-{page}.html"
  print(f"Парсим страницу {page} из 50...")

  response = requests.get(url, proxies={"http": None, "https": None})
  response.encoding = "utf-8"

  soup = BeautifulSoup(response.text, "html.parser")
  books = soup.find_all("article", class_="product_pod")

  for book in books:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text.replace("Â", "")
    ws.append([title, price])
    total_books += 1

  # Пауза 0.2 секунды, чтобы не забанить сайт частыми запросами (хорошая практика!)
  time.sleep(0.2)

# Сохраняем итоговый файл
wb.save("books_result.xlsx")
print(f"Готово! Спарсено всего книг: {total_books}. Файл сохранен!")