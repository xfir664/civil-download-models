# download_page_img.py

from func.set_new_error import set_new_error
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import os
import requests





def download_page_img(img_path, driver, index = 0):
    try:
        img_container = driver.find_element(By.XPATH, ".//div[contains(@class, 'flex min-h-0 flex-1 items-stretch justify-stretch')]")
        image = img_container.find_element(By.XPATH, ".//img[contains(@class, 'EdgeImage_image__iH4_q')]")
        img_url = image.get_attribute("src")
        if not img_url:
            print("❌ Не удалось получить src у изображения")
            return False
        
        parsed_url = urlparse(img_url)
        path = parsed_url.path
        ext = os.path.splitext(path)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            ext = '.jpg'

        file_path = os.path.join(img_path, f"img-{index}{ext}")
        if os.path.isfile(file_path):
            print(f"⚠️ Skipped: {file_path} already exists")
            return False

        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])
        
        response = session.get(img_url, stream=True, timeout=30)
        if response.status_code != 200:
            print(f"❌ Ошибка загрузки: {response.status_code}")
            return False

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✅ Изображение успешно скачано: {file_path}")
        return True

    except Exception as e:
        set_new_error({
            "error_message": f"⚠️ Ошибка при загрузке изображения:",
            "error_data": e,
            "error_type": "download_page_img",
        })