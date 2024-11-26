import pytest
import time
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
from datetime import datetime


@pytest.fixture(scope="module")
def org_login():
    """Login fixture to initialize and yield a WebDriver instance."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    file_path = r"D:\userinfo\login info.xlsx"
    df = pd.read_excel(file_path)
    url = df.iloc[0, 1]
    org_userid = df.iloc[1, 1]
    org_pass = df.iloc[1, 2]
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, "//div[@class='login-form']//div[1]//label[1]").send_keys(org_userid)
    driver.find_element(By.XPATH, "//div[@class='divisions']//div[2]//label[1]//input[1]").send_keys(org_pass)
    driver.find_element(By.XPATH, "//input[@value='Sign In']").click()
    time.sleep(5)
    otp = df.iloc[1, 3]
    driver.find_element(By.XPATH, "//input[@id='inp']").send_keys(otp)
    driver.find_element(By.XPATH, "//input[@value='Submit']").click()
    time.sleep(5)
    yield driver
    time.sleep(5)
    driver.quit()


@pytest.fixture
def take_screenshot(org_login, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = org_login
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = r"D:\Testcase\screenshots/department"

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
            screenshots_dir = r"D:\Testcase\screenshots/department"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_department_page(org_login, take_screenshot):
    driver = org_login
    time.sleep(5)
    driver.find_element(By.XPATH, "//span[normalize-space()='Organisation']").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//*[@id='admin']/ul/li[3]").click()
    time.sleep(2)
    take_screenshot()  # Capture after navigating to the department page


def test_create_department(org_login, take_screenshot):
    driver = org_login
    fake = Faker('en_GB')
    global user_name, first_name
    user_name = fake.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    random_number = fake.random_number(digits=8)
    if len(str(random_number)) < 8:
        extra_digit = fake.random_number(digits=1)
        phone = str(random_number) + str(extra_digit)
        phone = "+4474" + phone
    else:
        phone = "+4474" + str(random_number)
    time.sleep(5)
    driver.find_element(By.XPATH, "//div[@class='add-patient-btn']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//div[@class='form-wrap']//label[@class='inp']//input[@id='inp']").send_keys(user_name)
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, "next-btn").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//div[@class='content-body']//div[1]//label[1]//input[1]").send_keys(first_name)
    driver.find_element(By.XPATH, "//div[@class='content-body']//div[2]//label[1]//input[1]").send_keys(last_name)
    driver.find_element(By.XPATH, "//div[@class='content-body']//div[3]//label[1]//input[1]").send_keys(email)
    driver.find_element(By.XPATH, "//span[@class='ng-arrow-wrapper']").click()
    driver.find_element(By.XPATH, "//input[@placeholder='search country']").send_keys("United Kingdom")
    driver.find_element(By.XPATH, "//input[@placeholder='search country']").send_keys(Keys.ENTER)
    driver.find_element(By.XPATH, "//input[@id='phone']").send_keys(phone)
    driver.find_element(By.XPATH, "//div[@class='next-btn']").click()
    driver.find_element(By.XPATH, "//label[@class='schedule-drop-value inp']//input[@id='inp']").click()
    driver.find_element(By.XPATH, "//div[@class='dropdown open']//ul[@class='dropdown-menu']/li[1]").click()
    driver.find_element(By.XPATH, "//div[@class='schedule-custom-dropdown']//img").click()
    driver.find_element(By.XPATH, "//div[@class='dropdown open']//ul[@class='dropdown-menu']//li[1]").click()
    driver.find_element(By.XPATH, "//div[normalize-space()='Create Account']").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(4)


def test_search_department(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(first_name)
    time.sleep(2)
    take_screenshot()  # Capture after performing search


def test_edit_department(org_login, take_screenshot):
    driver = org_login
    fake = Faker('en_GB')
    global new_first_name
    new_first_name = fake.first_name()
    last_name = fake.last_name()
    driver.find_element(By.XPATH, "//body[1]/app-root[1]/div[3]/app-department-admin-list[1]/div[1]/div[1]/div[3]/div[1]/table[1]/tbody[1]/tr[1]/td[6]/div[1]/img[1]").click()
    driver.find_element(By.XPATH, "//div[@class='content-body']//div[1]//label[1]//input[1]").clear()
    driver.find_element(By.XPATH, "//div[@class='content-body']//div[1]//label[1]//input[1]").send_keys(new_first_name)
    driver.find_element(By.XPATH, "//div[@class='content-body']//div[2]//label[1]//input[1]").clear()
    driver.find_element(By.XPATH, "//div[@class='content-body']//div[2]//label[1]//input[1]").send_keys(last_name)
    driver.find_element(By.XPATH, "//div[@class='form-wrap-nav-btn']//div[@class='next-btn'][normalize-space()='Save Changes']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//app-assign-org-facility-dept//div[@class='next-btn'][normalize-space()='Save Changes']").click()
    time.sleep(2)
    take_screenshot()  # Capture after saving changes
    time.sleep(4)

def test_ref_department(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(2)
    take_screenshot()  # Capture after clicking Refresh


def test_delete_department(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").clear()
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(new_first_name)
    driver.find_element(By.XPATH, "//body[1]/app-root[1]/div[3]/app-department-admin-list[1]/div[1]/div[1]/div[3]/div[1]/table[1]/tbody[1]/tr[1]/td[6]/div[1]/img[2]").click()
    driver.find_element(By.XPATH, "//button[@class='btn btn-primary delete-medi-btn']").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(2)
