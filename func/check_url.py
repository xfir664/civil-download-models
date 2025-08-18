# check_url.py

from func.set_new_error import set_new_error
from func.wait_page_loaded import wait_page_loaded

def check_url(driver, url):
    try:
        print(f"🔍 Проверка URL: {url}")
        current_url = driver.current_url.rstrip("/")
        target_url = url.rstrip("/")

        if current_url == target_url:
            wait_page_loaded(driver)
            print(f"✅ URL уже открыт: {url}")
            return
        else:
            print(f"🔍 Переход на: {url}")
            driver.get(url)
            wait_page_loaded(driver)
            print(f"✅ URL открыт: {url}")

    except Exception as e:
        set_new_error({
            "error_message": f"❌ Ошибка при открытии URL:",
            "error_data": e,
            "error_type": "check_url",
        })
