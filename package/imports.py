from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from dotenv import load_dotenv
import os
import time
import re
import subprocess
from g4f.client import Client
from g4f.Provider import *
from g4f.errors import RateLimitError
import undetected_chromedriver as uc
from datetime import datetime
from package.exceptions import ExpiredApplicationError, RequiredWorkExperienceError
import getopt, sys
load_dotenv()
answers = {
    "HDYHAU": "other",
    "first": os.getenv("FIRST"),
    "last": os.getenv("LAST"),
    "name": os.getenv("NAME"),
    "address": os.getenv("ADDRESS"), 
    "city": os.getenv("CITY"),
    "state": os.getenv("STATE"),
    "zip": os.getenv("ZIP"),
    "email": os.getenv("EMAIL"),
    "phone_type": os.getenv("PHONE_TYPE"),
    "country_code": os.getenv("COUNTRY_CODE"), 
    "phone_number": os.getenv("PHONE_NUMBER"),
    "school": os.getenv("SCHOOL"),
    "degree": os.getenv("DEGREE"),
    "major": os.getenv("MAJOR"),
    "GPA": os.getenv("GPA"),
    "from": os.getenv("FROM"),
    "to": os.getenv("TO"),
    "linkedin": os.getenv("LINKEDIN"),
    "website": os.getenv("WEBSITE"),
    "resume": os.getenv("RESUME"),
    "cover_letter": os.getenv("COVER_LETTER"),
    "transcript": os.getenv("TRANSCRIPT"),
    "skills": os.getenv("SKILLS"),
    "worked_for": os.getenv("WORKED_FOR"),
    "us_authorization": os.getenv("US_AUTHORIZATION"),
    "sponsorship": os.getenv("SPONSORSHIP"), 
    "pronouns": os.getenv("PRONOUNS"),
    "location": os.getenv("LOCATION"),
    "company": os.getenv("COMPANY"),
    "github": os.getenv("GITHUB"),
    "twitter": os.getenv("TWITTER"),
    "start_month": os.getenv("START_MONTH"),
    "start_year": os.getenv("START_YEAR"),
    "end_month": os.getenv("END_MONTH"),
    "end_year": os.getenv("END_YEAR"),
    "country": os.getenv("COUNTRY"),
    "race": os.getenv("RACE"),
    "gender": os.getenv("GENDER"),
    "county": os.getenv("COUNTY")
}
AI_PROMPT = os.getenv("AI_PROMPT")
CL_1 = os.getenv("CL_1")
CL_2 = os.getenv("CL_2")
CL_3 = os.getenv("CL_3")
CL_4 = os.getenv("CL_4")
CL_5 = os.getenv("CL_5")