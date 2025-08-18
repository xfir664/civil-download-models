# create_details_file.py

from func.set_new_error import set_new_error
import os

def create_details_file(path, elem):
    try:
        if not os.path.isfile(path):
            details_text = elem.text + "\n"
            with open(path, "w", encoding="utf-8") as f:
                f.write(details_text)
            print(f"✅ Details file created: {path}")
        else:
            print(f"⚠️ Skipped: {path} already exists")
    except Exception as e:
        set_new_error({
            "error_message": f"⚠️ Ошибка при создании файла details:",
            "error_data": e,
            "error_type": "create_details_file",
        })