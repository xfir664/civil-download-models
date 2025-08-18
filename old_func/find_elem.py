# find_elem.py

from selenium.webdriver.common.by import By

def find_elem(driver, element, by=By.CLASS_NAME):
    try:
        elem = driver.find_element(by, element)
        print(f"find_elem success: {element} ✅")
        return elem
    except Exception as e:
        raise Exception(f"find_elem error❌: {element}  not found")
    