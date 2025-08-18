from func.check_url import check_url
from func.set_new_error import ERRORS as ERRORS_LIST
from func.sanitize_windows_path import sanitize_windows_path
from setup_driver import setup_driver
from func.wait_page_loaded import wait_page_loaded
from func.find_elems.find_version_div import find_version_div
from func.find_elems.find_version_btns import find_version_btns
from func.find_all_elems_on_url_page import find_all_elems_on_url_page
from func.find_elems.find_description_show_more import find_description_show_more
from func.create_files.create_description_file import create_description_file
from func.create_files.create_details_file import create_details_file
from func.create_files.create_description_links import create_description_links
from func.download.download_model import download_model
from func.download.download_img import download_img
from selenium.webdriver.common.action_chains import ActionChains
import os
import time

URLS = [
    "https://civitai.com/models/1259610/ugly-bastard-faceless-ugly-man-concept?modelVersionId=1420308",
];


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

    "pagination_btns": ".//button[contains(@class, 'mantine-focus-auto h-1 max-w-6 flex-1 rounded border border-solid border-gray-4 bg-white shadow-2xl') and contains(@class, 'mantine-UnstyledButton-root')]",
}

def init(url):
    driver = setup_driver()
    check_url(driver, url)
    version_div = find_version_div(driver, elems["version_container"])
    version_btns = find_version_btns(version_div, elems["version_btns"])
    for btn_index in range(len(version_btns)):
        wait_page_loaded(driver)

        new_version_div = find_version_div(driver, elems["version_container"])
        new_version_btns = find_version_btns(new_version_div, elems["version_btns"])

        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", new_version_btns[btn_index])

        ActionChains(driver).move_to_element(new_version_btns[btn_index]).click().perform()
        wait_page_loaded(driver)

        title, description_div, download_btn, img, details_div, details_type, details_base_model = find_all_elems_on_url_page(driver, elems)

        description_show_more = find_description_show_more(driver, elems["show_more_btn"])
        description_show_more.click()
        time.sleep(3)

        download_path = os.path.join(
            "downloads",
            "models",
            sanitize_windows_path(details_type.text),
            sanitize_windows_path(title.text),
            sanitize_windows_path(details_base_model.text),
            sanitize_windows_path(version_btns[btn_index].text),
        )

        img_path = os.path.join(download_path, "images")

        desc_file_path = os.path.join(download_path, "description.txt")
        details_file_path = os.path.join(download_path, "details.txt")
        desc_links_file_path = os.path.join(download_path, "description_links.txt")

        os.makedirs(download_path, exist_ok=True)
        os.makedirs(img_path, exist_ok=True)

        create_description_file(desc_file_path, description_div)
        create_details_file(details_file_path, details_div)
        create_description_links(desc_links_file_path, description_div)

        download_model(driver, download_btn, download_path)

        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", img)

        img.click()
        wait_page_loaded(driver)

        download_img(driver, elems["pagination_btns"], download_path, img_path)





        
for url in URLS:
    init(url)

if ERRORS_LIST:
    for error in ERRORS_LIST:
        print(f"❌ {error['error_message']}")
        print(f"❌ {error['error_data']}")
        print(f"❌ {error['error_type']}")
else:
    print("✅ Ошибок нет")