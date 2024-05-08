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
    "phone_type": ["phone", "type"],
    "country_code": ["country", "code"], 
    "phone_number": ["phone", "number"],
    "phone_extension": ["phone", "extension"],
    "school": ["school", "university"],
    "degree": ["degree"],
    "major": ["field", "major"],
    "GPA": ["gpa"],
    "from": ["from"],
    "to": ["to"],
    "linkedin": ["linkedin"],
    "website": ["website", "url"],
    "resume": ["resume"],
    "transcript": ["transcript"],
    "cover_letter": ["cover", "letter"],
    "skills": ["skills", "skill", 'add'],
    "worked_for": ["worked", "for"]
}

prompt = 'resume-allowable-file-types'

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

print(words)

ret = "skip"
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

print(ret)

