# get_type.py

from selenium.webdriver.common.by import By

def get_type(items):
    for item in items:
        try: 
            key_el = item.find_element(By.CLASS_NAME, "details-item-text")
            if(key_el.text == "type"):
                return item.find_elements(By.CLASS_NAME, "details-item-text")[1].text
        except Exception as e:
            raise Exception(f" get_type error❌: key not found")