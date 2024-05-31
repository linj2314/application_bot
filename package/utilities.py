from package.imports import *

keywords = {
    "HDYHAU": ["how did you hear about us"],
    "first": ["first name"],
    "last": ["last name"],
    "name": ["full name"],
    "address": ["address line", "address line 1"], 
    "city": ["city"],
    "state": ["state"],
    "country": ["country"],
    "zip": ["zip", "postal code"],
    "email": ["email"],
    "phone_number": ["phone number", "phone"],
    "phone_type": ["phone device type"],
    "country_code": ["country phone code"], 
    "school": ["school", "university", "school or university"],
    "degree": ["degree"],
    "major": ["field of study", "major", "discipline"],
    "GPA": ["overall result (gpa)", "gpa"],
    "linkedin": ["linkedin", "linkedin url", "linkedin profile"],
    "website": ["portfolio url", "website url", "website", "other website"],
    "resume": ["resume/cv", "resume-allowable-file-types"],
    "cover_letter": ["cover letter", "cover_letter-allowable-file-types"],
    "transcript": ["transcript"],
    "skills": ["type to add skills"],
    "us_authorization": ['are you authorized to work in the us?'],
    "sponsorship": ['sponsorship'],
    "pronouns": ['pronouns'],
    'github': ['github url'],
    'twitter': ['twitter', 'twitter url'],
    "location": ['current location'],
    "company": ['current company'],
    "start_year": ['from'],
    "end_year": ['to', 'to (actual or expected)'],
    "race": ['what is your race/ethnicity'],
    "gender": ['what is your gender'],
    "country": ['county'],
    "skip_fs": ['other website', 'gender', 'are you hispanic/latino', 'veteran status', 'disability status', 'phone extension', 'i have a preferred name', 'race']
}

providers = [DuckDuckGo, Ecosia, Aichatos, Feedough]
provider_ind = 0

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
    if not prompt:
        return "skip_fs"
    
    prompt = prompt.split('\n')[0]
    prompt = clean_str(prompt)

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
        f.close()

def clean_str(str):
    pattern = r'[\'\"?*]'
    str = re.sub(pattern, ' ', str)
    return str.lower().strip()

def scrape_links():
    f1 = open(os.getenv("PROJECT_PATH") + "raw.txt", "r")
    f2 = open(os.getenv("PROJECT_PATH") + "links.txt", "w")
    str = f1.read()
    str = re.sub('"', "'", str)
    pattern = r'<a.*?>'
    tags = re.findall(pattern, str, re.DOTALL)

    save = False
    curr = ""
    arr = []
    for t in tags:
        lines = t.splitlines()
        for l in lines:
            if l.endswith("="):
                l = l[:-1]
            for c in l:
                if c == "'":
                    if save:
                        arr.append(curr)
                        save = False
                        curr = ""
                    else:
                        save = True
                else:
                    if save:
                        curr += c

    arr = arr[:-2]

    i = 1
    while i < len(arr):
        f2.write(arr[i] + '\n')
        i += 2

    f1.close()
    f2.close()
