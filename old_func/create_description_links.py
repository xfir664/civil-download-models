import os

def create_description_links(model_data, folder_path = None):

    if folder_path is None:
        folder_path = f"downloads/models/{model_data['model_type']}/{model_data['model_base_model']}/{model_data['title']}/{model_data['version']}"

    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "description_links.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for link in model_data["description_links"]:
            f.write(f"{link['link']} - {link['text']}\n")
    
    print(f"✅ Description links file created: {file_path}")    
    
    return file_path
