# create_img_desc.py

from func.set_new_error import set_new_error
from selenium.webdriver.common.by import By
import os

def create_img_desc(img_path, img_description, index = 0):
    try:
        data_list = img_description.find_element(By.XPATH, ".//ul[contains(@class, 'flex list-none flex-col')]")
        data_list_items = data_list.find_elements(By.XPATH, ".//li[contains(@class, 'flex flex-col')]")
        if len(data_list_items) > 3:
            list_show_more_btn = img_description.find_element(By.XPATH, ".//div[contains(@class, 'flex flex-col')]//div[contains(@class, 'flex justify-start')]//p[contains(@class, 'mantine-focus-auto cursor-pointer')]")
            list_show_more_btn.click()
    except Exception as e:
        set_new_error({
            "error_message": f"⚠️ Ошибка при раскрытии списка:",
            "error_type": "create_img_desc",
        })
    print("1")
    try:
        prompts_container = img_description.find_elements(By.XPATH, ".//div[contains(@class, 'mantine-focus-auto relative break-words') and contains(@class, 'mantine-Text-root')]")

        for prompt in prompts_container:
            if prompt.get_attribute("data-line-clamp") == "true":
                prompt.find_element(By.XPATH, ".//span[contains(@class, 'absolute') and contains(@class, 'bottom-0') and contains(@class, 'right-0') and contains(@class, 'flex') and contains(@class, 'select-none') and contains(@class, 'items-end')]").click()
    except Exception as e:
        set_new_error({
            "error_message": f"⚠️ Ошибка при раскрытии списка:",
            "error_type": "create_img_desc",
        })
    print("2")
    
    try:
        if not os.path.isfile(os.path.join(img_path, f"img-{index}.txt")):
            description_text = img_description.find_elements(By.XPATH, ".//*")
            description_text_output = []
            for elem in description_text:
                description_text_output.append(elem.text.strip())

            img_description_links = img_description.find_elements(By.TAG_NAME, "a")
            img_description_links_output = []
            for link in img_description_links:
                img_href = link.get_attribute("href")
                img_text = link.text.strip()
                if img_href and img_text:
                    img_description_links_output.append(f"{img_href} - {img_text}")
                elif img_href:
                    img_description_links_output.append(img_href)

            with open(os.path.join(img_path, f"img-{index}.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(img_description_links_output) + "\n" + "\n".join(description_text_output))
            print(f"✅ Image description file created: {os.path.join(img_path, f'img-{index}.txt')}")
        else:
            print(f"⚠️ Skipped: {os.path.join(img_path, f'img-{index}.txt')} already exists")
    except Exception as e:
        set_new_error({
            "error_message": f"⚠️ Ошибка при создании файла описания изображения:",
            "error_data": e,
            "error_type": "create_img_desc",
        })
    print("3")
