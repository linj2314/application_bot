from imports import *
from utilities import Response, AI, CL_Write

def lever(link):
    chrome_options = uc.ChromeOptions()

    #chrome_options.add_argument('--remote-debugging-pipe')
    #chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")

    driver = uc.Chrome(options=chrome_options)
    driver.implicitly_wait(2)

    driver.get(link)

    driver.find_element(By.CSS_SELECTOR, "a[class*='postings-btn']").click()

    questions = driver.find_elements(By.CSS_SELECTOR, ".application-question")
    skip = ['name', 'email', 'phone_number', 'location', 'linkedin', 'github']

    driver.find_element(By.ID, "resume-upload-input").send_keys(answers["resume"])

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
        try:
            prompt = q.find_element(By.CSS_SELECTOR, ".application-label .text").text
        except:
            pass
        response = Response(prompt)
        if response in skip or response == "skip_fs":
            continue
        submission = 0
        if response == "skip":
            try:
                mc = q.find_element(By.CSS_SELECTOR, "ul[data-qa='multiple-choice']")
                choices = mc.find_elements(By.CSS_SELECTOR, 'li label')
                choices_list = []
                for c in choices:
                    choices_list.append(c.find_element(By.CSS_SELECTOR, 'span').text)
                print(choices_list)
                submission = AI(prompt, choices_list, extras)
            except Exception as e:
                submission = AI(prompt, [], extras)
        else:
            submission = answers[response]
            
        try:
            #MC input handler
            mc = q.find_element(By.CSS_SELECTOR, "ul[data-qa='multiple-choice']")
            choices = q.find_elements(By.CSS_SELECTOR, 'li label')
            found = False
            choices_list = []
            for c in choices:
                choices_list.append(c.find_element(By.CSS_SELECTOR, 'span').text)
                if c.find_element(By.CSS_SELECTOR, 'span').text == submission:
                    c.find_element(By.CSS_SELECTOR, 'input').click()
                    found = True
                    break
            if found == False:
                print("choices list: " + choices_list)
                submission = AI(prompt, choices_list, extras)
                for c in choices:
                    if c.find_element(By.CSS_SELECTOR, 'span').text == submission:
                        c.find_element(By.CSS_SELECTOR, 'input').click()
                        break
        except:
            #text/file input handler
            try:
                i = q.find_element(By.CSS_SELECTOR, "input")
            except:
                i = q.find_element(By.CSS_SELECTOR, "textarea")
            if i.get_attribute('type') == 'text':
                i.send_keys(Keys.CONTROL + "a" + Keys.BACK_SPACE)
            i.send_keys(submission)

    driver.find_element(By.ID, "additional-information").send_keys(CL_Write(company_name, role_name))

    time.sleep(3)

    driver.find_element(By.ID, "btn-submit").click()

    driver.quit()
