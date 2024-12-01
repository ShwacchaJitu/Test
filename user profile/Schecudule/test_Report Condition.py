import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    screenshots_dir = r"D:\Testcase\screenshots/Report Condition"

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
            screenshots_dir = r"D:\Testcase\screenshots/Report Condition"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")



def test_Schedule(userprofile_schedule, take_screenshot):
    driver= userprofile_schedule
    driver.find_element(By.XPATH, "//a[@id='Schedule']").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Create_Report_Condition(userprofile_schedule, take_screenshot):
    driver = userprofile_schedule
    driver.find_element(By.XPATH,"//div[@class='log-disease-title'][normalize-space()='Report Condition']").click()
    driver.find_element(By.XPATH,"//img[@src='./assets/images/edit.png']").click()
    driver.find_element(By.XPATH,"//div[@class='form-input-wrap']//label[@class='date-picker-label']//img").click()
    today_date = str(datetime.now().day)
    driver.find_element(By.XPATH, f"//div[normalize-space()='{today_date}']").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"//div[@class='schedule-drop-value duration']//img").click()
    driver.find_element(By.XPATH,"//li[normalize-space()='End Date']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//div[@class='form-input-wrap ng-star-inserted']//label[@class='date-picker-label']//img").click()
    today_date = str((datetime.now().day) + 5)
    driver.find_element(By.XPATH, f"//div[normalize-space()='{today_date}']").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(1)


def test_assign_Report_Condition(userprofile_schedule, take_screenshot):
    driver = userprofile_schedule
    text = driver.find_element(By.XPATH, "//*[contains(text(), 'Save')]").text
    assert text == "Save"
    driver.find_element(By.XPATH, "//*[contains(text(), 'Save')]").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(1)