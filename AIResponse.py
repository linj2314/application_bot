from imports import *
load_dotenv()
AI_PROMPT = os.getenv("AI_PROMPT")

def AI(prompt, type):
    client = Client(provider = DuckDuckGo)

    content = AI_PROMPT + '"' + prompt + '"Respond with only the answer and no other words.'
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}]
    )
    str = response.choices[0].message.content
    str = str.lower
    pattern = r'[^a-zA-Z0-9\s]'
    str = re.sub(pattern, ' ', str)
    return str