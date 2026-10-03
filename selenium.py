from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()
try:
    driver.get("https://quotes.toscrape.com/login")
    time.sleep(3)
    username_field = driver.find_element(By.CSS_SELECTOR, "#username")
    password_field = driver.find_element(By.CSS_SELECTOR, "#password")
    username_field.send_keys("student_user")
    password_field.send_keys("secret_password")
    print("Successfully found elements and filled the form using Selenium!")
    time.sleep(5)
finally:
    driver.quit()