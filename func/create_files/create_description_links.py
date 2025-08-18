# create_description_links.py

from func.set_new_error import set_new_error
from selenium.webdriver.common.by import By
import os

def create_description_links(path, elem):
    try:
        if not os.path.isfile(path):
            links = elem.find_elements(By.XPATH, ".//a")
            if links:
                for link in links:
                    href = link.get_attribute("href")
                    text = link.text.strip()
                    with open(path, "a", encoding="utf-8") as f:
                        f.write(f"{text} - {href}\n")
                print(f"✅ Description links file created: {path}")
            else:
                print(f"⚠️ No links found in description")
        else:
            print(f"⚠️ Skipped: {path} already exists")
    except Exception as e:
        set_new_error({
            "error_message": f"⚠️ Ошибка при создании файла description:",
            "error_data": e,
            "error_type": "create_description_links",
        })