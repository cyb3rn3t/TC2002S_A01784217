from openai import OpenAI

#{ "model": "gpt-3.5-turbo", "prompt": "give me a summary of the first shrek movie (2001)", "max_tokens": 100, "temperature": 1 }
secret_key = ""

prompt = "give me a summary of the first shrek movie (2001)"

client = OpenAI(
    api_key = secret_key,
    )

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",  
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=100,
    temperature=1
)

print(completion.choices[0].message.content)