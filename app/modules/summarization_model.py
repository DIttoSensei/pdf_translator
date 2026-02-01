import os
from openai import OpenAI

# 1. We wrap your code in a function so index.py can call it
def run_summarization(text_to_summarize):
    # Initialize the client inside or outside the function
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=os.environ["HF_TOKEN"], # Vercel will provide this
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
                5. Just write the summary, don't add personal text, sign off etc.

                I need you to summarize this text:
                {text_to_summarize}
                """
            }
        ],
    )

    # 2. Instead of writing to a file, we return the result
    summary = completion.choices[0].message.content
    return summary