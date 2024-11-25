import pytest
import time
from selenium import webdriver
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.maximize_window()
file_path = r"D:\pytest\login info.xlsx"
df = pd.read_excel(file_path)
url = df.iloc[0, 1]
stm1_userid = df.iloc[4, 1]
stm1_pass = df.iloc[4, 2]
otp = df.iloc[3, 3]
driver.get(url)
driver.implicitly_wait(100)
driver.find_element(By.XPATH, "//div[@class='login-form']//div[1]//label[1]").send_keys(stm1_userid)
driver.find_element(By.XPATH, "//div[@class='divisions']//div[2]//label[1]//input[1]").send_keys(stm1_pass)
driver.find_element(By.XPATH, "//input[@value='Sign In']").click()
time.sleep(3)
driver.find_element(By.XPATH, "//input[@id='inp']").send_keys(otp)
driver.find_element(By.XPATH, "//input[@value='Submit']").click()
time.sleep(5)



"""Filter"""
# driver.find_element(By.XPATH, "//button[normalize-space()='Filter']").click()
# time.sleep(2)
# driver.find_element(By.XPATH, "//button[normalize-space()='Done']").click()
# time.sleep(2)

"""Sort"""
# driver.find_element(By.XPATH, "//button[normalize-space()='Sort']").click()
# time.sleep(3)


"""Schedule Message"""
first_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div[3]/app-users/div[1]/div[2]/div[2]/div[1]/table/tbody/tr/td[1]/label/span[1]"))
)
first_element.click()
second_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[src='./assets/images/broadcast.png']"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", second_element)
time.sleep(1)
for attempt in range(5):
    try:
        second_element.click()
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(1)

time.sleep(3)
driver.find_element(By.XPATH, "//img[@alt='schedule']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='broadcast-message-patients']/div/div/div/div[2]/div[1]").click()
time.sleep(2)
driver.find_element(By.XPATH, "//button[normalize-space()='Next']").click()
time.sleep(2)
today_date = datetime.now().strftime("%a, %d %b %Y")
driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-users/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div[1]/label/nz-date-picker/div/input").send_keys(today_date)
tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%a, %d %b %Y")
driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-users/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div[3]/label/nz-date-picker/div/input").send_keys(tomorrow_date)
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='broadcast-message-patients']/div/div/div/div[2]/div[1]/div/div[5]/div/div[1]/label/label/span").click()
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='broadcast-message-patients']/div/div/div/div[2]/div[2]/button[1]").click()
driver.find_element(By.XPATH, "//button[normalize-space()='Schedule']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//button[@class='msgSubBtn']").click()
time.sleep(5)


"""Alert Escalation Message"""
faker = Faker()
message_body = faker.sentence()
driver.find_element(By.XPATH, "//tbody/tr[3]/td[1]/label[1]/span[1]").click()
time.sleep(2)
driver.find_element(By.XPATH, "//img[@src='./assets/images/send-message-hover.png']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//input[@formcontrolname='title']").send_keys('Automation')
driver.find_element(By.XPATH, "//textarea[@class='ng-untouched ng-pristine ng-invalid']").send_keys(message_body)
time.sleep(2)
driver.find_element(By.XPATH, "//button[normalize-space()='Send Escalation']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//div[@id='custom-alerts-to-users-success-message']//button[@class='btn btn-primary ack-dismiss-btn-custom'][normalize-space()='Dismiss']").click()
time.sleep(5)


"""Widgets"""
driver.find_element(By.XPATH, "//tbody/tr[3]/td[1]/label[1]/span[1]").click()
time.sleep(2)
driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-users/div[1]/div[2]/div[2]/div[3]/div/div[2]/img[3]").click()
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='customise-widget-modal']/div/div/div/div/div[2]/div[1]/label[2]/span[2]").click()
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='customise-widget-modal']/div/div/div/div/div[2]/div[1]/label[2]/span[2]").click()
time.sleep(2)
driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()
driver.find_element(By.XPATH, "//div[@id='success-message-widget']//button[@class='btn ack-dismiss-btn2'][normalize-space()='Dismiss']").click()
time.sleep(2)




import pytest
import time
from selenium import webdriver
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.maximize_window()
file_path = r"D:\pytest\login info.xlsx"
df = pd.read_excel(file_path)
url = df.iloc[0, 1]
stm1_userid = df.iloc[4, 1]
stm1_pass = df.iloc[4, 2]
otp = df.iloc[3, 3]
driver.get(url)
driver.implicitly_wait(100)
driver.find_element(By.XPATH, "//div[@class='login-form']//div[1]//label[1]").send_keys(stm1_userid)
driver.find_element(By.XPATH, "//div[@class='divisions']//div[2]//label[1]//input[1]").send_keys(stm1_pass)
driver.find_element(By.XPATH, "//input[@value='Sign In']").click()
time.sleep(3)
driver.find_element(By.XPATH, "//input[@id='inp']").send_keys(otp)
driver.find_element(By.XPATH, "//input[@value='Submit']").click()
time.sleep(5)



"""Filter"""
# driver.find_element(By.XPATH, "//button[normalize-space()='Filter']").click()
# time.sleep(2)
# driver.find_element(By.XPATH, "//button[normalize-space()='Done']").click()
# time.sleep(2)

"""Sort"""
# driver.find_element(By.XPATH, "//button[normalize-space()='Sort']").click()
# time.sleep(3)


"""Schedule Message"""
first_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div[3]/app-users/div[1]/div[2]/div[2]/div[1]/table/tbody/tr/td[1]/label/span[1]"))
)
first_element.click()
second_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[src='./assets/images/broadcast.png']"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", second_element)
time.sleep(1)
for attempt in range(5):
    try:
        second_element.click()
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(1)

time.sleep(3)
driver.find_element(By.XPATH, "//img[@alt='schedule']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='broadcast-message-patients']/div/div/div/div[2]/div[1]").click()
time.sleep(2)
driver.find_element(By.XPATH, "//button[normalize-space()='Next']").click()
time.sleep(2)
today_date = datetime.now().strftime("%a, %d %b %Y")
driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-users/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div[1]/label/nz-date-picker/div/input").send_keys(today_date)
tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%a, %d %b %Y")
driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-users/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div[3]/label/nz-date-picker/div/input").send_keys(tomorrow_date)
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='broadcast-message-patients']/div/div/div/div[2]/div[1]/div/div[5]/div/div[1]/label/label/span").click()
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='broadcast-message-patients']/div/div/div/div[2]/div[2]/button[1]").click()
driver.find_element(By.XPATH, "//button[normalize-space()='Schedule']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//button[@class='msgSubBtn']").click()
time.sleep(5)


"""Alert Escalation Message"""
faker = Faker()
message_body = faker.sentence()
driver.find_element(By.XPATH, "//tbody/tr[3]/td[1]/label[1]/span[1]").click()
time.sleep(2)
driver.find_element(By.XPATH, "//img[@src='./assets/images/send-message-hover.png']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//input[@formcontrolname='title']").send_keys('Automation')
driver.find_element(By.XPATH, "//textarea[@class='ng-untouched ng-pristine ng-invalid']").send_keys(message_body)
time.sleep(2)
driver.find_element(By.XPATH, "//button[normalize-space()='Send Escalation']").click()
time.sleep(2)
driver.find_element(By.XPATH, "//div[@id='custom-alerts-to-users-success-message']//button[@class='btn btn-primary ack-dismiss-btn-custom'][normalize-space()='Dismiss']").click()
time.sleep(5)


"""Widgets"""
driver.find_element(By.XPATH, "//tbody/tr[3]/td[1]/label[1]/span[1]").click()
time.sleep(2)
driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-users/div[1]/div[2]/div[2]/div[3]/div/div[2]/img[3]").click()
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='customise-widget-modal']/div/div/div/div/div[2]/div[1]/label[2]/span[2]").click()
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='customise-widget-modal']/div/div/div/div/div[2]/div[1]/label[2]/span[2]").click()
time.sleep(2)
driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()
driver.find_element(By.XPATH, "//div[@id='success-message-widget']//button[@class='btn ack-dismiss-btn2'][normalize-space()='Dismiss']").click()
time.sleep(2)

print("Testing")



