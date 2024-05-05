from imports import *

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
    time.sleep(0.1)

inputs = driver.find_elements(By.XPATH, '//*[@id[starts-with(., "input-")]]')
for i in inputs:
    id = i.get_attribute("id")
    prompt = ""
    try:
        label = driver.find_element(By.CSS_SELECTOR, '[for="' + id + '"]')
        prompt = label.text
    except:
        prompt = i.get_attribute("data-automation-id")
    print(prompt)



#driver.quit()