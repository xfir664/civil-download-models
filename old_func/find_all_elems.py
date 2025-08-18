# find all elems in the page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_all_elems(driver, elems):
    try:
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.XPATH, elems["title"])))
        title = driver.find_element(By.XPATH, elems["title"])
        print('title found ✅')
        wait.until(EC.presence_of_element_located((By.XPATH, elems["description_container"])))
        description_container = driver.find_element(By.XPATH, elems["description_container"])
        print('description_container found ✅')
        wait.until(EC.presence_of_element_located((By.XPATH, elems["details_container"])))
        details_container = driver.find_element(By.XPATH, elems["details_container"])
        print('details_container found ✅')
        wait.until(EC.presence_of_element_located((By.XPATH, elems["image_link"])))
        image_link = driver.find_element(By.XPATH, elems["image_link"])
        print('image_link found ✅')
        wait.until(EC.presence_of_element_located((By.XPATH, elems["download_btn"])))
        download_btn = driver.find_element(By.XPATH, elems["download_btn"])
        print('download_btn found ✅')
        wait.until(EC.presence_of_element_located((By.XPATH, elems["details_type"])))
        details_type = details_container.find_element(By.XPATH, elems["details_type"])
        print(f'details_type found ✅: {details_type.text}')
        wait.until(EC.presence_of_element_located((By.XPATH, elems["details_base_model"])))
        details_base_model = details_container.find_element(By.XPATH, elems["details_base_model"])
        print(f'details_base_model found ✅: {details_base_model.text}')
        return {
            "title": title,
            "description_container": description_container,
            "details_container": details_container,
            "image_link": image_link,
            "download_btn": download_btn,
            "details_type": details_type,
            "details_base_model": details_base_model,
        }
    except Exception as e:
        print(f"REAL ERROR: {type(e).__name__}: {e}")







