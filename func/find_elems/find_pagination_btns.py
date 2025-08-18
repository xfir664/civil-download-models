# find_pagination_btns.py

from selenium.webdriver.common.by import By
from func.set_new_error import set_new_error
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_pagination_btns(driver, path, found_by = By.XPATH):
    try:
        pagination_btns = driver.find_elements(found_by, path)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((found_by, path)))
        if pagination_btns:
            return pagination_btns
        else:
            return None
    except Exception as e:
        set_new_error({
            "error_message": f"⚠️ Ошибка при поиске кнопок пагинации:",
            "error_data": e,
            "error_type": "find_pagination_btns",
        })