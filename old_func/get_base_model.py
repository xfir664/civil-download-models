# get_base_model.py

from selenium.webdriver.common.by import By

def get_base_model(items):
    for item in items:
        try: 
            key_el = item.find_element(By.CLASS_NAME, "details-item-text")
            if(key_el.text == "base-mode"):
                return item.find_elements(By.CLASS_NAME, "details-item-text")[1].text
        except Exception as e:
            raise Exception(f" get_base_model error❌: key not found")