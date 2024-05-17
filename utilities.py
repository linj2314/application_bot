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
    "major": ["field", "major"],
    "GPA": ["gpa"],
    "linkedin": ["linkedin", "linkedin url"],
    "website": ["portfolio url", "website url"],
    "resume": ["resume/cv"],
    "cover_letter": ["cover", "letter"],
    "transcript": ["transcript"],
    "skills": ["skills", "skill", 'add'],
    "us_authorization": ['are you authorized to work in the us?'],
    "sponsorship": ['sponsorship'],
    "pronouns": ['pronouns'],
    'github': ['github url'],
    'twitter': ['twitter', 'twitter url'],
    "location": ['current location'],
    "company": ['current company'],
    "skip_fs": ['other website']
}

providers = [DuckDuckGo, Ecosia, Aichatos, Feedough]
provider_ind = 1

def AI(prompt, choices = [], extras = []):
    global AI_PROMPT
    global provider_ind
    ai_prompt = AI_PROMPT
    client = Client(provider = providers[provider_ind])
    for x in extras:
        ai_prompt += x
    if not choices:
        content = ai_prompt + 'Given this information, how would you fill out this question: ' + '"' + prompt + '". Respond with only the answer and no other words or punctuation.'
    else:
        choices = '; '.join(choices)
        content = ai_prompt + 'Given this information, how would you fill out this question: ' + '"' + prompt + '". These are the possible choices (separated by semicolons) to choose from: ' + choices + '. Respond with only the correct choice and no other words or punctuation.'
    try:
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[{"role": "user", "content": content}]
        )
    except Exception as e:
        if type(e) == RateLimitError:
            provider_ind += 1
            if provider_ind == len(providers):
                provider_ind = 0
            client = Client(provider = providers[provider_ind])
            response = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages=[{"role": "user", "content": content}]
            )
        else:
            print(e)
            exit()

    str = response.choices[0].message.content
    return str

def Response(prompt):
    if prompt.endswith('*'):
        prompt = prompt[:-1]
    
    if prompt.endswith('?'):
        prompt = prompt[:-1]

    prompt = prompt.lower()

    if len(prompt) == 0:
        return "skip"
    
    for word, list in keywords.items():
        for l in list:
            if l == prompt:
                return word
    return "skip"

def CL_Write(company_name, role_name, file = False):
    if not file:
        return CL_1 + company_name + CL_2 + role_name + CL_3 + company_name + CL_4 + company_name + CL_5
    else:
        with open("COVER_LETTER.txt", "w") as f:
            f.write(CL_1 + company_name + CL_2 + role_name + CL_3 + company_name + CL_4 + company_name + CL_5)
