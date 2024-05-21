from imports import *
from utilities import *

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

chrome_options = Options()

chrome_options.add_argument('--remote-debugging-pipe')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)

driver.get("https://valeo.wd3.myworkdayjobs.com/valeo_jobs/job/Greensburg-IN/IT-Trainee_REQ2024039634")

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
    try:
        driver.find_element(By.CSS_SELECTOR, '[data-automation-id="createAccountCheckbox"]').click()
    except:
        pass
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, '[data-automation-id="click_filter"]').send_keys(Keys.ENTER)
except:
    pass

time.sleep(3)

while True:
    try:
        country_input = driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='countryDropdown']")
        if country_input.text != answers["country"]:
            country_input.send_keys(answers["country"])
            time.sleep(3)
    except:
        pass
    
    inputs = driver.find_elements(By.XPATH, '//*[starts-with(@id, "input-")]')
    for i in inputs:
        try:
            label = driver.find_element(By.CSS_SELECTOR, '[for="' + i.get_attribute("id") + '"]')
            prompt = label.text
        except:
            try:
                prompt = i.get_attribute("data-automation-id")
            except:
                continue

        response = Response(prompt)
        if response in ["skip_fs", "country", "email"]:
            continue

        if i.get_attribute("aria-haspopup") == "listbox":
            if response == "skip":
                submission = AI(prompt)
            else:
                submission = answers[response]
            if i.text == submission:
                continue
            i.send_keys(submission)
        elif i.get_attribute("data-uxi-widget-type") == "selectinput":
            submission = answers[response]
            submission = submission.split(',')
            for s in submission:
                i.send_keys(s)
                i.send_keys(Keys.ENTER)
                try:
                    driver.find_element(By.CSS_SELECTOR, "div[data-automation-id='activeListContainer'] div div").find_element(By.CSS_SELECTOR, "input").click()
                except:
                    pass
        elif i.get_attribute("data-uxi-widget-type") == "radioGroup":
            choices = i.find_elements(By.CSS_SELECTOR, "label")
            choices_list = []
            for c in choices:
                t = clean_str(c.text)
                choices_list.append(t)
            if response == "skip":
                submission = AI(prompt, choices_list)
            else:
                submission = answers[response]
            for c in choices:
                if clean_str(c.text) == clean_str(submission):
                    driver.find_element(By.CSS_SELECTOR, "body").click()
                    c.click()
                    break
        else:
            if response == "skip":
                submission = AI(prompt)
            else:
                submission = answers[response]
            i.send_keys(submission)
    time.sleep(1000)
    break
    driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='bottom-navigation-next-button']")

