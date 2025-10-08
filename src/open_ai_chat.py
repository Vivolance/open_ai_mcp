import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt: str = (
    "You are an expert in Finance specifically in Quantitative Investment and Trading"
)

user_prompt: str = input("What is your question?")

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    model="gpt-4o",
)

response_text: str = chat_completion.choices[0].message.content

print(response_text)
