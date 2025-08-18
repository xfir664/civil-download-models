import re
import unicodedata

def sanitize_windows_path(filename):
    """
    Очищает имя файла, оставляя только безопасные символы.
    """
    # 1. Нормализуем Unicode
    filename = unicodedata.normalize('NFKC', filename)
    
    # 2. Оставляем только разрешённые символы: буквы, цифры, пробелы, подчёркивания, скобки (по желанию)
    # Если хочешь убрать ВСЁ, кроме букв/цифр/пробелов:
    sanitized = re.sub(r'[^\w\s\-\(\)\[\]「」《》]', '_', filename)
    
    # 3. Заменяем пробелы и табы на _
    sanitized = re.sub(r'[\s\t]+', '_', sanitized)
    
    # 4. Убираем множественные подчёркивания
    sanitized = re.sub(r'_{2,}', '_', sanitized)
    
    # 5. Убираем _ в начале и конце
    sanitized = sanitized.strip('_')
    
    # 6. Ограничиваем длину
    max_length = 100
    if len(sanitized) > max_length:
        prefix = sanitized[:max_length//2]
        suffix = sanitized[-(max_length//2):]
        sanitized = f"{prefix}_{suffix}"
        sanitized = sanitized[:max_length]
    
    # 7. Защита от пустого имени
    if not sanitized:
        sanitized = "unnamed"
    
    return sanitized