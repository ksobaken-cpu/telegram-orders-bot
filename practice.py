# prices = {
#     "яблоки": 120,
#     "бананы": 80,
#     "молоко": 90,
#     "хлеб": 45,
#     "сыр": 350
# }
# total_expensive = 0
# for item, price in prices.items():
#     if price > 100:
#         print(f"Дорогой товар: {item} - {price} руб.")
#         total_expensive += price
# print(f"Общая сумма дорогих товаров: {total_expensive} руб.")

# def calculate_discount(price, discount):
#     final_price = price - (price * discount / 100)
#     return final_price
# phone_price = calculate_discount(50000,15)
# laptop_price = calculate_discount(100000,20)
# total_sum = phone_price + laptop_price
# print(f"Телефон со скидкой стоит: {phone_price} руб.")
# print(f"Ноутбук со скдикой стоит: {laptop_price} руб.")
# print(f"Общая цена покупки составляет: {total_sum} руб.")
# def is_even(number):
#     if number % 2 == 0:
#         return True
#     else:
#         return False
# print(is_even(2))
# print(is_even(5))

# prices = [100, 250, 800, 1500, 400]
# new_prices = [round(f * 1.1) for f in prices if f > 300]
# print(new_prices)

# orders = [
#     {"title": "Клавиатура", "price": 2500, "count": 2, "discount": 10},
#     {"title": "Мышь", "price": 900, "count": 1, "discount": 15},
#     {"title": "Монитор", "price": 18000, "count": 1, "discount": 20},
#     {"title": "Коврик", "price": 400, "count": 3, "discount": 5},
#     {"title": "Наушники", "price": 4500, "count": 2, "discount": 10}
# ]
# def get_total_spent(orders):
#     total = [item["price"] * item["count"] * (1 - item["discount"] / 100) for item in orders]
#     return sum(total)
# print (int(get_total_spent(orders)))

orders = [
    {"title": "Клавиатура", "price": 2500, "count": 2},
    {"title": "Мышь", "price": 900, "count": 1},
    {"title": "Монитор", "price": 18000, "count": 1},
    {"title": "Коврик", "price": 400, "count": 3},
    {"title": "Наушники", "price": 4500, "count": 5}
]
most_popular = max(orders, key=lambda item: item["count"])
print(most_popular["title"])