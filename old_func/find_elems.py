# find_elems.py

from selenium.webdriver.common.by import By

def find_elems(driver, element, by=By.CLASS_NAME):
    try:
        elems = driver.find_elements(by, element)
        print(f"find_elems success: {element} ✅")
        return elems
    except Exception as e:
        raise Exception(f"find_elems error❌: {element} not found")
    