# find_verson_div.py

from func.set_new_error import set_new_error
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_version_div(driver, path, found_by = By.XPATH):
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((found_by, path)))
        version_div = driver.find_element(found_by, path)
        return version_div
    except Exception as e:
        set_new_error({
            "error_message": f"❌ Ошибка при получении версии :",
            "error_data": e,
            "error_type": "find_verson_div",
        })