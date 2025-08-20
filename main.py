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

CITE_URL = [

"https://civitai.com/models/962877/dio-brandos-pose-poses?modelVersionId=1078027",
"https://civitai.com/models/926242/soap-censor-concept?modelVersionId=1036773",
"https://civitai.com/models/1018425/incoming-gift-concept?modelVersionId=1141913",
"https://civitai.com/models/1035803/christmas-sweater-clothing?modelVersionId=1161798",
"https://civitai.com/models/1064533/kneeling-upright-sex-from-behind-concept?modelVersionId=1194714",
"https://civitai.com/models/1122064/penis-on-shoulder-concept?modelVersionId=1261116",
"https://civitai.com/models/558342/rin-kagamine-cosplay-clothing?modelVersionId=621541",
"https://civitai.com/models/589523/cum-pool-concept?modelVersionId=658223",
"https://civitai.com/models/1199250/parfait-concept?modelVersionId=1350397",
"https://civitai.com/models/1122062/erection-under-clothes-concept?modelVersionId=1261114",
"https://civitai.com/models/585411/polka-dot-panties-clothing?modelVersionId=653249",
"https://civitai.com/models/778914/negligee-clothing?modelVersionId=871125",
"https://civitai.com/models/828914/x-fingers-concept?modelVersionId=927055",
"https://civitai.com/models/544706/tutu-clothing?modelVersionId=605755",
"https://civitai.com/models/1155298/mating-press-from-above-concept?modelVersionId=1299338",
"https://civitai.com/models/564628/surprise-kiss-concept-commission?modelVersionId=629253",
"https://civitai.com/models/555700/lum-cosplay-clothing?modelVersionId=618473",
"https://civitai.com/models/566162/fellatio-under-mask-concept?modelVersionId=630997",
"https://civitai.com/models/551167/bubble-tea-challenge-concept?modelVersionId=613305",
"https://civitai.com/models/551269/naked-chocolate-clothing?modelVersionId=613413",
"https://civitai.com/models/551328/penis-to-breast-concept?modelVersionId=613481",
"https://civitai.com/models/566164/opening-door-concept?modelVersionId=630999",
"https://civitai.com/models/545251/undone-sarashi-clothing?modelVersionId=606366",
"https://civitai.com/models/923565/lactation-from-behind-concept?modelVersionId=1033791",
"https://civitai.com/models/583498/bikini-pull-clothing?modelVersionId=650989",
"https://civitai.com/models/545258/undressing-concept?modelVersionId=606376",
"https://civitai.com/models/1155653/terrified-noot-noot-concept?modelVersionId=1299726",
"https://civitai.com/models/547666/reverse-upright-straddle-reverse-cowgirl-position-concept?modelVersionId=609174",
"https://civitai.com/models/585214/dimples-of-venus-concept?modelVersionId=653024",
"https://civitai.com/models/585215/dolphin-shorts-clothing?modelVersionId=653025",
"https://civitai.com/models/566160/fellatio-gesture-poses?modelVersionId=630995",
"https://civitai.com/models/843414/clown-clothing?modelVersionId=943559",
"https://civitai.com/models/1138462/snake-wrapped-around-body-concept?modelVersionId=1280272",
"https://civitai.com/models/566037/sitting-on-face-concept?modelVersionId=630853",
"https://civitai.com/models/631420/letterman-jacket-clothing?modelVersionId=705875",
"https://civitai.com/models/1376134/shushing-concept?modelVersionId=1554909",
"https://civitai.com/models/1365557/grabbed-breast-over-shoulder-concept?modelVersionId=1542758",
"https://civitai.com/models/1343951/reaching-overhead-concept?modelVersionId=1517785",
"https://civitai.com/models/1392517/bunny-ears-prank-concept?modelVersionId=1573925",
"https://civitai.com/models/929497/aesthetic-quality-modifiers-masterpiece?modelVersionId=1050644",
"https://civitai.com/models/1805497/glory-wall-concept",
"https://civitai.com/models/1715234/dripping-pussy-juice-from-behind-concept-commission",
"https://civitai.com/models/1256683/disney-animation-illustrious-and-pony?modelVersionId=1416874",
"https://civitai.com/models/661736/s1-dramatic-lighting?modelVersionId=1280045",
"https://civitai.com/models/1059581/incase-gothic-style-mix-or-illustrious?modelVersionId=1189052",
"https://civitai.com/models/1513554/eugene-delacroix-artist-style-illustrious?modelVersionId=1712254",
"https://civitai.com/models/242753/ak-74-by-ct0kk",
"https://civitai.com/models/1566731/draco-ak-pistol-illustrious",
"https://civitai.com/models/1292899/ak-74m-illustrious",
"https://civitai.com/models/1221363/untitled-goose-game-style-illustrious?modelVersionId=1396727",
"https://civitai.com/models/405747/fernando-style-pdxlilxl-or-experimental?modelVersionId=1271352",
"https://civitai.com/models/1514485/ice-immigration-and-customs-enforcement-plate-carrier-with-triple-magazine-placard-loaded-with-magpul-pmags-illustrious?modelVersionId=1713324",
"https://civitai.com/models/1475989/krysdeckerstylev3?modelVersionId=1669481",
"https://civitai.com/models/1494933/lunafreya-nox-fleuret-illustrious?modelVersionId=1691193",
]



def init(url):
    driver = setup_driver()
    check_url(driver, url)
    set_new_error(url)


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

for url in CITE_URL:
    init(url)



if ERRORS_LIST:
    for error in ERRORS_LIST:
        print(f"❌ Ошибки: {error}")

