from imports import *
def Response(prompt):
    if prompt.endswith('*'):
        prompt = prompt[:-1]
    
    if prompt.endswith('?'):
        prompt = prompt[:-1]

    prompt = prompt.lower()

    pattern = r'[^a-zA-Z0-9\s]'
    prompt = re.sub(pattern, ' ', prompt)

    return prompt

print(Response("Resume/CV"))