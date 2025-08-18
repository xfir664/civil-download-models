# main.py
from operator import itemgetter
from selenium import webdriver
from setup_driver import setup_driver
from func.check_url import check_url
from func.find_all_elems import find_all_elems
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from func.wait_for_page_load import wait_for_page_load
from func.sanitize_windows_path import sanitize_windows_path
from func.wait_download_end import wait_download_end
from func.download_model import download_model
from func.extract_image_description import extract_image_description
from func.download_image import download_image
import os
import time
from selenium.webdriver.common.action_chains import ActionChains



elems = {
    "title": "//h1[contains(@class, 'mantine-Title-root')]",

    "version_container": "//div[contains(@class, 'mantine-Group-root') and contains(@style, '--group-justify: flex-start')]",

    "version_btns": "//button[contains(@class, 'mantine-Button-root') and @data-variant='filled' and @data-size='compact-sm']",

    "description_container": "//div[contains(@class, 'mantine-TypographyStylesProvider-root')]",

    "details_container": "//div[contains(@class, 'mantine-Accordion-item') and @data-active='true']",

    "image_link": "(//div[contains(@class, 'ModelVersionDetails_mainSection__46plL')]//a[.//img[contains(@class, 'EdgeImage_image__iH4_q')]])",

    "download_btn": "//a[@data-tour='model:download']",

    "details_type": ".//p[normalize-space()='Type']/ancestor::tr//td[2]//span[contains(@class, 'mantine-Badge-label')]",

    "details_base_model": ".//p[normalize-space()='Base Model']/ancestor::tr//td[2]//p[not(ancestor::a)]",

    "show_more_btn": ".//button[contains(@class, 'mantine-focus-auto') and contains(@class, 'mantine-Anchor-root')]",
}


error_arr = []



driver = setup_driver()
print("main start ✅")
for URL in URLS:
    itemgetter = 1
    try:
        print(f"processing page {URL} 💡 {itemgetter} of {len(URLS)}")
        check_url(driver, URL)
        wait = WebDriverWait(driver, 100)

        wait.until(EC.presence_of_element_located((By.XPATH, elems["version_container"])))
        version_container = driver.find_element(By.XPATH, elems["version_container"])
        print('version_container found ✅')

        wait.until(EC.presence_of_element_located((By.XPATH, elems["version_btns"])))
        version_btns = version_container.find_elements(By.XPATH, elems["version_btns"])
        print(f'version_btns found ✅ ({len(version_btns)})')

        # Кликнуть на все версии
        for i in range(len(version_btns)):
            # 🔁 Переполучаем список кнопок (чтобы избежать stale)
            wait_for_page_load(driver, wait, (By.XPATH, elems["version_btns"]))
            wait.until(EC.presence_of_element_located((By.XPATH, elems["version_btns"])))
            version_btns = version_container.find_elements(By.XPATH, elems["version_btns"])
            button = version_btns[i]
            print(f"button: {button}")
            version_text = button.text.strip()
            print(f"Clicking version: '{version_text}'")

            wait.until(EC.element_to_be_clickable((By.XPATH, elems["version_btns"])))

            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", button)

            ActionChains(driver).move_to_element(button).click().perform()
            
            # 🔴 Кликаем
            print(f"version '{version_text}' clicked ✅")
            
            # 🔁 Ждём перезагрузки
            wait_for_page_load(driver, wait, (By.XPATH, elems["download_btn"]))

            # ✅ ПОЛНОСТЬЮ ПЕРЕПОЛУЧАЕМ ВСЕ ЭЛЕМЕНТЫ
            all_elems = find_all_elems(driver, elems)
            if not all_elems:
                print(f"❌ Failed to parse version: '{version_text}'")
            print(f"✅ Successfully parsed version: '{version_text}'")

            # ✅ Создаём путь
            download_path = os.path.join(
                "downloads",
                "models",
                sanitize_windows_path(all_elems["details_type"].text),
                sanitize_windows_path(all_elems["details_base_model"].text),
                sanitize_windows_path(all_elems["title"].text),
                sanitize_windows_path(version_text)
            )

            img_path = os.path.join(download_path, "images")
            
            # ✅ Создать папки
            os.makedirs(download_path, exist_ok=True)
            os.makedirs(img_path, exist_ok=True)
            print(f"✅ Download path created: {download_path}")
            print(f"✅ Image path created: {img_path}")

            try:
                show_more_btn = driver.find_element(By.XPATH, elems["show_more_btn"])
                print(f"✅ Show more btn found")
                if show_more_btn.get_attribute("aria-expanded") == "false":
                    show_more_btn.click()
                    print(f"✅ Show more btn clicked")
                    time.sleep(1)
            except Exception as e:
                print(f"❌ Show more btn not found")
                error_arr.append({
                    "error": "❌ Show more btn not found",
                    "url": URL,
                    "itemgetter": itemgetter,
                    "title": all_elems["title"].text,
                    "error_location": "show_more_btn",
                    "version": version_text
                })

            try: 
                desc_file_path = os.path.join(download_path, "description.txt")
                if not os.path.isfile(desc_file_path):
                    desc_elems = all_elems["description_container"].find_elements(By.XPATH, ".//*")
                    desc_text = ""
                    for elem in desc_elems:
                        desc_text += elem.text + "\n" + "\n"
                    with open(desc_file_path, "w", encoding="utf-8") as f:
                        f.write(desc_text)
                    print(f"✅ Description file created: {desc_file_path}")
                else:
                    print(f"⚠️ Skipped: {desc_file_path} already exists")
            except Exception as e:
                error_arr.append({
                    "error": "❌ Description container not found",
                    "url": URL,
                    "itemgetter": itemgetter,
                    "title": all_elems["title"].text,
                    "error_location": "description_container",
                    "version": version_text
                })
                print(f"❌ Description container not found: {e}")
                

            # ✅ Ссылки из описания
            links_file = os.path.join(download_path, "description-links.txt")
            if not os.path.isfile(links_file):
                links = all_elems["description_container"].find_elements(By.TAG_NAME, "a")
                links_output = []
                for link in links:
                    href = link.get_attribute("href")
                    text = link.text.strip()
                    if href and text:
                        links_output.append(f"{href} - {text}")
                    elif href:
                        links_output.append(href)
                with open(links_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(links_output))
                print(f"✅ Links file created: {links_file}")
            else:
                print(f"⚠️ Skipped: {links_file} already exists")

            # ✅ Детали (текст таблицы)
            try:
                details_file = os.path.join(download_path, "details.txt")
                if not os.path.isfile(details_file):
                    details_text = all_elems["details_container"].text
                    with open(details_file, "w", encoding="utf-8") as f:
                        f.write(details_text)
                    print(f"✅ Details file created: {details_file}")
                else:
                    print(f"⚠️ Skipped: {details_file} already exists")
            except Exception as e:
                error_arr.append({
                    "error": "❌ Details container not found",
                    "url": URL,
                    "itemgetter": itemgetter,
                    "title": all_elems["title"].text,
                    "error_location": "details_container",
                    "version": version_text
                })
                print(f"❌ Details container not found: {e}")
                

            # ✅ Скачивание через requests
            try:
                if download_model(all_elems, driver, download_path):
                    print("🎉 Файл успешно скачан!")
                else:
                    print("❌ Не удалось скачать файл.")
            except Exception as e:
                error_arr.append({
                    "error": "❌ Failed to download model",
                    "url": URL,
                    "itemgetter": itemgetter,
                    "title": all_elems["title"].text,
                    "error_location": "download_model",
                    "version": version_text
                })
                print(f"❌ Не удалось скачать файл: {e}")
            
            # ✅ ПОЛНОСТЬЮ ПЕРЕПОЛУЧАЕМ ВСЕ ЭЛЕМЕНТЫ
            all_elems = find_all_elems(driver, elems)
            if not all_elems:
                print(f"❌ Failed to parse version: '{version_text}'")
                error_arr.append({
                    "error": "❌ Failed to parse version",
                    "url": URL,
                    "itemgetter": itemgetter,
                    "title": all_elems["title"].text,
                    "error_location": "image_link",
                    "version": version_text
                })
                print(f"❌ Image link not found: {e}")
            else:
                print(f"✅ Successfully parsed version: '{version_text}'")

            # ✅ КЛИКНУТЬ НА ИЗОБРАЖЕНИЕ
            try:
                all_elems['image_link'].click()
                print(f"✅ Image clicked")
            except Exception as e:
                error_arr.append({
                    "error": "❌ Image link not found",
                    "url": URL,
                    "itemgetter": itemgetter,
                    "title": all_elems["title"].text,
                    "error_location": "image_link",
                    "version": version_text
                })
                print(f"❌ Image link not found: {e}")

            wait_for_page_load(driver, wait, (By.XPATH, ".//div[contains(@class, 'flex flex-col gap-3') and contains(@class, 'mantine-Paper-root')]"))
            print(f"✅ Page loaded")
            try:
                paggination_btns = driver.find_elements(By.XPATH, ".//button[contains(@class, 'mantine-focus-auto h-1 max-w-6 flex-1 rounded border border-solid border-gray-4 bg-white shadow-2xl') and contains(@class, 'mantine-UnstyledButton-root')]")
            except Exception as e:
                error_arr.append({
                    "error": "❌ Pagination btn not found",
                    "url": URL,
                    "itemgetter": itemgetter,
                    "title": all_elems["title"].text,
                    "error_location": "paggination_btns",
                    "version": version_text
                })
                print(f"❌ Pagination btn not found: {e}")

            
            for btn in range(len(paggination_btns)):

                try:
                    print(f"✅ Pagination btn: {btn + 1} clicked  in {len(paggination_btns)} btns")
                    paggination_btns[btn].click()
                    print(f"✅ Pagination btn clicked ✅")
                except Exception as e:
                    error_arr.append({
                        "error": "❌ Pagination btn not found",
                        "url": URL,
                        "itemgetter": itemgetter,
                        "img_iterration": btn + 1,
                        "title": all_elems["title"].text,
                        "error_location": "paggination_btns",
                        "version": version_text
                    })
                    print(f"❌ Pagination btn not found: {e}")

                time.sleep(3)
                wait_for_page_load(driver, wait, (By.XPATH, ".//div[contains(@class, 'flex flex-col gap-3') and contains(@class, 'mantine-Paper-root')]"))
                print(f"✅ Page loaded")

                img_description = driver.find_element(By.XPATH, ".//div[contains(@class, 'flex flex-col gap-3') and contains(@class, 'mantine-Paper-root')]")
                print(f"✅ Image description found")

                try: 
                    data_list = img_description.find_element(By.XPATH, ".//ul[contains(@class, 'flex list-none flex-col')]")
                    data_list_items = data_list.find_elements(By.XPATH, ".//li[contains(@class, 'flex flex-col')]")
                    if(len(data_list_items) > 3):
                        print(f"✅ Data list items len {len(data_list_items)}")
                        list_show_more_btn = img_description.find_element(By.XPATH, ".//div[contains(@class, 'flex flex-col')]//div[contains(@class, 'flex justify-start')]//p[contains(@class, 'mantine-focus-auto cursor-pointer')]")
                        list_show_more_btn.click()
                except Exception as e:
                    print(f"❌ error: {e}")
                    error_arr.append({
                        "error": "❌ Data container not found",
                        "url": URL,
                        "itemgetter": itemgetter,
                        "img_iterration": btn + 1,
                        "title": all_elems["title"].text,
                        "error_location": "data_list",
                        "version": version_text
                    })

                try:
                    prompts_container = img_description.find_elements(By.XPATH, ".//div[contains(@class, 'mantine-focus-auto relative break-words') and contains(@class, 'mantine-Text-root')]")

                    for prompt in prompts_container:
                        if prompt.get_attribute("data-line-clamp") == "true":
                            print(f"✅ Prompt: {prompt}")
                            prompt.find_element(By.XPATH, ".//span[contains(@class, 'absolute') and contains(@class, 'bottom-0') and contains(@class, 'right-0') and contains(@class, 'flex') and contains(@class, 'select-none') and contains(@class, 'items-end')]").click()
                except Exception as e:
                    print(f"❌ error: not found show more btn")

                if not os.path.isfile(os.path.join(img_path, f"img-{btn}.txt")):
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

                    with open(os.path.join(img_path, f"img-{btn}.txt"), "w", encoding="utf-8") as f:
                        f.write("\n".join(description_text_output) + "\n" + "\n".join(img_description_links_output))
                    print(f"✅ Image description file created: {os.path.join(img_path, f'img-{btn}.txt')}")
                else:
                    print(f"⚠️ Skipped: {os.path.join(img_path, f'img-{btn}.txt')} already exists")

                # ✅ ПОЛУЧИТЬ ИЗОБРАЖЕНИЕ
                try:
                    img_container = driver.find_element(By.XPATH, ".//div[contains(@class, 'flex min-h-0 flex-1 items-stretch justify-stretch')]")
                    print(f"✅ Image container found")
                    image = img_container.find_element(By.XPATH, ".//img[contains(@class, 'EdgeImage_image__iH4_q')]")
                    print(f"✅ Image found")
                    time.sleep(10)
                    if download_image(image, driver, img_path, f"img-{btn}"):
                        print("🎉 Изображение успешно скачано!")
                    else:
                        print("❌ Не удалось скачать изображение.")
                except Exception as e:
                    error_arr.append({
                        "error": "❌ Image not found",
                        "url": URL,
                        "itemgetter": itemgetter,
                        "img_iterration": btn + 1,
                        "title": all_elems["title"].text,
                        "error_location": "image",
                        "version": version_text
                    })
                    print(f"❌ Image not found: {e}")
                

            print('All images downloaded ✅')
            print('All images descriptions downloaded ✅')
            print('All images descriptions links downloaded ✅')

            close_btn = driver.find_element(By.XPATH, ".//button[contains(@class, 'mantine-focus-auto mantine-active size-9 rounded-full') and contains(@class, 'mantine-CloseButton-root') and contains(@class, 'mantine-UnstyledButton-root')]")
            close_btn.click()
            print(f"✅ Close btn clicked")
            time.sleep(3)
            wait_for_page_load(driver, wait, (By.XPATH, elems["version_container"]))
            print(f"✅ Page loaded")

            print(f"✅ end {all_elems['title'].text}")
        print(f"page {URL} success ✅ {itemgetter} of {len(URLS)}")
        itemgetter += 1
        
    except Exception as e:
        print(f"error ❌ processing page {URL}: {e}")
        print(f"main end with error ❌ press enter to quit")

if len(error_arr) > 0:
    for arr in error_arr:
        print(f"❌❌❌❌❌❌❌❌❌❌")
        print(f"❌ Error: {arr['error']}")
        print(f"❌ URL: {arr['url']}")
        if 'itemgetter' in arr:
            print(f"❌ Itemgetter: {arr['itemgetter']}")
        if 'title' in arr:
            print(f"❌ Title: {arr['title']}")
        print(f"❌ Error location: {arr['error_location']}")
        if 'img_iterration' in arr:
            print(f"❌ Image iterration: {arr['img_iterration']}")
        if 'version' in arr:
            print(f"❌ Version: {arr['version']}")


