import pytest
import time
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
from datetime import datetime

@pytest.fixture(scope="module")
def org_login():
    driver = webdriver.Chrome()
    driver.maximize_window()
    file_path = r"D:\userinfo\login info.xlsx"
    df = pd.read_excel(file_path)
    url = df.iloc[0, 1]
    org_userid = df.iloc[1, 1]
    org_pass = df.iloc[1, 2]
    otp = df.iloc[3, 3]
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
    time.sleep(5)
    driver.quit()


@pytest.fixture
def take_screenshot(org_login, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = org_login
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = r"D:\Testcase\screenshots/medichine"

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
            screenshots_dir = r"D:\Testcase\screenshots/medichine"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_medichine_page(org_login, take_screenshot):
    driver = org_login
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[normalize-space()='Programme Management']").click()
    driver.find_element(By.XPATH, "//a[normalize-space()='Medicines']").click()
    time.sleep(2)
    take_screenshot()

def test_create_medichine(org_login, take_screenshot):
    driver = org_login
    fake = Faker()  # Specify 'en_GB' for UK locale
    global medicine_name
    medicine_name = fake.name()
    brand = fake.name()
    time.sleep(5)
    driver.find_element(By.XPATH, "//div[@class='add-patient-btn']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@trim='blur']").send_keys(medicine_name)
    driver.find_element(By.XPATH, "//input[@formcontrolname='brand']").send_keys(brand)
    driver.find_element(By.XPATH, "//label[@class='schedule-drop-value inp']//img").click()
    driver.find_element(By.XPATH,"//*[@id='add-medicine']/div/div/div/div/app-add-medicine/div/div/div[2]/div[2]/form/div[3]/div[1]/div/ul/li[1]").click()
    driver.find_element(By.XPATH, "//label[@class='inp adjacent-box']//input[@id='inp']").send_keys(100)
    driver.find_element(By.XPATH, "//div[@class='schedule-drop-value duration']//img").click()
    driver.find_element(By.XPATH, "//*[@id='add-medicine']/div/div/div/div/app-add-medicine/div/div/div[2]/div[2]/form/div[4]/div/div/ul/li[1]").click()
    driver.find_element(By.XPATH, "//div[@class='next-btn']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@class='btn btn-primary confirm-medi-btn']").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@class='btn btn-primary ack-dismiss-btn']").click()
    time.sleep(4)


def test_Search_medichine(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(medicine_name)
    medicine = driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-medicine/div[1]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[1]").text
    assert medicine == medicine_name
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Refresh_medichine(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Edit_medichine(org_login, take_screenshot):
    driver = org_login
    fake = Faker()
    global new_medicine_name
    new_medicine_name = fake.name()
    driver.find_element(By.XPATH, "//tbody/tr[1]/td[5]/div[1]/img[1]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='content-body']//div[1]//label[1]//input[1]").clear()
    driver.find_element(By.XPATH, "//div[@class='content-body']//div[1]//label[1]//input[1]").send_keys(new_medicine_name)
    driver.find_element(By.XPATH, "//div[normalize-space()='Capsule']//img").click()
    driver.find_element(By.XPATH, "//*[@id='add-medicine']/div/div/div/div/app-edit-medicine/div/div[2]/div/form/div[3]/div[2]/div/ul/li[3]").click()
    driver.find_element(By.XPATH, "//label[@class='inp adjacent-box']//input[@id='inp']").clear()
    driver.find_element(By.XPATH, "//label[@class='inp adjacent-box']//input[@id='inp']").send_keys(500)
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='next-btn']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)

def test_Delete_medichine(org_login, take_screenshot):
    driver = org_login
    time.sleep(1)
    driver.find_element(By.XPATH, "//tbody/tr[1]/td[5]/div[1]/img[2]").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-view-medicine/div[2]/div/div/div/div/div/app-disable-medicine/div/div[3]/button[2]").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(2)



