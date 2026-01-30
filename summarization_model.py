import os
from openai import OpenAI


text = """"""

with open("extracted.txt", 'r') as file:
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
            1. Summarize the text in a concise manner.
            2. Use simple and clear language.
            3. Focus on the main points and key information.
            4. Don't include any personal opinions or interpretations.
            5. Just write the summary, don't add personal text, sign off etc just the summary.

            I need you to summerize this text:
            {text}
"""
            
        }
    ],
)

clean_text = completion.choices[0].message.content
with open("summarized.txt", 'w') as file:
    file.write(clean_text)
    print("Summarized text saved to summarized.txt")