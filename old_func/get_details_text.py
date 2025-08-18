# get_details_text.py
from selenium.webdriver.common.by import By

def get_details_text(details):
    elems = details.find_elements(By.XPATH, ".//*")
    
    return "\n".join([elem.text for elem in elems])
