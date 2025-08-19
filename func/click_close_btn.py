from selenium.webdriver.common.by import By
from func.set_new_error import set_new_error
import time

def click_close_btn(driver):
    time.sleep(5)
    try:
        close_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'mantine-focus-auto mantine-active size-9 rounded-full m_86a44da5 mantine-CloseButton-root m_87cf2631 mantine-UnstyledButton-root')]")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", close_btn)
        close_btn.click()
    except Exception as e:
        set_new_error({
            "error_message": f"⚠️ Ошибка при закрытии окна:",
            "error_data": e,
            "error_type": "click_close_btn",
        })