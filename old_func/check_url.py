# check_url.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException


def check_url(driver, url):
    try:

        current_url = driver.current_url.rstrip("/")
        target_url = url.rstrip("/")

        if current_url == target_url:
            logging.info(f"Уже на нужной странице: {url}")
            wait = WebDriverWait(driver, 100)
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            return
        else:
            logging.info(f"Переход на: {url}")
            driver.get(url)

            wait = WebDriverWait(driver, 100)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))


            logging.info(f"Страница загружена успешно: {url}")
    except Exception as e:
        error_msg = f"Ошибка при открытии URL❌: {url}\n{str(e)}"
        logging.error(error_msg)
        raise Exception(f"check_url error❌: {url}\n {error_msg}")
