from func.check_url import check_url
from func.set_new_error import ERRORS as ERRORS_LIST, set_new_error
from func.sanitize_windows_path import sanitize_windows_path
from setup_driver import setup_driver
from func.wait_page_loaded import wait_page_loaded
from func.find_elems.find_version_div import find_version_div
from func.find_elems.find_version_btns import find_version_btns
from func.find_all_elems_on_url_page import find_all_elems_on_url_page
from func.create_files.create_details_file import create_details_file
from func.download.download_model import download_model
from func.download.download_img import download_img
from func.create_files.create_img_desc import create_img_desc
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.webdriver.common.by import By

elems = {
    "title": "//h1[contains(@class, 'mantine-Title-root')]",

    "version_container": "//div[contains(@class, 'mantine-Group-root') and contains(@style, '--group-justify: flex-start')]",

    "version_btns": "//button[contains(@class, 'mantine-Button-root') and @data-variant='filled' and @data-size='compact-sm']",

    "details_container": "//div[contains(@class, 'mantine-Accordion-item') and @data-active='true']",

    "image_link": "(//div[contains(@class, 'ModelVersionDetails_mainSection__46plL')]//a[.//img[contains(@class, 'EdgeImage_image__iH4_q')]])",

    "download_btn": "//a[@data-tour='model:download']",

    "details_type": ".//p[normalize-space()='Type']/ancestor::tr//td[2]//span[contains(@class, 'mantine-Badge-label')]",

    "details_base_model": ".//p[normalize-space()='Base Model']/ancestor::tr//td[2]//p[not(ancestor::a)]",

    "pagination_btns": ".//button[contains(@class, 'mantine-focus-auto h-1 max-w-6 flex-1 rounded border border-solid border-gray-4 bg-white shadow-2xl') and contains(@class, 'mantine-UnstyledButton-root')]",
}

CITE_URL = "https://civitai.com/models/1467600/presenting-removed-panties-concept?modelVersionId=1659859"



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

        title, download_btn, img, details_div, details_type, details_base_model = find_all_elems_on_url_page(driver, elems)

        download_path = os.path.join(
            "downloads",
            "models",
            sanitize_windows_path(details_type.text),
            sanitize_windows_path(title.text),
            sanitize_windows_path(details_base_model.text),
            sanitize_windows_path(version_btns[btn_index].text),
        )

        img_path = os.path.join(download_path, "images")

        details_file_path = os.path.join(download_path, "details.txt")

        os.makedirs(download_path, exist_ok=True)
        os.makedirs(img_path, exist_ok=True)

        create_details_file(details_file_path, details_div)

        download_model(driver, download_btn, download_path)

        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", img)

        img.click()
        wait_page_loaded(driver)

        download_img(driver, elems["pagination_btns"], img_path)
        
    driver.quit()

init(CITE_URL)

if ERRORS_LIST:
    print(f"❌ Ошибки: {CITE_URL}")
    for error in ERRORS_LIST:
        print(f"❌ Ошибки: {error}")

