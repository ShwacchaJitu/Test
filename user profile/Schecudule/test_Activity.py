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
    screenshots_dir = "D:/pytest/screenshots/Activity"

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
            screenshots_dir = "D:/pytest/screenshots/Activity"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")



def test_create_Activity(userprofile_schedule, take_screenshot):
    driver = userprofile_schedule
    fake = Faker()
    global group_name
    group_name = fake.name()
    notes = fake.sentence()
    driver.find_element(By.XPATH, "//div[@class='navigation-bars']//div[4]").click()
    driver.find_element(By.XPATH, "//div[normalize-space()='Activity']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//div[@class='add-exercise']").click()
    driver.find_element(By.XPATH, "//input[@placeholder='Enter group name']").send_keys(group_name)
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[@class='ng-arrow-wrapper']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[normalize-space()='Walking (For Stride Analysis)']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[@class='btn-outline-single']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[@placeholder='Eg. Take 2-3 minutes rest in between each set.']").send_keys("Create using automation")
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[contains(text(),'End Date')]//img").click()
    driver.find_element(By.XPATH, "//li[normalize-space()='Number of Days']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[@type='number']").clear()
    driver.find_element(By.XPATH, "//input[@type='number']").send_keys(5)
    time.sleep(3)
    take_screenshot()
    time.sleep(4)


def test_assign_Activity(userprofile_schedule, take_screenshot):
    driver = userprofile_schedule
    driver.find_element(By.XPATH, "//button[normalize-space()='Add to Schedule']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)

def test_edit_Activity(userprofile_schedule, take_screenshot):
    driver = userprofile_schedule
    driver.find_element(By.XPATH, "//img[@src='./assets/images/edit.png']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@placeholder='Enter group name']").clear()
    driver.find_element(By.XPATH, "//input[@placeholder='Enter group name']").send_keys(group_name)
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[normalize-space()='Number of Days']//img").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//li[normalize-space()='End Date']").click()
    # driver.find_element(By.XPATH, "//div[@aria-disabled='false'][normalize-space()='30']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[normalize-space()='Update Schedule']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)


def test_delete_Activity(userprofile_schedule, take_screenshot):
    driver = userprofile_schedule
    driver.find_element(By.XPATH, "//img[@src='./assets/images/edit.png']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-edit-landing-screen/div/div[1]/app-nw-edit-exercise/div[2]/button").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-edit-landing-screen/div/div[1]/app-nw-edit-exercise/div[5]/div/div/div/div/div[3]/button[2]").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)


