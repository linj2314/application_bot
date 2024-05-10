from imports import *
load_dotenv()

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
    "website": ["website", "url", "portfolio"],
    "resume": ["resume"],
    "cover_letter": ["cover", "letter"],
    "transcript": ["transcript"],
    "skills": ["skills", "skill", 'add'],
    "worked_for": ["worked", "for"],
    "us_authorization": ['authorized', 'us'],
    "sponsorship": ['sponsorship'],
    "pronouns": ['pronouns'],
    "company": ['company']
}

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



    