# download_img.py

from func.set_new_error import set_new_error
from func.wait_page_loaded import wait_page_loaded
from func.find_elems.find_pagination_btns import find_pagination_btns
from func.download.download_page_img import download_page_img
from func.create_files.create_img_desc import create_img_desc
from func.click_close_btn import click_close_btn
from selenium.webdriver.common.by import By
import time


def download_img(driver, pagintaion_path, img_path):
    try:
        wait_page_loaded(driver)
        img_description = driver.find_element(By.XPATH, ".//div[contains(@class, 'flex flex-col gap-3') and contains(@class, 'mantine-Paper-root')]")

        pagination_btns = find_pagination_btns(driver, pagintaion_path)
        if pagination_btns:
            for btn_index in range(len(pagination_btns)):
                pagination_btns[btn_index].click()
                wait_page_loaded(driver)
                time.sleep(5)
                img_description = driver.find_element(By.XPATH, ".//div[contains(@class, 'flex flex-col gap-3') and contains(@class, 'mantine-Paper-root')]")
                create_img_desc(img_path, img_description, btn_index)
                download_page_img(img_path, driver, btn_index)
        else:
            create_img_desc(img_path, img_description, 0)
            download_page_img(img_path, driver, 0)
            
        click_close_btn(driver)


    except Exception as e:
        set_new_error({
            "error_message": f"⚠️ Ошибка при загрузке изображения:",
            "error_data": e,
            "error_type": "download_img",
        })