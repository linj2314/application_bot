from imports import *

keywords = {
    "HDYHAU": ["hear", "about", "us"],
    "first": ["first"],
    "last": ["last"],
    "name": ["full", "name"],
    "address": ["address", "line"], 
    "city": ["city"],
    "state": ["state"],
    "zip": ["zip", "postal", "code"],
    "email": ["email"],
    "phone_number": ["phone", "number"],
    "phone_type": ["phone", "type"],
    "country_code": ["country", "code"], 
    "phone_extension": ["phone", "extension"],
    "school": ["school", "university"],
    "degree": ["degree"],
    "major": ["field", "major"],
    "GPA": ["gpa"],
    "from": ["from"],
    "to": ["to"],
    "linkedin": ["linkedin"],
    "website": ["website", "portfolio"],
    "resume": ["resume"],
    "cover_letter": ["cover", "letter"],
    "transcript": ["transcript"],
    "skills": ["skills", "skill", 'add'],
    "worked_for": ["worked", "for"],
    "us_authorization": ['authorized', 'us'],
    "sponsorship": ['sponsorship'],
    "pronouns": ['pronouns'],
    "location": ['location'],
    "company": ['company'],
    'github': ['github']
}

def AI(prompt, choices = []):
    client = Client(provider = DuckDuckGo)
    if not choices:
        content = AI_PROMPT + '"' + prompt + '". Respond with only the answer and no other words or punctuation.'
    else:
        choices = '; '.join(choices)
        content = AI_PROMPT + '"' + prompt + '". These are the possible choices (separated by semicolons) to choose from: ' + choices + '. Respond with only the correct choice and no other words or punctuation.'
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}]
    )
    str = response.choices[0].message.content
    str = str.lower()
    return str

def Response(prompt):
    try:
        if prompt.endswith('*'):
            prompt = prompt[:-1]
    except:
        pass
    
    try:
        if prompt.endswith('?'):
            prompt = prompt[:-1]
    except:
        pass

    prompt = prompt.lower()

    pattern = r'[^a-zA-Z0-9\s]'
    prompt = re.sub(pattern, ' ', prompt)

    words = prompt.split()

    ret = "skip"
    if len(words) == 0:
        return "skip"
    best = 0
    for key, value in keywords.items():
        score = 0
        for word in words:
            if word in value:
                score += 1
        score = score / len(words)
        if (score > best):
            ret = key
            best = score
    return ret

def CL_Write(company_name, role_name, file = False):
    if not file:
        return CL_1 + company_name + CL_2 + role_name + CL_3 + company_name + CL_4 + company_name + CL_5
    else:
        with open("COVER_LETTER.txt", "w") as f:
            f.write(CL_1 + company_name + CL_2 + role_name + CL_3 + company_name + CL_4 + company_name + CL_5)
