# set_new_error.py

ERRORS = []

def set_new_error(error):
    ERRORS.append(error)
    print(f"Ошибка добавлена: {error}")
    print(f"Всего ошибок: {len(ERRORS)}")
