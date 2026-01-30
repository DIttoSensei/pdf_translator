import os
from openai import OpenAI


text = """"""
with open("summarized.txt", 'r') as file:
    text = file.read()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

completion = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct:novita",
    messages=[
        {
            "role": "user",
            "content": f"""
            STRICT RULES:
            1. Translate the text accurately to Nigerian Pidgin English.
            2. Don't add personal thought only write the translation.
            3. No personal opinion write off or questions just translated text.
            4. Make sure translation is pure Nigerian Pidgin English.
            
            I need you to translate this text to Nigerian Pidgin English:
            {text}
            """
        }
    ],
)

clean_text = completion.choices[0].message.content


with open("translated.txt", 'w') as file:
    file.write(clean_text)  
    print("Translated text saved to translated.txt")