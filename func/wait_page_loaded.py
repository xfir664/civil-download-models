# wait_page_loaded.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def wait_page_loaded(driver):
    wait = WebDriverWait(driver, 100)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(10)
    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    return