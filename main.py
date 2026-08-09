import os
folder = os.path.dirname(__file__)
file_path = os.path.join(folder, "tasks.txt")
tasks = {}
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                name, status = line.split(" | ")
                tasks[name] = status
while True:
    print("\n--- МЕНЕДЖЕР ЗАДАЧ ---")
    print("1. Добавить задачу")
    print("2. Показать все задачи")
    print("3. Выполнить задачу")
    print("4. Выход")

    user_choice = input("Выберите ваше действие: (1-4): ")
    if user_choice == "1":
        task_name = input("Введите название задачи:" )
        tasks[task_name] = "В процессе"
    elif user_choice == "2":
        if not tasks:
            print("Задач пока нет.")
        else:
            for name, status in tasks.items():
                print(f"{name} | {status}")
    elif user_choice == "3":
        task_name = input("Какую задачу вы выполнили?: ")
        if task_name in tasks:
            tasks[task_name] = "Выполнено"
        else:
            print("Такой задачи не существует")
    elif user_choice == "4":
        with open(file_path, "w", encoding="utf-8") as f:
            for name, status in tasks.items():
                f.write(f"{name} | {status}\n")
        print("Выход из программы.")
        break
        