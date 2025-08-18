# get_all_pages.py
from func.check_url import check_url
from func.get_versions_links import get_versions_links
import time

def get_all_pages(driver, urls):
    """Собирает все страницы для обработки из списка URL и версий"""
    all_pages = []
    for url in urls:
        try:
            # Добавляем проверку на существование страницы
            check_url(driver, url)
            # Получаем версии и добавляем их в список
            versions = get_versions_links(driver, "versions")
            all_pages.extend([{"link": v["link"], "text": v["text"]} for v in versions])
            
            print(f"✅ Page {url} processed successfully")
        except Exception as e:
            print(f"❌ Error processing URL {url}: {e}")
            continue
    
    return all_pages
