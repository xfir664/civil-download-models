# create_details_text.py

import os

def create_details_text(model_data, folder_path = None):
    if folder_path is None:
        folder_path = f"downloads/models/{model_data['model_type']}/{model_data['model_base_model']}/{model_data['title']}/{model_data['version']}"

    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "details.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(model_data["details_text"])

    print(f"✅ Details text file created: {file_path}")

    return file_path