from imports import *
from response import Response

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

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
    "phone_extension": "skip",
    "school": os.getenv("SCHOOL"),
    "degree": os.getenv("DEGREE"),
    "major": os.getenv("MAJOR"),
    "GPA": os.getenv("GPA"),
    "from": os.getenv("FROM"),
    "to": os.getenv("TO"),
    "linkedin": os.getenv("LINKEDIN"),
    "website": os.getenv("WEBSITE"),
    "resume": os.getenv("RESUME"),
    "transcript": os.getenv("TRANSCRIPT"),
    "skills": os.getenv("SKILLS").split(),
}

chrome_options = Options()

chrome_options.add_argument('--remote-debugging-pipe')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)

driver.get("https://simonsfoundation.wd1.myworkdayjobs.com/simonsfoundationcareers/job/160-Fifth-Avenue-New-York-NY/Summer-Research-Intern--Assistant--Associate-or-Pre-Doctoral---Polymathic-AI--Building-Foundation-Models-for-Science_R0001598")

driver.find_element(By.CSS_SELECTOR, '[data-uxi-element-id="Apply_adventureButton"]').click()
driver.find_element(By.CSS_SELECTOR, '[data-automation-id="applyManually"]').click()

driver.find_element(By.CSS_SELECTOR, '[data-automation-id="email"]').send_keys(EMAIL)
driver.find_element(By.CSS_SELECTOR, '[data-automation-id="password"]').send_keys(PASSWORD)
time.sleep(0.5)
driver.find_element(By.CSS_SELECTOR, '[data-automation-id="click_filter"]').send_keys(Keys.ENTER)

try:
    driver.find_element(By.CSS_SELECTOR, '[data-automation-id="errorMessage"]')
    driver.find_element(By.CSS_SELECTOR, '[data-automation-id="createAccountLink"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-automation-id="email"]').send_keys(EMAIL)
    driver.find_element(By.CSS_SELECTOR, '[data-automation-id="password"]').send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, '[data-automation-id="verifyPassword"]').send_keys(PASSWORD)
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, '[data-automation-id="click_filter"]').send_keys(Keys.ENTER)
except:
    pass

time.sleep(3)
submitted = []
inputs = driver.find_elements(By.XPATH, '//*[starts-with(@id, "input-")]')
while True:
    try:
        driver.find_element(By.CSS_SELECTOR, '[data-automation-id="file-upload-input-ref"]').send_keys(answers["resume"])
    except:
        pass

    try:
        driver.find_element(By.CSS_SELECTOR, '[aria-label="Add Education"]').click()
    except:
        pass
    try:
        driver.find_element(By.CSS_SELECTOR, '[aria-label="Add Websites"]').click()
    except:
        pass
    done = True
    
    for i in inputs:
        try:
            id = i.get_attribute("id")
            if i.tag_name != "button" and i.tag_name != "input":
                continue
        except:
            inputs = driver.find_elements(By.XPATH, '//*[starts-with(@id, "input-")]')
            done = False
            break
        print(id)
        prompt = ""

        if "dateSectionYear" in id:
            if "from" not in submitted:
                i.send_keys(answers["from"])
                submitted.append("from")
            elif "to" not in submitted:
                i.send_keys(answers["to"])
                submitted.append("to")
            continue

        try:
            label = driver.find_element(By.CSS_SELECTOR, '[for="' + id + '"]')
            prompt = label.text
        except:
            prompt = i.get_attribute("data-automation-id")

        if prompt == "email":
            continue

        response = Response(prompt)

        if response == "skip" or response in submitted:
            continue
        else:
            print(response)
            done = False

        input_type = "text"
        try:
            if i.get_attribute("aria-haspopup") == "listbox":
                input_type = "dropdown"
        except:
            pass

        try:
            if i.get_attribute("data-uxi-widget-type") == "selectinput":
                input_type = "mc_search"
        except:
            pass

        submission = answers[response]
        if submission == "skip":
            submitted.append(response)
            continue
        submitted.append(response)

        if input_type == "text":
            i.send_keys(Keys.CONTROL + "a" + Keys.BACK_SPACE)
            i.send_keys(submission)
        elif input_type == "dropdown":
            if i.text == submission:
                continue
            if response == "phone_type":
                i.send_keys("mo")
                if i.text == "":
                    i.send_keys("h")
            else: 
                i.send_keys(submission)
        elif input_type == "mc_search":
            if type(submission) is list:
                for s in submission:
                    i.send_keys(s)
                    i.send_keys(Keys.RETURN)
                    i.send_keys(Keys.RETURN)
            else:
                i.send_keys(submission)
                i.send_keys(Keys.RETURN)
                i.send_keys(Keys.RETURN)

        #time.sleep(0.1)
        break

    if done:
        driver.find_element(By.CSS_SELECTOR, "[data-automation-id='bottom-navigation-next-button']").click()
        time.sleep(2)

time.sleep(200)
driver.quit()