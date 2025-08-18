# create_model_folder.py
import os
from func.sanitize_windows_path import sanitize_windows_path

def create_model_folder(model_data, download_dir=None):
    """
    Создает структуру папок для модели
    
    Args:
        model_data (dict): Словарь с данными модели (title, model_type, model_base_model)
        download_dir (str): Путь к папке для хранения моделей (по умолчанию: проект/downloads/models)
    """
    # Если не задано - ищем папку проекта (без func/)
    if download_dir is None:
        # Получаем путь к текущему файлу (create_model_folder.py)
        current_file_path = os.path.abspath(__file__)
        # Берем родительскую папку от текущего файла (чтобы попасть в project/)
        project_dir = os.path.dirname(os.path.dirname(current_file_path))
        # Создаем путь к downloads/models
        download_dir = os.path.join(project_dir, "downloads", "models")
    
    # Убедимся, что папка существует
    os.makedirs(download_dir, exist_ok=True)
    
    # Создаем структуру папок
    model_path = os.path.join(
        download_dir,
        model_data["model_type"],
        model_data["model_base_model"],
        model_data["title"],
        model_data["version"]
    )
    
    os.makedirs(model_path, exist_ok=True)
    
    print(f"✅ Created model folder: {model_path}")
    return model_path
