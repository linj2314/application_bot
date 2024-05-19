from imports import *

keywords = {
    "HDYHAU": ["how did you hear about us?"],
    "first": ["first name"],
    "last": ["last name"],
    "name": ["full name"],
    "address": ["address line"], 
    "city": ["city"],
    "state": ["state"],
    "zip": ["zip", "postal", "code"],
    "email": ["email"],
    "phone_number": ["phone number", "phone"],
    "phone_type": ["phone", "type"],
    "country_code": ["country code"], 
    "phone_extension": ["phone extension"],
    "school": ["school", "university"],
    "degree": ["degree"],
    "major": ["field", "major", "discipline"],
    "GPA": ["gpa"],
    "linkedin": ["linkedin", "linkedin url", "linkedin profile"],
    "website": ["portfolio url", "website url", "website"],
    "resume": ["resume/cv", "resume-allowable-file-types"],
    "cover_letter": ["cover letter", "cover_letter-allowable-file-types"],
    "transcript": ["transcript"],
    "skills": ["skills", "skill", 'add'],
    "us_authorization": ['are you authorized to work in the us?'],
    "sponsorship": ['sponsorship'],
    "pronouns": ['pronouns'],
    'github': ['github url'],
    'twitter': ['twitter', 'twitter url'],
    "location": ['current location'],
    "company": ['current company'],
    "skip_fs": ['other website', 'gender', 'are you hispanic/latino', 'veteran status', 'disability status']
}

def Response(prompt):
    pattern = r'[\'\"?*]'
    prompt = re.sub(pattern, ' ', prompt)
    prompt = prompt.lower()
    prompt = prompt.strip()

    if len(prompt) == 0:
        return "skip"
    
    for word, list in keywords.items():
        for l in list:
            if l == prompt:
                return word
    return "skip"

print(Response("Gender"))