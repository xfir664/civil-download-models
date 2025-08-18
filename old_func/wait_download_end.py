# wait_download_end.py

import os
import time

def wait_download_end(folder_path, timeout=300, stable_check_interval=1.0):
    """
    Ожидает завершения скачивания в указанной папке.
    
    :param folder_path: Путь к папке загрузки
    :param timeout: Максимальное время ожидания (сек)
    :param stable_check_interval: Время между проверками стабильности размера
    :return: True, если скачивание завершено, иначе False
    """
    print(f"🔄 Waiting for download to complete in: {folder_path}")
    start_time = time.time()

    # Начальный список файлов
    initial_files = set(os.listdir(folder_path)) if os.path.exists(folder_path) else set()

    # Проверка: может, файлы уже есть?
    if os.path.exists(folder_path):
        current_files = set(os.listdir(folder_path))
        stable_files = [
            f for f in current_files
            if not f.endswith(('.crdownload', '.tmp', '.part')) and os.path.isfile(os.path.join(folder_path, f))
        ]
        if stable_files:
            valid_files = [
                f for f in stable_files
                if os.path.getsize(os.path.join(folder_path, f)) > 0
            ]
            if valid_files:
                print(f"✅ Files already downloaded: {valid_files}")
                return True

    while (time.time() - start_time) < timeout:
        if not os.path.exists(folder_path):
            time.sleep(0.5)
            continue

        current_files = set(os.listdir(folder_path))
        new_files = current_files - initial_files

        if new_files:
            # Проверяем наличие .crdownload
            crdownload_files = [f for f in current_files if f.endswith('.crdownload')]
            if not crdownload_files:
                # Проверяем, что файлы не пустые и размер стабилен
                file_sizes = {}
                for file in new_files:
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path):
                        file_sizes[file] = os.path.getsize(file_path)

                # Если все файлы пустые — возможно, ошибка
                if all(size == 0 for size in file_sizes.values()):
                    time.sleep(0.5)
                    continue

                # Ждём и проверяем стабильность
                time.sleep(stable_check_interval)

                stable = True
                for file in new_files:
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path):
                        current_size = os.path.getsize(file_path)
                        if current_size != file_sizes.get(file, -1):
                            stable = False
                            break

                if stable:
                    downloaded_files = list(new_files)
                    print(f"✅ Download completed! Files: {downloaded_files}")
                    return True
            else:
                print(f"🔄 Download in progress... ({len(crdownload_files)} .crdownload files)")

        time.sleep(0.5)  # Не перегружаем CPU

    print(f"⏰ Timeout reached ({timeout}s). Download might still be in progress.")
    return False