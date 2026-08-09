passwords = ["123", "qwerty12345", "password_without_numbers", "super_secure_99", "1234567890"]
strong_count = 0
for item in passwords:
    if len(item) > 8 and any(char.isdigit() for char in item) and any(char.isalpha() for char in item):
        print (f"Надежный пароль: {item}")
        strong_count += 1
print(f"Всего надежный паролей: {strong_count}")
