from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import time
import re
import subprocess
load_dotenv()
answers = {
    "HDYHAU": "I",
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
    "phone_extension": "skip",
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
    "company": os.getenv("COMPANY")
}