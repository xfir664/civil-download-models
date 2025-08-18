import os

def create_description_file(model_data, folder_path = None):

    os.makedirs(folder_path, exist_ok=True)
    
    file_path = os.path.join(folder_path, "description.txt")
    
    description_text = "\n".join(model_data["description_text"])
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(description_text)

    print(f"✅ Description file created: {file_path}")    
    
    return file_path