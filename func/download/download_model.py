import os
import requests
from urllib.parse import urlparse
from func.set_new_error import set_new_error

def download_model(driver, download_btn, download_path):
    """
    Скачивает модель через requests, используя куки из Selenium.
    Показывает прогресс в консоли.
    """
    href = download_btn.get_attribute("href")
    
    # Создаём сессию с куками из Selenium
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    # Определяем имя файла
    filename = "model.safetensors"
    path = urlparse(href).path
    if path:
        filename = os.path.basename(path) or filename
    if not filename.endswith(('.safetensors', '.ckpt', '.pt', '.bin')):
        filename += ".safetensors"

    file_path = os.path.join(download_path, filename)

    if os.path.isfile(file_path):
        print(f"✅ Файл уже существует: {file_path}")
        return True

    try:
        print(f"📥 Начинаем скачивание: {filename}")
        response = session.get(href, stream=True, allow_redirects=True)

        if response.status_code == 403:
            print("❌ Доступ запрещён. Возможно, модель требует авторизации.")
            return False
        elif response.status_code != 200:
            print(f"❌ Ошибка {response.status_code}: {response.text[:200]}")
            return False

        # Пытаемся получить имя файла из заголовка
        new_filename = filename
        if "Content-Disposition" in response.headers:
            content_disp = response.headers["Content-Disposition"]
            if "filename*" in content_disp:
                new_filename = content_disp.split("filename*=")[1].split("'")[-1]
            elif "filename" in content_disp:
                new_filename = content_disp.split("filename=")[1].strip('"').strip()
            if new_filename != filename:
                file_path = os.path.join(download_path, new_filename)

        if os.path.isfile(file_path):
            print(f"✅ Файл уже существует (после редиректа): {file_path}")
            return True

        # Получаем общий размер файла
        total_size = int(response.headers.get("content-length", 0))
        block_size = 8192
        downloaded = 0

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    # Показываем прогресс
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r    ⏳ {downloaded / 1024 / 1024:.1f} MB / {total_size / 1024 / 1024:.1f} MB ({percent:.1f}%)", end="", flush=True)
                    else:
                        print(f"\r    ⏳ Скачано: {downloaded / 1024 / 1024:.1f} MB", end="", flush=True)

        print()  # Новая строка после завершения
        print(f"✅ Успешно скачано")
        return True

    except Exception as e:
        set_new_error({
            "error_message": f"⚠️ Ошибка при скачивании модели:",
            "error_data": str(e),
            "error_type": "download_model",
        })
        return False