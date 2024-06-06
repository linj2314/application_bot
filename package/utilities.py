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
    "transcript": ["transcript", "transcript upload"],
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

def AI2(prompt, choices = [], extras = []):
    global AI_PROMPT
    ai_prompt = AI_PROMPT
    for x in extras:
        ai_prompt += x
    if not choices:
        content = ai_prompt + 'Given this information, how would you fill out this question: ' + '"' + prompt + '". Respond with only the answer and no other words or punctuation.'
    else:
        choices = '; '.join(choices)
        content = ai_prompt + 'Given this information, how would you fill out this question: ' + '"' + prompt + '". These are the possible choices (separated by semicolons) to choose from: ' + choices + '. Respond with only the correct choice and no other words or punctuation.'
    try:
        response = gpt(content)
    except Exception as e:
        print(e)
        exit()

    return response

def AI(prompt, choices = [], extras = []):
    client = Client(You)
    global AI_PROMPT
    ai_prompt = AI_PROMPT
    for x in extras:
        ai_prompt += x
    if not choices:
        content = ai_prompt + 'Given this information, how would you fill out this question: ' + '"' + prompt + '". Respond with only the answer and no other words or punctuation.'
    else:
        choices = '; '.join(choices)
        content = ai_prompt + 'Given this information, how would you fill out this question: ' + '"' + prompt + '". These are the possible choices (separated by semicolons) to choose from: ' + choices + '. Respond with only the correct choice and no other words or punctuation.'
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": content}]
        )
    except Exception as e:
        print(e)
        exit()
    return(response.choices[0].message.content)

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

def gpt(content):
    def get_shadow_root(element):
        return driver.execute_script('return arguments[0].shadowRoot', element)

    chrome_options = Options()

    chrome_options.add_argument('--remote-debugging-pipe')
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(2)

    driver.get("https://bing.com/chat")

    sd = driver.find_element(By.CSS_SELECTOR, "cib-serp")
    sd2 = get_shadow_root(sd).find_element(By.CSS_SELECTOR, "cib-action-bar")
    sd3 = get_shadow_root(sd2).find_element(By.CSS_SELECTOR, "cib-text-input")
    sd4 = get_shadow_root(sd3).find_element(By.ID, "searchbox")

    content = re.sub('\n', '', content)
    sd4.send_keys(content + "\n")

    sd3 = get_shadow_root(sd2).find_element(By.CSS_SELECTOR, "cib-typing-indicator")
    sd4 = get_shadow_root(sd3).find_element(By.CSS_SELECTOR, "span")

    while True:
        if sd4.text == "Response stopped":
            break
        time.sleep(0.5)

    sd2 = get_shadow_root(sd).find_element(By.CSS_SELECTOR, "cib-conversation")
    sd3 = get_shadow_root(sd2).find_element(By.CSS_SELECTOR, "cib-chat-turn")
    sd4 = get_shadow_root(sd3).find_element(By.CSS_SELECTOR, "cib-message-group:nth-of-type(2)")
    sd5 = get_shadow_root(sd4).find_element(By.CSS_SELECTOR, "cib-message")
    sd6 = get_shadow_root(sd5).find_element(By.CSS_SELECTOR, "cib-shared")

    main_element = sd6.find_element(By.CSS_SELECTOR, ".ac-textBlock")

    driver.execute_script("arguments[0].querySelectorAll('sup').forEach(function(el) { el.style.display = 'none'; });", main_element)
    response = main_element.text

    driver.quit()

    return response
