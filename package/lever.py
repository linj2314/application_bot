from package.imports import *
from package.utilities import *

def lever(link):
    chrome_options = uc.ChromeOptions()

    #chrome_options.add_argument('--remote-debugging-pipe')
    #chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")

    driver = uc.Chrome(options=chrome_options)
    driver.implicitly_wait(2)

    driver.get(link)

    time.sleep(1)

    try:
        if driver.find_element(By.TAG_NAME, "h2").text == "Sorry, we couldn't find anything here":
            raise ExpiredApplicationError
    except ExpiredApplicationError:
        raise ExpiredApplicationError
    except:
        pass
        
    driver.find_element(By.CSS_SELECTOR, "a[class*='postings-btn']").click()

    questions = driver.find_elements(By.CSS_SELECTOR, ".application-question")
    skip = ['name', 'email', 'phone_number', 'location', 'linkedin', 'github']

    driver.find_element(By.ID, "resume-upload-input").send_keys(answers["resume"])
    time.sleep(4)

    extras = []
    company_info = driver.title
    company_info = company_info.split(' - ')
    company_name = company_info[0].strip()
    role_name = company_info[1].strip()
    location = driver.find_element(By.CSS_SELECTOR, ".location").text
    location = "This job is located in " + location + ". "
    extras.append(location)

    skips = 6

    for q in questions:
        if skips > 0:
            skips -= 1
            continue
        if 'awli-application-row' in q.get_attribute('class'):
            continue
        try:
            prompt = q.find_element(By.CSS_SELECTOR, ".application-label").text
        except:
            continue

        response = Response(prompt)
        if response in skip or response == "skip_fs":
            continue
        submission = 0

        try:
            #check if text input
            try:
                i = q.find_element(By.CSS_SELECTOR, "input")
            except:
                i = q.find_element(By.CSS_SELECTOR, "textarea")

            if response == "skip":
                submission = AI(prompt, [], extras)
            else:
                submission = answers[response]

            if i.get_attribute('type') == 'text':
                i.send_keys(Keys.CONTROL + "a" + Keys.BACK_SPACE)
            i.send_keys(submission)
        except:
            try:
                #check if mc input
                mc = q.find_element(By.CSS_SELECTOR, "ul[data-qa='multiple-choice']")
                if response == "skip":
                    choices = mc.find_elements(By.CSS_SELECTOR, 'li label')
                    choices_list = []
                    for c in choices:
                        choices_list.append(c.find_element(By.CSS_SELECTOR, 'span').text)
                    submission = AI(prompt, choices_list, extras)
                    for c in choices:
                        if clean_str(c.find_element(By.CSS_SELECTOR, 'span').text) == clean_str(submission):
                            c.find_element(By.CSS_SELECTOR, 'input').click()
                            break
                else:
                    submission = answers[response]
                    found = False
                    for c in choices:
                        if clean_str(c.find_element(By.CSS_SELECTOR, 'span').text) == clean_str(submission):
                            c.find_element(By.CSS_SELECTOR, 'input').click()
                            found = True
                            break
                    if found == False:
                        print("choices list: " + choices_list)
                        submission = AI(prompt, choices_list, extras)
                        for c in choices:
                            if clean_str(c.find_element(By.CSS_SELECTOR, 'span').text) == clean_str(submission):
                                c.find_element(By.CSS_SELECTOR, 'input').click()
                                break
            except:
                try:
                    #check if dropdown input
                    s = Select(q.find_element(By.TAG_NAME, "select"))
                    if response == "skip":
                        choices_list = []
                        for o in s.options:
                            if o.text == "Select ...":
                                continue
                            choices_list.append(o.text)
                        submission = AI(prompt, choices_list, extras)
                        s.select_by_visible_text(submission)
                        continue
                    else:
                        submission = answers[response]
                        ind = 0
                        for o in s.options:
                            if clean_str(o.text) == clean_str(submission):
                                s.select_by_index(ind)
                                break
                            ind += 1
                except:
                    continue

    try:
        driver.find_element(By.ID, "additional-information").send_keys(CL_Write(company_name, role_name))
    except:
        pass

    time.sleep(2)

    driver.find_element(By.ID, "btn-submit").click()

    time.sleep(1)

    try:
        driver.find_element(By.CSS_SELECTOR, "[data-qa='msg-submit-success']")
        driver.quit()
        return 0
    except:
        try:
            driver.find_element(By.CLASS_NAME, "application-already-received")
            driver.quit()
            return 2
        except:
            driver.quit()
            return 1

