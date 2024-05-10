from imports import *
from response import Response

chrome_options = Options()

chrome_options.add_argument('--remote-debugging-pipe')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)

driver.get("https://jobs.lever.co/divergent3d/c14a8e29-d59d-4422-8ac1-72526b0447f2")

driver.find_element(By.CSS_SELECTOR, "a[class*='postings-btn']").click()

questions = driver.find_elements(By.CSS_SELECTOR, ".application-question")

for q in questions:
    if 'awli-application-row' in q.get_attribute('class'):
        print('hi')
        continue
    prompt = q.find_element(By.CSS_SELECTOR, ".application-label").text
    print(prompt)
    try:
        prompt = q.find_element(By.CSS_SELECTOR, ".application-label .text").text
    except:
        pass
    submission = answers[Response(prompt)]
    try:
        mc = q.find_element(By.CSS_SELECTOR, "ul[data-qa='multiple-choice']")
        choices = q.find_elements(By.CSS_SELECTOR, 'li label')
        for c in choices:
            if c.find_element(By.CSS_SELECTOR, 'span').text == submission:
                c.find_element(By.CSS_SELECTOR, 'input').click()
    except:
        q.find_element(By.CSS_SELECTOR, "input").send_keys(submission)

time.sleep(100)

driver.quit()
