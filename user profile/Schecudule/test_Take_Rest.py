import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from faker import Faker
import pandas as pd
import os
from datetime import datetime


@pytest.fixture(scope="module")
def userprofile_schedule():
    driver = webdriver.Chrome()
    driver.maximize_window()
    file_path = r"D:\userinfo\login info.xlsx"
    df = pd.read_excel(file_path)
    url = df.iloc[0, 1]
    stm1_userid = df.iloc[4, 1]
    stm1_pass = df.iloc[4, 2]
    otp = df.iloc[4, 3]
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
def take_screenshot(userprofile_schedule, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = userprofile_schedule
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = r"D:\Testcase\screenshots/Take_Rest"

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
            screenshots_dir = r"D:\Testcase\screenshots/Take_Rest"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_create_TakeRest(userprofile_schedule, take_screenshot):
    driver = userprofile_schedule
    time.sleep(2)
    driver.find_element(By.XPATH, "//a[@id='Schedule']").click()
    driver.find_element(By.XPATH, "//div[normalize-space()='Take a Rest']").click()
    driver.find_element(By.XPATH, "//img[@src='./assets/images/edit.png']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//*[@id='dosage-edit-start-datepicker']/div/input").clear()
    driver.find_element(By.XPATH, "//*[@id='dosage-edit-start-datepicker']/div/input").send_keys('15 Nov 2024')
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-edit-landing-screen/div/div[1]/app-add-rest/div[1]/div[2]/div[1]/div[3]/label/nz-date-picker/div/input").clear()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-edit-landing-screen/div/div[1]/app-add-rest/div[1]/div[2]/div[1]/div[3]/label/nz-date-picker/div/input").send_keys('16 Nov 2024')
    time.sleep(2)
    take_screenshot()
    time.sleep(4)

def test_assign_TakeRest(userprofile_schedule, take_screenshot):
    driver = userprofile_schedule
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-edit-landing-screen/div/div[1]/app-add-rest/div[2]/button").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)


def test_edit_TakeRest(userprofile_schedule, take_screenshot):
    driver = userprofile_schedule
    driver.find_element(By.XPATH, "//img[@src='./assets/images/edit.png']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//*[@id='dosage-edit-start-datepicker']/div/input").clear()
    driver.find_element(By.XPATH, "//*[@id='dosage-edit-start-datepicker']/div/input").send_keys('21 Nov 2024')
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-edit-landing-screen/div/div[1]/app-add-rest/div[1]/div[2]/div[1]/div[3]/label/nz-date-picker/div/input").clear()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-edit-landing-screen/div/div[1]/app-add-rest/div[1]/div[2]/div[1]/div[3]/label/nz-date-picker/div/input").send_keys('30 Nov 2024')
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='form-input-wrap ng-star-inserted']//div[@class='dropdown']").click()
    driver.find_element(By.XPATH, "//li[normalize-space()='12:30 am']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@class='btn btn-success save-medicine-btn']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)
