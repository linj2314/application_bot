from imports import *
load_dotenv()

keywords = {
    "HDYHAU": ["hear", "about", "us"],
    "first": ["first"],
    "last": ["last"],
    "name": ["full", "name"],
    "address": ["address"], 
    "city": ["city"],
    "state": ["state"],
    "zip": ["zip", "postal", "code"],
    "email": ["email"],
    "phone_type": ["phone", "type"],
    "country_code": ["country", "code"], 
    "phone_number": ["phone", "number"],
    "phone_extension": ["phone", "extension"],
}

answers = {
    "HDYHAU": "I",
    "first": os.getenv("FIRST"),
    "last": os.getenv("LAST"),
    "name": os.getenv("NAME"),
    "address": os.getenv("ADDRESS"), 
    "city": os.getenv("CITY"),
    "state": os.getenv("STATE"),
    "zip": os.getenv("ZIP"),
    "email": os.getenv("EMAIL"),
    "phone_type": os.getenv("PHONE_TYPE"),
    "country_code": os.getenv("COUNTRY_CODE"), 
    "phone_number": os.getenv("PHONE_NUMBER"),
    "phone_extension": "skip"
}

def Response(prompt):
    if prompt.endswith('*'):
        prompt = prompt[:-1]

    if prompt.endswith('?'):
        prompt = prompt[:-1]

    prompt = prompt.lower()
    words = prompt.split()

    ret = "skip"
    best = 0
    for key, value in keywords.items():
        score = 0
        for word in words:
            if word in value:
                score += 1
        score = score / len(value)
        if (score > best):
            ret = key
            best = score
    return answers[ret]



    