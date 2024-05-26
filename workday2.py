from imports import *
from utilities import *

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

chrome_options = Options()

chrome_options.add_argument('--remote-debugging-pipe')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)

driver.get("https://gen.wd1.myworkdayjobs.com/careers/job/CZE---Prague/Product-Design-Summer-Internship_53121")

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

page = 1
year = False

#driver.execute_script("document.body.style.zoom='25%'")

while True:
    if page == 1:
        try:
            country_input = driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='countryDropdown']")
            if country_input.text != answers["country"]:
                country_input.click()
                choices = driver.find_element(By.CSS_SELECTOR, 'div[class*="wd-popup"]').find_elements(By.CSS_SELECTOR, "ul li")
                for c in choices:
                    if c.text == answers["country"]:
                        c.click()
                        time.sleep(3)
                        break
        except:
            pass
    elif page == 2:
        try:
            driver.find_element(By.CSS_SELECTOR, "input[data-automation-id='jobTitle']")
        except:
            pass
        else:
            try:
                driver.find_element(By.CSS_SELECTOR, "button[aria-label='Delete Work Experience 1']").click()
                print("delete button clicked")
            except:
                print("Application required job experience; could not be completed")
                exit()

        try:
            driver.find_element(By.CSS_SELECTOR, "input[data-automation-id='school']")
        except:
            driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Add Education"]').send_keys(Keys.ENTER)
            time.sleep(1)

    if page > 2:
        try:
            driver.find_element(By.CSS_SELECTOR, 'div[data-automation-id="reviewJobApplicationPage"]')
            driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='bottom-navigation-next-button']").click()
            break
        except:
            pass

    
    inputs = driver.find_elements(By.XPATH, '//*[starts-with(@id, "input-")]')
    for i in inputs:
        try:
            _ = i.get_attribute("id")
        except StaleElementReferenceException:
            continue

        if page == 2:
            if i.get_attribute("data-automation-id") == "select-files":
                driver.find_element(By.CSS_SELECTOR, "input[data-automation-id='file-upload-input-ref']").send_keys(answers["resume"])
                continue
            if i.get_attribute('data-automation-id') == 'dateInputWrapper' or 'display' in i.get_attribute("id"):
                continue
            if 'dateSectionYear-input' in i.get_attribute("id"):
                if not year:
                    i.send_keys(answers["start_year"])
                    year = True
                    continue
                else:
                    i.send_keys(answers["end_year"])
                    continue
        
        if page > 2:
            if i.get_attribute("data-automation-id") == "agreementCheckbox":
                driver.find_element(By.CSS_SELECTOR, "label[for='" + i.get_attribute("id") + "']").click()
                continue
            if i.get_attribute("aria-label") == "Day":
                i.send_keys(datetime.today().strftime('%d'))
                continue
            elif i.get_attribute("aria-label") == "Month":
                i.send_keys(datetime.today().strftime('%m'))
                continue
            elif i.get_attribute("aria-label") == "Year":
                i.send_keys(datetime.today().strftime('%Y'))
                continue

        try:
            label = driver.find_element(By.CSS_SELECTOR, '[for="' + i.get_attribute("id") + '"]')
            prompt = label.text
        except:
            try:
                prompt = i.get_attribute("data-automation-id")
            except:
                continue

        print(prompt)

        response = Response(prompt)
        if response in ["skip_fs", "country", "email"]:
            continue

        if i.get_attribute("aria-haspopup") == "listbox":
            if response == "phone_type":
                print("in phone type")
                i.send_keys(answers[response])
                time.sleep(1)
                if clean_str(i.text) != answers[response]:
                    i.send_keys("home")
                time.sleep(1)
                if clean_str(i.text) != "home":
                    i.send_keys("cell")
                continue    
            if response == "skip":
                i.send_keys(Keys.ENTER)
                choices = driver.find_element(By.CSS_SELECTOR, 'div[class*="wd-popup"]').find_elements(By.CSS_SELECTOR, "ul li")
                choices = choices[1:]
                choices_list = []
                for c in choices:
                    choices_list.append(c.text)
                i.click()
                i.click()
                time.sleep(0.25)
                submission = AI(prompt, choices_list)
            else:
                submission = answers[response]
            if i.text == submission:
                continue
            i.send_keys(submission)
            try:
                options = driver.find_element(By.CSS_SELECTOR, 'div[class*="wd-popup"]').find_elements(By.CSS_SELECTOR, "ul li")
                for o in options:
                    print(o.value_of_css_property('background-color'))
                    if o.value_of_css_property('background-color') == 'rgba(8, 117, 225, 1)':
                        o.click()
                        break
            except Exception as e:
                pass
        elif i.get_attribute("data-uxi-widget-type") == "selectinput":
            if response == "HDYHAU":
                i.send_keys("other")
                i.send_keys(Keys.ENTER)
                try:
                    driver.find_element(By.CSS_SELECTOR, "div[data-automation-id='activeListContainer'] div div").find_element(By.CSS_SELECTOR, "input").click()
                except:
                    pass
                try:
                    driver.find_element(By.CSS_SELECTOR, "div[data-automation-id='formField-sourcePrompt']").find_element(By.CSS_SELECTOR, "div[data-automation-id='DELETE_charm']")
                    driver.find_element(By.TAG_NAME, "body").click()
                except:
                    i.clear()
                    i.send_keys("linkedin")
                    i.send_keys(Keys.ENTER)
                    try:
                        driver.find_element(By.CSS_SELECTOR, "div[data-automation-id='activeListContainer'] div div").find_element(By.CSS_SELECTOR, "input").click()
                    except:
                        pass
                continue
            submission = answers[response]
            submission = submission.split(',')
            for s in submission:
                i.send_keys(s)
                i.send_keys(Keys.ENTER)
                try:
                    driver.find_element(By.CSS_SELECTOR, "div[data-automation-id='activeListContainer'] div div").find_element(By.CSS_SELECTOR, "input").click()
                except:
                    pass
            time.sleep(0.5)
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
        elif i.tag_name == 'fieldset':
            #TODO implement fieldset handling (multiple choice but different format)
            print("fieldset encountered")
            exit()
        else:
            if response == "skip":
                submission = AI(prompt)
            else:
                submission = answers[response]
            try:
                i.send_keys(Keys.CONTROL + "a" + Keys.BACK_SPACE)
                i.send_keys(submission)
            except ElementNotInteractableException:
                pass
    
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='bottom-navigation-next-button']").click()
    time.sleep(3)
    page += 1

time.sleep(10)