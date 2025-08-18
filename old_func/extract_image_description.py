from selenium.webdriver.common.by import By
import re


def extract_image_description(img_description_element):
    """
    Извлекает описание по секциям: Prompt, Negative, Resources, Metadata
    """
    result = []

    # 1. Resources used
    resources = img_description_element.find_elements(By.XPATH, ".//p[contains(text(), 'Resources used')]/following::ul[1]//a")
    if resources:
        result.append("## Resources used")
        for resource in resources:
            name = resource.text.strip()
            link = resource.get_attribute("href")
            # Ищем тип модели (Checkpoint, LoRA и т.д.)
            try:
                badge = resource.find_element(By.XPATH, "./ancestor::li//div[contains(@class, 'mantine-Badge-root')]")
                model_type = badge.text.strip()
            except:
                model_type = "Unknown"
            result.append(f"- {name} ({model_type}) [{link}]")

    # 2. Prompt
    try:
        prompt_title = img_description_element.find_element(By.XPATH, ".//p[contains(text(), 'Prompt')]")
        prompt_text = prompt_title.find_element(By.XPATH, "./following::div[1]").text.strip()
        result.append("## Prompt")
        result.append(prompt_text)
    except:
        pass

    # 3. Negative prompt
    try:
        neg_title = img_description_element.find_element(By.XPATH, ".//p[contains(text(), 'Negative prompt')]")
        neg_text = neg_title.find_element(By.XPATH, "./following::div[1]").text.strip()
        result.append("## Negative Prompt")
        result.append(neg_text)
    except:
        pass

    # 4. Other metadata
    try:
        meta_title = img_description_element.find_element(By.XPATH, ".//p[contains(text(), 'Other metadata')]")
        badges = meta_title.find_elements(By.XPATH, "./following::div[contains(@class, 'mantine-Badge-root')]")
        if badges:
            result.append("## Metadata")
            for badge in badges:
                text = badge.text.strip()
                # Пытаемся разобрать "key: value"
                if ':' in text:
                    key, value = [part.strip() for part in text.split(':', 1)]
                    result.append(f"- {key}: {value}")
                else:
                    result.append(f"- {text}")
    except:
        pass

    return '\n\n'.join(result)