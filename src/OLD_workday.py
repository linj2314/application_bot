from src.imports import *
from src.utilities import Response, AI, CL_Write

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

chrome_options = Options()

chrome_options.add_argument('--remote-debugging-pipe')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)

driver.get("https://autodesk.wd1.myworkdayjobs.com/Ext/job/Montreal-QC-CAN/Software-Developer--Intern--Fall-_24WD78460-2")

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
submitted = []
page = 1
inputs = driver.find_elements(By.XPATH, '//*[starts-with(@id, "input-")]')
resume_uploaded = False
while True:
    if page == 2:
        if resume_uploaded == False:
            try:
                driver.find_element(By.CSS_SELECTOR, '[data-automation-id="file-upload-input-ref"]').send_keys(answers["resume"])
                resume_uploaded = True
            except:
                pass
        try:
            driver.find_element(By.CSS_SELECTOR, '[aria-label="Add Education"]').send_keys(Keys.ENTER)
        except:
            pass
        try:
            driver.find_element(By.CSS_SELECTOR, '[aria-label="Add Websites"]').send_keys(Keys.ENTER)
        except:
            pass

    done = True
    
    for i in inputs:
        try:
            id = i.get_attribute("id")
            if i.get_attribute("aria-haspopup") != "listbox" and i.tag_name != "input" and i.get_attribute("data-uxi-widget-type") != "radioGroup":
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

        try:
            if i.get_attribute("data-uxi-widget-type") == "radioGroup":
                input_type = "mc"
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
            submission = submission.split()
            for s in submission:
                i.send_keys(s)
                time.sleep(2)
                i.send_keys(Keys.ENTER)
                time.sleep(2)
                i.send_keys(Keys.ENTER)
        elif input_type == "mc":
            choices = driver.find_elements(By.CSS_SELECTOR, "#" + id + " label")
            for c in choices:
                t = c.text.lower()
                if t == submission:
                    c.click()
                    break

        #time.sleep(0.1)
        break

    if done:
        driver.find_element(By.CSS_SELECTOR, "[data-automation-id='bottom-navigation-next-button']").click()
        page += 1
        time.sleep(2)

time.sleep(200)
driver.quit()