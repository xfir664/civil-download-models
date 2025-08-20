# create_img_desc.py

from func.set_new_error import set_new_error
from selenium.webdriver.common.by import By
import os

def create_img_desc(img_path, img_description, index = 0):
    try:
        data_list = img_description.find_element(By.XPATH, ".//ul[contains(@class, 'flex list-none flex-col')]")
        data_list_items = data_list.find_elements(By.XPATH, ".//li[contains(@class, 'flex flex-col')]")
        if len(data_list_items) >= 3:
            list_show_more_btns = img_description.find_elements(By.XPATH, ".//div[contains(@class, 'flex flex-col')]//div[contains(@class, 'flex justify-start')]//p[contains(@class, 'mantine-focus-auto cursor-pointer')]")
            if list_show_more_btns: 
                list_show_more_btns[0].click()
    except Exception as e:
        set_new_error({
            "error_data": e,
            "error_message": f"⚠️ Ошибка при раскрытии списка:",
            "error_type": "data list show more",
        })
    try:
        prompts_container = img_description.find_elements(By.XPATH, ".//div[contains(@class, 'mantine-focus-auto relative break-words') and contains(@class, 'mantine-Text-root')]")

        for prompt in prompts_container:
            sm_btn = prompt.find_elements(By.XPATH, ".//span[contains(@class, 'absolute') and contains(@class, 'bottom-0') and contains(@class, 'right-0') and contains(@class, 'flex') and contains(@class, 'select-none') and contains(@class, 'items-end')]")
            if sm_btn:
                for btn in sm_btn:
                    btn.click()
    except Exception as e:
        set_new_error({
            "error_data": e,
            "error_message": f"⚠️ Ошибка при раскрытии списка:",
            "error_type": "sm_btn",
        })

                

    pos_promot = img_description.find_elements(By.XPATH, ".//div[contains(@class, 'flex flex-col') and .//text()[contains(., 'Prompt')]]")

    negative_prompt = img_description.find_elements(By.XPATH, ".//div[contains(@class, 'flex flex-col') and .//text()[contains(., 'Negative prompt')]]")

    prompt_text = ''

    if pos_promot:
        for prompt in pos_promot:
            prompt_text += prompt.text + '\n'

    if negative_prompt:
        for prompt in negative_prompt:
            prompt_text += prompt.text + '\n'
    
    try:
        if not os.path.isfile(os.path.join(img_path, f"img-{index}.txt")):

            img_description_link_list = img_description.find_element(By.XPATH, ".//ul[contains(@class, 'flex list-none flex-col')]")
            img_description_links = img_description_link_list.find_elements(By.XPATH, ".//li[contains(@class, 'flex flex-col')]")

            img_description_links_output = []
            for link in img_description_links:
                img_link = link.find_element(By.XPATH, ".//a")
                img_det_link_type = link.find_element(By.XPATH, ".//div[contains(@class, 'flex gap-1')]")
                img_href = img_link.get_attribute("href")
                img_text = img_link.text.strip()
                if img_href and img_text:
                    img_description_links_output.append(f"{img_det_link_type.text}\n {img_text}\n {img_href}\n ")
                elif img_href:
                    img_description_links_output.append(img_href)




            complite_img_links = "\n".join(img_description_links_output)
    
            with open(os.path.join(img_path, f"img-{index}.txt"), "w", encoding="utf-8") as f:
                f.write(complite_img_links + '\n' + prompt_text)
            print(f"✅ Image description file created: {os.path.join(img_path, f'img-{index}.txt')}")
        else:
            print(f"⚠️ Skipped: {os.path.join(img_path, f'img-{index}.txt')} already exists")
    except Exception as e:
        set_new_error({
            "error_message": f"⚠️ Ошибка при создании файла описания изображения:",
            "error_data": e,
            "error_type": "create_img_desc",
        })
