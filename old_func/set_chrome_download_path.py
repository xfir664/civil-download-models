# set_chrome_download_path.py

import os


def set_chrome_download_path(driver, model_data, folder_path=None):
    """Устанавливает папку загрузок Chrome"""
    # Получаем абсолютный путь
    if folder_path is None:
        folder_path = f"downloads/models/{model_data['model_type']}/{model_data['model_base_model']}/{model_data['title']}/{model_data['version']}"

    abs_folder_path = os.path.abspath(folder_path)
    
    # Настраиваем папку загрузок через Chrome DevTools
    driver.execute_cdp_cmd('Page.setDownloadBehavior', {
        'behavior': 'allow',
        'downloadPath': abs_folder_path
    })
    print(f"✅ Chrome download path set to: {abs_folder_path}")
