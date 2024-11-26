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
    driver = webdriver.Chrome()
    driver.maximize_window()
    file_path = r"D:\userinfo\login info.xlsx"
    df = pd.read_excel(file_path)
    url = df.iloc[0, 1]
    org_userid = df.iloc[1, 1]
    org_pass = df.iloc[1, 2]
    driver.get(url)
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, "//div[@class='login-form']//div[1]//label[1]").send_keys(org_userid)
    driver.find_element(By.XPATH, "//div[@class='divisions']//div[2]//label[1]//input[1]").send_keys(org_pass)
    driver.find_element(By.XPATH, "//input[@value='Sign In']").click()
    time.sleep(5)
    otp = df.iloc[1, 3]
    driver.find_element(By.XPATH, "//input[@id='inp']").send_keys(otp)
    driver.find_element(By.XPATH, "//input[@value='Submit']").click()
    time.sleep(2)
    yield driver  # Yielding the driver instance
    time.sleep(5)
    driver.quit()

@pytest.fixture
def take_screenshot(org_login, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = org_login
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = r"D:\Testcase\screenshots\clinician"

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
            screenshots_dir = r"D:\Testcase\screenshots\clinician"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_stm_page(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//span[normalize-space()='Organisation']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//*[@id='admin']/ul/li[4]").click()
    time.sleep(2)
    take_screenshot()

def test_create_stm(org_login, take_screenshot):
    driver = org_login
    fake = Faker('en_GB')  # Specify 'en_GB' for UK locale
    global first_name
    first_name = fake.first_name()
    last_name = fake.last_name()
    specialization = fake.job()
    email = fake.email()
    random_number = fake.random_number(digits=8)
    if len(str(random_number)) < 8:
        extra_digit = fake.random_number(digits=1)
        phone = str(random_number) + str(extra_digit)
        phone = "+4474" + phone
    else:
        phone = "+4474" + str(random_number)
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[@class='add-patient-btn']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//body/app-root[@class='app-main']/div[@class='mainBody']/app-admin/div[@class='ack-modal']/div[@id='add-doctor']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-body']/div/app-add-doctor/div[@class='add-patient-container']/div[@class='body-wrap']/div[@class='right-content-wrap']/div/form[@class='ng-untouched ng-invalid ng-dirty']/div[1]/div[2]/div[1]/label[1]/input[1]").send_keys(email)
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "next-btn").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='content-body']//div[1]//label[1]//input[1]").send_keys(first_name)
    driver.find_element(By.XPATH, "//div[@class='content-body']//div[2]//label[1]//input[1]").send_keys(last_name)
    driver.find_element(By.XPATH, "//div[@class='content-body']//div[3]//label[1]//input[1]").send_keys(specialization)
    driver.find_element(By.XPATH, "//span[@class='ng-arrow-wrapper']").click()
    driver.find_element(By.XPATH, "//input[@placeholder='search country']").send_keys("United Kingdom")
    driver.find_element(By.XPATH, "//input[@placeholder='search country']").send_keys(Keys.ENTER)
    driver.find_element(By.XPATH, "//input[@id='phone']").send_keys(phone)
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='next-btn']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//*[@id='add-doctor']/div/div/div/div/app-add-doctor/div[1]/div[2]/div[2]/div/form/div[2]/div[2]/div[1]/label[1]").click()
    driver.find_element(By.XPATH,"//*[@id='add-doctor']/div/div/div/div/app-add-doctor/div[1]/div[2]/div[2]/div/form/div[2]/div[2]/div[2]/label[1]").click()
    driver.find_element(By.XPATH,"//*[@id='add-doctor']/div/div/div/div/app-add-doctor/div[1]/div[2]/div[2]/div/form/div[2]/div[2]/div[3]/label[1]").click()
    driver.find_element(By.XPATH,"//*[@id='add-doctor']/div/div/div/div/app-add-doctor/div[1]/div[2]/div[2]/div/form/div[2]/div[2]/div[4]/label[1]").click()
    driver.find_element(By.XPATH,"//*[@id='add-doctor']/div/div/div/div/app-add-doctor/div[1]/div[2]/div[2]/div/form/div[2]/div[2]/div[5]/label[1]").click()
    driver.find_element(By.XPATH,"//*[@id='add-doctor']/div/div/div/div/app-add-doctor/div[1]/div[2]/div[2]/div/form/div[2]/div[2]/div[6]/label[1]").click()
    driver.find_element(By.XPATH,"//*[@id='add-doctor']/div/div/div/div/app-add-doctor/div[1]/div[2]/div[2]/div/form/div[2]/div[2]/div[7]/label[1]").click()
    driver.find_element(By.XPATH,"//*[@id='add-doctor']/div/div/div/div/app-add-doctor/div[1]/div[2]/div[2]/div/form/div[2]/div[2]/div[8]/label[1]").click()
    driver.find_element(By.XPATH,"//*[@id='add-doctor']/div/div/div/div/app-add-doctor/div[1]/div[2]/div[2]/div/form/div[2]/div[2]/div[9]/label[1]").click()
    driver.find_element(By.XPATH, "//div[10]//div[2]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//*[@id='add-doctor']/div/div/div/div/app-add-doctor/div[1]/div[2]/div[2]/div/form/div[2]/div[2]/div[1]/label[1]").click()
    driver.find_element(By.XPATH,"//body/app-root[@class='app-main']/div[@class='mainBody']/app-admin/div[@class='ack-modal']/div[@id='add-doctor']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-body']/div/app-add-doctor/div[@class='add-patient-container']/div[@class='body-wrap']/div[@class='right-content-wrap']/div/form[@class='ng-invalid ng-dirty ng-touched']/div/div[@class='content-body']/div[4]/div[2]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='schedule-custom-dropdown-single']//img").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='dropdown open']//ul[@class='dropdown-menu']/li[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='schedule-custom-dropdown']//img").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='dropdown open']//ul[@class='dropdown-menu']//li[2]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[normalize-space()='Create Account']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(2)

def test_search_stm(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(first_name)
    driver.find_element(By.XPATH, "//img[@src='./assets/images/edit.png']").click()
    take_screenshot()

def test_edit_stm(org_login, take_screenshot):
    driver = org_login
    fake = Faker('en_GB')
    last_name = fake.last_name()
    specialization = fake.job()
    random_number = fake.random_number(digits=8)
    if len(str(random_number)) < 8:
        extra_digit = fake.random_number(digits=1)
        phone = str(random_number) + str(extra_digit)
        phone = "+4474" + phone
    else:
        phone = "+4474" + str(random_number)
    time.sleep(1)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-admin/div[3]/div[1]/div/div/div/div/app-edit-doctor/div[1]/div[2]/div[2]/form/div[1]/div[2]/label/input").clear()
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-admin/div[3]/div[1]/div/div/div/div/app-edit-doctor/div[1]/div[2]/div[2]/form/div[1]/div[2]/label/input").send_keys(last_name)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-admin/div[3]/div[1]/div/div/div/div/app-edit-doctor/div[1]/div[2]/div[2]/form/div[1]/div[4]/label/input").clear()
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-admin/div[3]/div[1]/div/div/div/div/app-edit-doctor/div[1]/div[2]/div[2]/form/div[1]/div[4]/label/input").send_keys(specialization)
    time.sleep(2)
    driver.find_element(By.XPATH, "//span[@class='ng-arrow-wrapper']").click()
    driver.find_element(By.XPATH, "//input[@placeholder='search country']").send_keys("United Kingdom")
    driver.find_element(By.XPATH, "//input[@placeholder='search country']").send_keys(Keys.ENTER)
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@id='phone']").clear()
    driver.find_element(By.XPATH, "//input[@id='phone']").send_keys(phone)
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[normalize-space()='Unit Preferences']").click()
    driver.find_element(By.XPATH, "//label[normalize-space()='Miles (mi)']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[normalize-space()='Notification Preference']").click()
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-admin/div[3]/div[1]/div/div/div/div/app-edit-doctor/div[1]/div[2]/div[2]/form/div[2]/div/div[1]/label[2]/span").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[normalize-space()='Affiliation']").click()
    driver.find_element(By.XPATH, "//div[@class='schedule-custom-dropdown-single']//img").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"//*[@id='add-doctor']/div/div/div/div/app-edit-doctor/div[1]/div[2]/div[2]/form/div[3]/div/app-assign-care-team-facility-dept/form/div[1]/div/div/div[1]/div/div/ul/li[1]").click()
    driver.find_element(By.XPATH, "//div[@class='schedule-custom-dropdown']//img").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//*[@id='add-doctor']/div/div/div/div/app-edit-doctor/div[1]/div[2]/div[2]/form/div[3]/div/app-assign-care-team-facility-dept/form/div[1]/div/div/div[2]/div/div[1]/ul/li[2]").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-admin/div[3]/div[1]/div/div/div/div/app-edit-doctor/div[1]/div[2]/div[2]/form/div[3]/div/app-assign-care-team-facility-dept/div[2]/div").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)

def test_Refresh_stm(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(2)
    take_screenshot()


def test_delete_stm(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(first_name)
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-admin/div[1]/div[3]/div[1]/table/tbody/tr/td[7]/div/img[2]").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-admin/div[3]/div[5]/div/div/div/app-delete-user/div/div[4]/button[2]").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(2)
