import requests
import os
from urllib.parse import urlparse

def download_image(img_element, driver, download_path, filename="img-1"):
    """
    Скачивает изображение из img_element и сохраняет в папку.
    :param img_element: WebElement <img>
    :param download_path: Путь для сохранения
    :param filename: Имя файла (без расширения)
    """
    try:
        # 1. Получаем URL изображения
        img_url = img_element.get_attribute("src")
        if not img_url:
            print("❌ Не удалось получить src у изображения")
            return False

        print(f"📥 Скачивание изображения: {img_url}")

        # 2. Определяем расширение файла
        # Пытаемся извлечь из URL или используем .jpg по умолчанию
        parsed_url = urlparse(img_url)
        path = parsed_url.path
        ext = os.path.splitext(path)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            ext = '.jpg'  # fallback

        # 3. Путь к файлу
        file_path = os.path.join(download_path, f"{filename}{ext}")

        # 4. Проверяем, существует ли файл
        if os.path.isfile(file_path):
            print(f"✅ Файл уже существует: {file_path}")
            return True

        # 5. Скачиваем с куками из Selenium
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        response = session.get(img_url, stream=True, timeout=30)
        if response.status_code != 200:
            print(f"❌ Ошибка загрузки: {response.status_code}")
            return False

        # 6. Сохраняем файл
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✅ Изображение сохранено: {file_path}")
        return True

    except Exception as e:
        print(f"❌ Ошибка при скачивании изображения: {e}")
        return False