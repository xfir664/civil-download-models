import os
import requests
from urllib.parse import urlparse

def download_model(all_elems, driver, download_path):
    """
    Скачивает модель через requests, используя куки из Selenium.
    Получает имя файла из Content-Disposition при первом GET.
    """
    # 1. Получаем ссылку
    download_btn = all_elems["download_btn"]
    href = download_btn.get_attribute("href")
    
    # 2. Настраиваем сессию с куками
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    # 3. Извлекаем имя файла из URL на всякий случай
    filename = "model.safetensors"
    path = urlparse(href).path
    if path:
        filename = os.path.basename(path) or filename
    if not filename.endswith(('.safetensors', '.ckpt', '.pt', '.bin')):
        filename += ".safetensors"

    # 4. Путь к файлу
    file_path = os.path.join(download_path, filename)

    # 5. Проверяем, существует ли файл
    if os.path.isfile(file_path):
        print(f"✅ Файл уже существует: {file_path}")
        return True

    # 6. Пробуем GET-запрос (игнорируем HEAD)
    try:
        print("Cookies:", session.cookies.get_dict())
        print(f"📥 Попытка скачивания: {filename}")
        response = session.get(href, stream=True, allow_redirects=True)
        
        if response.status_code == 403:
            print("❌ Доступ запрещён. Возможно, модель требует авторизации или ограничена.")
            return False
        elif response.status_code != 200:
            print(f"❌ Ошибка {response.status_code}: {response.text[:200]}")
            return False

        # 7. Обновляем имя файла из Content-Disposition
        new_filename = filename
        if "Content-Disposition" in response.headers:
            content_disp = response.headers["Content-Disposition"]
            if "filename*" in content_disp:
                new_filename = content_disp.split("filename*=")[1].split("'")[-1]
            elif "filename" in content_disp:
                new_filename = content_disp.split("filename=")[1].strip('"')
            # Обновляем путь, если имя изменилось
            if new_filename != filename:
                file_path = os.path.join(download_path, new_filename)

        # 8. Повторная проверка: вдруг после редиректа файл уже есть
        if os.path.isfile(file_path):
            print(f"✅ Файл уже существует (после редиректа): {file_path}")
            return True

        # 9. Скачиваем
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Успешно скачан: {file_path}")
        return True

    except Exception as e:
        print(f"❌ Ошибка при скачивании: {e}")
        return False