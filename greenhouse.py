from imports import *

chrome_options = Options()

chrome_options.add_argument('--remote-debugging-pipe')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)

driver.get("https://boards.greenhouse.io/kininsurance/jobs/5170004004#app")

text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']:not([class])")
dropdown_inputs = driver.find_elements(By.CSS_SELECTOR, "div[class='select2-container']")
file_inputs = driver.find_elements(By.CSS_SELECTOR, "button[data-source='attach']")
required_checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox'][aria-required='true']")

for t in text_inputs:
    prompt = t.find_element(By.XPATH, '..').text
    required = False
    try:
        t.find_element(By.XPATH, '..').find_element(By.CSS_SELECTOR, '.asterisk')
        required = True
    except:
        pass
    print(prompt)
    response = Response(prompt)
    if response == 'skip':
        if required == True:
            t.send_keys(AI(prompt))
            continue
        else:
            continue
    try:
        t.send_keys(answers[response])
    except:
        pass

for d in dropdown_inputs:
    try:
        d.find_element(By.XPATH, '..//span[@class="asterisk"]')
    except:
        continue
    prompt = d.find_element(By.XPATH, '..').text
    submission = answers[Response(prompt)]
    d.click()
    input = driver.find_element(By.CSS_SELECTOR, 'div[id="select2-drop"] div input')
    options = driver.find_elements(By.CSS_SELECTOR, 'div[id="select2-drop"] ul li div')
    down = 0
    for o in options:
        choice = o.text
        choice = choice.lower()
        if choice == submission:
            break
        down += 1
    for _ in range(down):
        input.send_keys(Keys.DOWN)
    input.send_keys(Keys.ENTER)
    

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

for r in required_checkboxes:
    r.click()

driver.find_element(By.CSS_SELECTOR, 'input[id="submit_app]').click()

driver.quit()
