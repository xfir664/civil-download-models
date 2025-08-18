# get_description_text.py

from selenium.webdriver.common.by import By

def get_description_text(description):
    elements = description.find_elements(By.XPATH, ".//*")
    return [element.text for element in elements]