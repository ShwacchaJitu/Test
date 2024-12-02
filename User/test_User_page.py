import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
from datetime import datetime


@pytest.fixture(scope="module")
def user():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver = webdriver.Chrome()
    driver.maximize_window()
    file_path = r"D:\userinfo\login info.xlsx"
    df = pd.read_excel(file_path)
    url = df.iloc[0, 1]
    org_userid = df.iloc[1, 1]
    org_pass = df.iloc[1, 2]
    otp = df.iloc[1, 3]
    driver.get(url)
    driver.implicitly_wait(100)
    driver.find_element(By.XPATH, "//div[@class='login-form']//div[1]//label[1]").send_keys(org_userid)
    driver.find_element(By.XPATH, "//div[@class='divisions']//div[2]//label[1]//input[1]").send_keys(org_pass)
    driver.find_element(By.XPATH, "//input[@value='Sign In']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@id='inp']").send_keys(otp)
    driver.find_element(By.XPATH, "//input[@value='Submit']").click()
    time.sleep(5)
    yield driver  # Yielding the driver instance
    driver.quit()


@pytest.fixture
def take_screenshot(user, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = user
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = r"D:\Testcase\screenshots/User_page"

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
            screenshots_dir = r"D:\Testcase\screenshots/User_page"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_landing_page(user, take_screenshot):
    driver = user
    driver.find_element(By.XPATH,"//span[normalize-space()='Organisation']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//a[normalize-space()='Users']").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Assigned_User(user, take_screenshot):
    driver = user
    driver.find_element(By.XPATH, "//button[normalize-space()='Sort']")
    driver.find_element(By.XPATH, "//img[@title='Refresh']")
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_all_User(user, take_screenshot):
    driver = user
    driver.find_element(By.XPATH, "//div[@class='user-list-title']//div[@class='dropdown']").click()
    driver.find_element(By.XPATH, "//div[@class='user-list-title']//li[1]//a[1]").click()
    driver.find_element(By.XPATH, "//button[normalize-space()='Sort']")
    driver.find_element(By.XPATH, "//input[@placeholder='Search']")
    driver.find_element(By.XPATH, "//img[@title='Refresh']")
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Unassigned_User(user, take_screenshot):
    driver = user
    driver.find_element(By.XPATH, "//div[@class='user-list-title']//div[@class='dropdown']").click()
    driver.find_element(By.XPATH, "//div[@class='user-list-title']//li[3]//a[1]").click()
    driver.find_element(By.XPATH, "//button[normalize-space()='Sort']")
    driver.find_element(By.XPATH, "//input[@placeholder='Search']")
    driver.find_element(By.XPATH, "//img[@title='Refresh']")
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Pending_Onboarding_User(user, take_screenshot):
    driver = user
    driver.find_element(By.XPATH, "//div[@class='user-list-title']//div[@class='dropdown']").click()
    driver.find_element(By.XPATH, "//div[@class='user-list-title']//li[4]//a[1]").click()
    driver.find_element(By.XPATH, "//img[@title='Refresh']")
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Pending_Activation_User(user, take_screenshot):
    driver = user
    driver.find_element(By.XPATH, "//div[@class='user-list-title']//div[@class='dropdown']").click()
    driver.find_element(By.XPATH, "//div[@class='user-list-title']//li[5]//a[1]").click()
    driver.find_element(By.XPATH, "//img[@title='Refresh']")
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Invited_User(user, take_screenshot):
    driver = user
    driver.find_element(By.XPATH, "//div[@class='user-list-title']//div[@class='dropdown']").click()
    driver.find_element(By.XPATH, "//div[@class='user-list-title']//li[6]//a[1]").click()
    driver.find_element(By.XPATH, "//img[@title='Refresh']")
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_reinvited_User(user, take_screenshot):
    driver = user
    driver.find_element(By.XPATH,"//body[1]/app-root[1]/div[3]/app-all-patients[1]/div[1]/div[2]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[8]/div[1]/span[1]/img[1]").click()
    driver.find_element(By.XPATH, "//div[contains(text(),'Resend Invitation')]").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(1)









