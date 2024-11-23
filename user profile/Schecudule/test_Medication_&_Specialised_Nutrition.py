import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from faker import Faker
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime


@pytest.fixture(scope="module")
def userprofile_schedule():
    driver = webdriver.Chrome()
    driver.maximize_window()
    file_path = r"D:\pytest\login info.xlsx"
    df = pd.read_excel(file_path)
    url = df.iloc[0, 1]
    stm1_userid = df.iloc[4, 1]
    stm1_pass = df.iloc[4, 2]
    otp = df.iloc[3, 3]
    user = df.iloc[10, 1]
    driver.get(url)
    driver.implicitly_wait(100)
    driver.find_element(By.XPATH, "//div[@class='login-form']//div[1]//label[1]").send_keys(stm1_userid)
    driver.find_element(By.XPATH, "//div[@class='divisions']//div[2]//label[1]//input[1]").send_keys(stm1_pass)
    driver.find_element(By.XPATH, "//input[@value='Sign In']").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//input[@id='inp']").send_keys(otp)
    driver.find_element(By.XPATH, "//input[@value='Submit']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(user)
    driver.find_element(By.XPATH, "//div[@class='p-element blurry-text']").click()
    time.sleep(3)
    yield driver  # Yielding the driver instance
    driver.quit()

@pytest.fixture
def take_screenshot(org_login, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = org_login
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = "D:/pytest/screenshots/Medication_&_Specialised_Nutrition"

    os.makedirs(screenshots_dir, exist_ok=True)

    def _screenshot():
        file_name = f"{test_name}_{timestamp}.png"
        file_path = os.path.join(screenshots_dir, file_name)
        driver.save_screenshot(file_path)
        print(f"Screenshot saved at {file_path}")

    return _screenshot


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot if a test fails."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get('org_login')
        if driver:
            test_name = item.name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshots_dir = "D:/pytest/screenshots/Medication_&_Specialised_Nutrition"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_Medication_page(userprofile_schedule, take_screenshot):
    driver = userprofile_schedule
    driver.find_element(By.XPATH, "//a[@id='Schedule']").click()
    time.sleep(4)
    driver.find_element(By.XPATH,"//div[@class='log-disease-title'][normalize-space()='Medication & Specialised Nutrition']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)

def test_create_Medication(userprofile_schedule, take_screenshot):
    driver = userprofile_schedule
    driver.find_element(By.XPATH, "//*[contains(text(), '+ Add New Medication')]").click()
    time.sleep(2)
    global medichine_name
    medichine_name = driver.find_element(By.XPATH, "//tbody/tr[6]/td[1]").text
    driver.find_element(By.XPATH, "//tbody/tr[6]/td[1]").click()
    driver.find_element(By.XPATH, "//div[@class='form-input-wrap']//label[@class='date-picker-label']//img").click()
    time.sleep(1)
    today_date = str(datetime.now().day)
    driver.find_element(By.XPATH, f"//div[normalize-space()='{today_date}']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[contains(text(),'End Date')]//img").click()
    driver.find_element(By.XPATH, "//li[normalize-space()='End Date']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='form-input-wrap ng-star-inserted']//img").click()
    time.sleep(1)
    today_date = str((datetime.now().day) + 5)
    driver.find_element(By.XPATH, f"//div[normalize-space()='{today_date}']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)


def test_assign_Medication(userprofile_schedule, take_screenshot):
    driver = userprofile_schedule
    text = driver.find_element(By.XPATH, "//*[contains(text(), 'Save Medication')]").text
    assert text == "Save"
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Save Medication')]")))
    element.click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)



def test_edit_Medication(userprofile_schedule, take_screenshot):
    driver = userprofile_schedule
    driver.find_element(By.XPATH, f"//div[normalize-space()='{medichine_name}']").click()
    driver.find_element(By.XPATH, "//div[@class='edit-schedule']//img").click()
    driver.find_element(By.XPATH, "//div[contains(text(),'End Date')]//img").click()
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-edit-landing-screen/div/div[1]/app-edit-medicine/div[1]/div[2]/div[3]/div[2]/div/div[1]/div[2]/div/div").click()
    driver.find_element(By.XPATH, "//li[normalize-space()='11:45 pm']").click()
    driver.find_element(By.XPATH, "//button[normalize-space()='Save Medication']").click()
    time.sleep(4)
    take_screenshot()
    time.sleep(4)














