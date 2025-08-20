# find_all_elems_on_url_page.py

from func.find_elems.find_title import find_title
from func.find_elems.find_download_btn import find_download_btn
from func.find_elems.find_img import find_img
from func.find_elems.find_details_div import find_details_div
from func.find_elems.find_details_type import find_details_type
from func.find_elems.find_details_base_model import find_details_base_model

def find_all_elems_on_url_page(driver, elems):
    title = find_title(driver, elems["title"])
    download_btn = find_download_btn(driver, elems["download_btn"])
    img = find_img(driver, elems["image_link"])
    details_div = find_details_div(driver, elems["details_container"])
    details_type = find_details_type(driver, elems["details_type"])
    details_base_model = find_details_base_model(driver, elems["details_base_model"])
    return title, download_btn, img, details_div, details_type, details_base_model