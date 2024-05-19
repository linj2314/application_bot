from imports import *
from utilities import *

chrome_options = Options()

chrome_options.add_argument('--remote-debugging-pipe')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)

driver.get("https://boards.greenhouse.io/torcrobotics/jobs/7067416002")

text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']:not([class])")
dropdown_inputs_1 = driver.find_elements(By.CSS_SELECTOR, "div[class='select2-container']")
dropdown_inputs_2 = driver.find_elements(By.TAG_NAME, 'select')
file_inputs = driver.find_elements(By.CSS_SELECTOR, "button[data-source='attach']")
required_checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox'][aria-required='true']")
checkbox_questions = driver.find_elements(By.CSS_SELECTOR, "label label:nth-of-type(1) input[type='checkbox']")

skip_dropdown_2 = False
if len(dropdown_inputs_1) > 0:
    skip_dropdown_2 = True

company_name = driver.find_element(By.CSS_SELECTOR, "span[class='company-name']").text
company_name = company_name.split()
company_name = company_name[1]
role_name = driver.find_element(By.CSS_SELECTOR, "h1[class='app-title']").text

for t in text_inputs:
    if t.get_attribute("aria-label") == "Education Start Month":
        t.send_keys(answers["start_month"])
    elif t.get_attribute("aria-label") == "Education Start Year":
        t.send_keys(answers["start_year"])
    elif t.get_attribute("aria-label") == "Education End Month":
        t.send_keys(answers["end_month"])
    elif t.get_attribute("aria-label") == "Education End Year":
        t.send_keys(answers["end_year"])
    elif t.get_attribute("name") == "job_application[location]":
        t.send_keys(answers["location"])
    prompt = t.find_element(By.XPATH, '..').text
    if not prompt:
        continue
    response = Response(prompt)
    if response == 'skip_fs':
        continue
    if response == 'skip':
        t.send_keys(AI(prompt))
    else:
        try:
            t.send_keys(answers[response])
        except:
            pass

for d in dropdown_inputs_1:
    prompt = d.find_element(By.XPATH, '..').text
    prompt = prompt.split('\n')[0]
    print(prompt)
    response = Response(prompt)
    if response == 'skip_fs':
        continue
    d.click()
    input = driver.find_element(By.CSS_SELECTOR, 'div[id="select2-drop"] div input')
    options = driver.find_elements(By.CSS_SELECTOR, 'div[id="select2-drop"] ul li div')
    if response == "skip":
        choices = []
        for o in options:
            choices.append(o.text)
        submission = AI(prompt, choices)
        down = 0
        for o in options:
            if o.text == submission:
                break
            down += 1
        for _ in range(down):
            input.send_keys(Keys.DOWN)
        input.send_keys(Keys.ENTER)
    else:
        choices = []
        submission = answers[response]
        down = 0
        found = False
        for o in options:
            choice = o.text
            choices.append(choice)
            choice = clean_str(choice)
            if choice == submission:
                found = True
                break
            down += 1
        if found:
            for _ in range(down):
                input.send_keys(Keys.DOWN)
            input.send_keys(Keys.ENTER)
        else:
            submission = AI(prompt, choices)
            down = 0
            for o in options:
                if o.text == submission:
                    break
                down += 1
            for _ in range(down):
                input.send_keys(Keys.DOWN)
            input.send_keys(Keys.ENTER)

if not skip_dropdown_2:
    for d in dropdown_inputs_2:
        sd = Select(d)
        prompt = d.find_element(By.XPATH, '..').text
        response = Response(prompt)
        if response == "skip_fs":
            continue
        if response == "skip":
            choices = []
            for o in d.find_elements(By.CSS_SELECTOR, "option"):
                choices.append(o.text)
            sd.select_by_visible_text(AI(prompt, choices))
        else:
            ind = 0
            found = False
            choices = []
            for o in d.find_elements(By.CSS_SELECTOR, "option"):
                choices.append(o.text)
                if clean_str(o.text) == answers[response]:
                    sd.select_by_index(ind)
                    found = True
                    break
                ind += 1
            if not found:
                sd.select_by_visible_text(AI(prompt, choices))

for c in checkbox_questions:
    question = c.find_element(By.XPATH, '..//..')
    prompt = question.text.split('\n')[0]
    response = Response(prompt)
    if response == "skip_fs":
        continue
    if response == "skip":
        choices = []
        boxes = question.find_elements(By.CSS_SELECTOR, "label")
        for b in boxes:
            choices.append(b.text)
        submission = AI(prompt, choices)
        print(submission)
        for b in boxes:
            if b.text == submission:
                b.find_element(By.CSS_SELECTOR, "input").click()
                break
    else:
        boxes = question.find_elements(By.CSS_SELECTOR, "label")
        found = False
        choices = []
        submission = answers[response]
        for b in boxes:
            choices.append(b.text)
            choice = clean_str(b.text)
            if submission == choice:
                b.find_element(By.CSS_SELECTOR, "input").click()
                found = True
                break
        if not found:
            submission = AI(prompt, choices)
            for b in boxes:
                if b.text == submission:
                    b.find_element(By.CSS_SELECTOR, "input").click()
                    break

for f in file_inputs:
    prompt = f.get_attribute('aria-describedby')
    response = Response(prompt)
    if response == "skip_fs":
        continue
    if response == "cover_letter":
        CL_Write(company_name, role_name, True)
    f.click()
    subprocess.Popen(['xdotool', 'search', '--sync', '--onlyvisible', '--class', 'dialog'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(0.5)
    subprocess.Popen(['xdotool', 'type', answers[response]])
    time.sleep(0.5)
    subprocess.Popen(['xdotool', 'key', 'Return'])
    time.sleep(1)

for r in required_checkboxes:
    r.click()

#driver.find_element(By.ID, 'submit_app').click()

time.sleep(100)

driver.quit()
