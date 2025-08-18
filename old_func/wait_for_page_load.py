from selenium.webdriver.support import expected_conditions as EC
import time

def wait_for_page_load(driver, wait, stable_locator):
    """
    Ждёт, пока страница загрузится, проверяя появление стабильного элемента
    """
    print("Waiting for page to reload...")
    wait.until(EC.presence_of_element_located(stable_locator))
    # Можно добавить небольшую паузу, если контент подгружается дольше
    time.sleep(5)