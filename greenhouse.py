from imports import *
from response import Response

chrome_options = Options()

chrome_options.add_argument('--remote-debugging-pipe')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)

driver.get("https://boards.greenhouse.io/kininsurance/jobs/5170004004#app")

text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']:not([class])")
dropdown_inputs = driver.find_elements(By.CSS_SELECTOR, "div[class='select2-container']")
file_inputs = driver.find_elements(By.CSS_SELECTOR, "button[data-source='attach']")

for t in text_inputs:
    prompt = t.get_attribute('id')
    print(prompt)
    response = Response(prompt)
    if response == 'skip':
        try:
            prompt = t.find_element(By.XPATH, '..').text
            response = Response(prompt)
            if response == 'skip':
                continue
        except:
            pass
    try:
        t.send_keys(answers[response])
    except:
        pass

for d in dropdown_inputs:
    d.click()
    d.find_element(By.XPATH, '..//input').send_keys(Keys.DOWN)
    time.sleep(100)
    '''
    prompt = d.find_element(By.XPATH, '..').text
    submission = answers[Response(prompt)]
    options = d.find_element(By.XPATH, "following-sibling::*[1]").find_elements(By.XPATH, "./*")
    down = 0
    for o in options:
        choice = o.text
        choice = choice.lower
        if o.text == submission:
            break
        down += 1
    d.click()
    for _ in range(down):
        d.send_keys(Keys.DOWN)
    d.send_keys(Keys.ENTER)
    '''

for f in file_inputs:
    prompt = f.get_attribute('aria-describedby')
    response = Response(prompt)
    f.click()
    subprocess.Popen(['xdotool', 'search', '--sync', '--onlyvisible', '--class', 'dialog'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(0.5)
    subprocess.Popen(['xdotool', 'type', answers[response]])
    time.sleep(0.5)
    subprocess.Popen(['xdotool', 'key', 'Return'])
    time.sleep(1)

time.sleep(100)

driver.quit()
