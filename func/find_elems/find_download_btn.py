# find_dowdload_btn.py

from func.set_new_error import set_new_error
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_download_btn(driver, path, found_by = By.XPATH):
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((found_by, path)))
        btn = driver.find_element(found_by, path)
        return btn
    except Exception as e:
        set_new_error({
            "error_message": f"❌ Ошибка при получении кнопки загрузки :",
            "error_data": e,
            "error_type": "find_download_btn",
        })