from imports import *
from response import Response

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

chrome_options = Options()

chrome_options.add_argument('--remote-debugging-pipe')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)

driver.get("https://clarioclinical.wd1.myworkdayjobs.com/en-US/clarioclinical_careers/job/Intern--Clinical-Data-Management--Imaging_R14233")

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
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, '[data-automation-id="click_filter"]').send_keys(Keys.ENTER)
except:
    pass

time.sleep(3)
count = 1
while True:
    print(count)
    i = ""
    try:
        i = driver.find_element(By.ID, 'input-' + str(count))
    except Exception as e:
        print(e)
        break
    id = i.get_attribute("id")
    prompt = ""
    try:
        label = driver.find_element(By.CSS_SELECTOR, '[for="' + id + '"]')
        prompt = label.text
    except:
        prompt = i.get_attribute("data-automation-id")
    response = Response(prompt)
    if response == "skip":
        continue
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

    if input_type == "text":
        i.send_keys(response)
    elif input_type == "dropdown":
        i.send_keys(response)
    elif input_type == "mc_search":
        i.send_keys(response)
        i.send_keys(Keys.RETURN)
        i.send_keys(Keys.RETURN)
    count+=1
        

time.sleep(600)
driver.quit()