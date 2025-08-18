# get_description_links.py

from selenium.webdriver.common.by import By

def get_description_links(description):
    links = []

    links_el = description.find_elements(By.XPATH, ".//a")

    for link_el in links_el:
        try: 
            link = link_el.get_attribute("href")
            text = link_el.text
            links.append({"link": link, "text": text})
        except Exception as e:
            raise Exception(f" get_description_links error❌: link_el not found")
    print(f"get_description_links success✅")
    return links