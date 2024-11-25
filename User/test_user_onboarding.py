import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pandas as pd
import os
from datetime import datetime

@pytest.fixture(scope="module")
def user_onboarding():
    driver = webdriver.Chrome()
    driver.maximize_window()
    file_path = r"D:\userinfo\login info.xlsx"
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
    yield driver  # Yielding the driver instance
    driver.quit()

@pytest.fixture
def take_screenshot(user_onboarding, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = user_onboarding
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = r"D:\Testcase\screenshots/user_onboarding"

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
        driver = item.funcargs.get('user_onboarding')
        if driver:
            test_name = item.name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshots_dir = r"D:\Testcase\screenshots/user_onboarding"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_user_onboarding(user_onboarding, take_screenshot):
    driver = user_onboarding
    driver.find_element(By.XPATH,"//button[normalize-space()='Assigned']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-users/div[1]/div[1]/div[3]/div/ul/li[2]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//body[1]/app-root[1]/div[3]/app-pending-onboarding-patient[1]/div[1]/div[2]/div[2]/div[1]/table[1]/tbody[1]/tr[2]/td[7]/div[1]/button[1]").click()
    driver.find_element(By.XPATH,"//span[@class='ng-arrow-wrapper']").click()
    time.sleep(2)
    # driver.find_element(By.XPATH,"//input[@placeholder='search country']").send_keys("United Kingdom")
    driver.find_element(By.XPATH,"//*[contains(text(), 'United Kingdom')]").click()
    driver.find_element(By.XPATH,"//div[@class='next-btn']").click()
    driver.find_element(By.XPATH,"//*[@id='unassigned-patient']/div/div/div/div/app-add-patient/div/div[2]/div[2]/div/div[2]/form/div[5]/div[2]").click()
    driver.find_element(By.XPATH,"//div[@class='next-btn']").click()
    driver.find_element(By.XPATH,"//div[@class='next-btn']").click()
    driver.find_element(By.XPATH,"//button[normalize-space()='Onboard User']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(5)