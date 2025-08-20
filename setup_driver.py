# setup_driver.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHROME_BINARY_PATH = os.path.join(BASE_DIR, "chrome", "chrome.exe")
CHROMEDRIVER_PATH = os.path.join(BASE_DIR, "chrome", "chromedriver.exe")
CHROME_USER_DATA_DIR = os.path.join(BASE_DIR, "chrome", "User Data")
PROFILE_DIRECTORY = "Default"

assert os.path.isfile(CHROME_BINARY_PATH), f"Chrome не найден: {CHROME_BINARY_PATH}"
assert os.path.isfile(CHROMEDRIVER_PATH), f"Chromedriver не найден: {CHROMEDRIVER_PATH}"

def setup_driver():
    chrome_options = Options()
    chrome_options.binary_location = CHROME_BINARY_PATH
    
    # Чистый профиль
    chrome_options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
    chrome_options.add_argument(f"--profile-directory={PROFILE_DIRECTORY}")
    
    # Анти-автоматизация
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    # Безопасность и производительность
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--disable-extensions")  # Может мешать, но безопаснее
    chrome_options.add_argument("--start-maximized")
    
    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)