from imports import *
from utilities import Response, AI, CL_Write

chrome_options = Options()

chrome_options.add_argument('--remote-debugging-pipe')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)

driver.get("https://jobs.lever.co/divergent3d/c14a8e29-d59d-4422-8ac1-72526b0447f2")

driver.find_element(By.CSS_SELECTOR, "a[class*='postings-btn']").click()

questions = driver.find_elements(By.CSS_SELECTOR, ".application-question")
skip = ['name', 'email', 'phone_number', 'location', 'linkedin', 'github']

for q in questions:
    required = False
    try:
        q.find_element(By.CSS_SELECTOR, ".required")
        required = True
    except:
        pass
    if 'awli-application-row' in q.get_attribute('class'):
        continue
    prompt = q.find_element(By.CSS_SELECTOR, ".application-label").text
    if prompt == "Additional information":
        #TODO: add cover letter here
        continue
    print(prompt)
    try:
        prompt = q.find_element(By.CSS_SELECTOR, ".application-label .text").text
    except:
        pass
    response = Response(prompt)
    if response in skip:
        continue
    submission = 0
    if response == "skip":
        if required == True:
            submission = AI(prompt)
        else:
            continue
    else:
        submission = answers[response]
    print(submission)
    try:
        #MC input handler
        #TODO figure out format for AI mc response
        mc = q.find_element(By.CSS_SELECTOR, "ul[data-qa='multiple-choice']")
        choices = q.find_elements(By.CSS_SELECTOR, 'li label')
        for c in choices:
            if c.find_element(By.CSS_SELECTOR, 'span').text == submission:
                c.find_element(By.CSS_SELECTOR, 'input').click()
    except:
        #text/file input handler
        i = q.find_element(By.CSS_SELECTOR, "input")
        if i.get_attribute('type') == 'text':
            i.send_keys(Keys.CONTROL + "a" + Keys.BACK_SPACE)
        i.send_keys(submission)

driver.find_element(By.ID, "btn-submit").click()

time.sleep(100)

driver.quit()
