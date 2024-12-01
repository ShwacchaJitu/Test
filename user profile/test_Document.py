import os.path
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
from datetime import datetime


@pytest.fixture(scope="module")
def userprofile_document():
    driver = webdriver.Chrome()
    driver.maximize_window()
    file_path = r"D:\userinfo\login info.xlsx"
    df = pd.read_excel(file_path)
    url = df.iloc[0, 1]
    stm1_userid = df.iloc[4, 1]
    stm1_pass = df.iloc[4, 2]
    otp = df.iloc[4, 3]
    driver.get(url)
    driver.implicitly_wait(100)
    driver.find_element(By.XPATH, "//div[@class='login-form']//div[1]//label[1]").send_keys(stm1_userid)
    driver.find_element(By.XPATH, "//div[@class='divisions']//div[2]//label[1]//input[1]").send_keys(stm1_pass)
    driver.find_element(By.XPATH, "//input[@value='Sign In']").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//input[@id='inp']").send_keys(otp)
    driver.find_element(By.XPATH, "//input[@value='Submit']").click()
    time.sleep(5)
    user = df.iloc[10, 1]
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
    screenshots_dir = r"D:\Testcase\screenshots/Document"

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
            screenshots_dir = r"D:\Testcase\screenshots/Document"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")

def test_Navigating_Document(userprofile_document, take_screenshot):
    driver = userprofile_document
    driver.find_element(By.XPATH, "//a[@id='Document']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//a[normalize-space()='Upload Files']").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Document_Upload(userprofile_document, take_screenshot):
    driver = userprofile_document
    time.sleep(2)
    image = os.path.abspath('Document.jpg')
    driver.find_element(By.XPATH, "/html[1]/body[1]/app-root[1]/div[3]/app-profile[1]/div[1]/div[2]/div[1]/app-upload-document[1]/div[1]/div[2]/form[1]/file-upload[1]/label[1]/input[1]").send_keys(image)
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[normalize-space()='Upload All']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-upload-document/div[2]/div/div/div[2]/div[2]/button[2]").click()
    time.sleep(6)
    take_screenshot()
    time.sleep(1)

def test_Document_Sent_User(userprofile_document, take_screenshot):
    driver = userprofile_document
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(6)
    take_screenshot()
    time.sleep(1)

def test_Document_Sent_User(userprofile_document, take_screenshot):
    driver = userprofile_document
    time.sleep(2)
    driver.find_element(By.XPATH, "//tbody/tr[1]/td[1]/label[1]/span[1]").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//div[@class='broadCast-bottom-option-container ng-star-inserted']//img[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-document/div[2]/div/div/div/div[3]/button").click()
    time.sleep(6)
    take_screenshot()
    time.sleep(1)

def test_Document_Archive(userprofile_document, take_screenshot):
    driver = userprofile_document
    driver.refresh()
    time.sleep(10)
    driver.find_element(By.XPATH,"//body[1]/app-root[1]/div[3]/app-profile[1]/div[1]/div[2]/div[1]/app-document[1]/div[1]/div[2]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[7]/div[1]/img[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-document/div[7]/div/div/div/div/div[2]/div/button[2]").click()
    time.sleep(6)
    driver.find_element(By.XPATH, "//button[normalize-space()='Files']").click()
    driver.find_element(By.XPATH, "//a[@id='Archived']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//tr[@class='ng-star-inserted']//span[@class='checkmark']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-archive-document/div[1]/div[2]/div[2]/div[3]/div/div[2]/img").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-archive-document/div[2]/div/div/div/div/div[2]/div/button[2]").click()
    time.sleep(6)
    take_screenshot()
    time.sleep(1)

def test_Document_Recovered(userprofile_document, take_screenshot):
    driver = userprofile_document
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[normalize-space()='Archived']").click()
    driver.find_element(By.XPATH, "//a[@id='Files']").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(1)