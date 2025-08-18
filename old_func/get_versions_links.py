# get_versions_links.py

from func.find_elem import find_elem
from selenium.webdriver.common.by import By

def get_versions_links(driver, class_name):
    try:
        versions_block = find_elem(driver, class_name)
        versions_links = versions_block.find_elements(By.TAG_NAME, "a")
        links = []
        for link in versions_links:
            text = link.text
            link = link.get_attribute("href")
            links.append({"text": text, "link": link})
        print(f"get_versions_links success✅")
        return links

    except Exception as e:
        raise Exception(f"get_versions_links error❌: link not found")
