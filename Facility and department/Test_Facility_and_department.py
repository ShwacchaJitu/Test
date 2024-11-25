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
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, "//div[@class='login-form']//div[1]//label[1]").send_keys(org_userid)
    driver.find_element(By.XPATH, "//div[@class='divisions']//div[2]//label[1]//input[1]").send_keys(org_pass)
    driver.find_element(By.XPATH, "//input[@value='Sign In']").click()
    time.sleep(5)
    otp = 111222
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
    screenshots_dir = r"D:\Testcase\screenshots/Facility_and_department"

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
            screenshots_dir = r"D:\Testcase\screenshots/Facility_and_department"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_Create_Facility(org_login, take_screenshot):
    driver = org_login
    time.sleep(2)
    take_screenshot()


def test_Create_Facility(org_login, take_screenshot):
    driver = org_login
    fake = Faker()
    global facility_name
    facility_name = fake.name()
    facility_address = fake.address()
    driver.find_element(By.XPATH, "//button[normalize-space()='+ Add New Facility']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//div[@id='edit-department']//div[@class='content-body']//div[1]//label[1]//input[1]").send_keys(facility_name)
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[2]/div[1]/div/div/div/div/"
                                 "app-facility-operations/div/div[2]/div/form/div[2]/label/input").send_keys(facility_address)
    time.sleep(3)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[2]/div[1]/div/div/div/div/"
                                 "app-facility-operations/div/div[2]/div/form/div[3]/div").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-organization-view/div[1]/div[1]/img").click()
    time.sleep(4)

def test_create_Department(org_login, take_screenshot):
    driver = org_login
    fake = Faker()
    global department_name
    department_name = fake.name()
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[1]/div[3]/div[1]/div[2]/span[2]/button").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[@class='close-dept']//div//label[@class='inp']//input[@id='inp']").send_keys(department_name)
    driver.find_element(By.XPATH, "//img[@src='./assets/images/downarrow.png']").click()
    facility_names = driver.find_elements(By.XPATH,"//*[@id='edit-department']/div/div/div/div/app-department-operations/div/div[2]/div/form/div[1]/div/div/div[2]/div/div/ul/li")
    for p_facility_name in facility_names:
        if p_facility_name.text == facility_name:
            p_facility_name.click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[contains(text(),'Add Department')]").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(7)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-organization-view/div[1]/div[1]/img").click()
    time.sleep(4)

def test_Search_Department(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(department_name)
    time.sleep(2)
    take_screenshot()


def test_Assign_Department(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//tr[@class='facility-row']")
    time.sleep(2)
    driver.find_element(By.XPATH, "//img[@class='collapse-btn']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[1]/div[3]/div[2]/table/tbody/tr[2]/td[4]/div/img[1]").click()
    time.sleep(3)
    driver.find_element(By.XPATH,"//div[@id='all-departMent']//div[@class='left-wrap']//div[1]//label[1]//span[1]").click()
    time.sleep(3)
    driver.find_element(By.XPATH,"//div[@class='modal-body']//div//app-assign-dept-list//button[@class='success-btn'][normalize-space()='Confirm']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(7)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-organization-view/div[1]/div[1]/img").click()
    time.sleep(4)

def test_Unassign_Department(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(department_name)
    time.sleep(2)
    driver.find_element(By.XPATH, "//img[@class='collapse-btn']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//img[@data-target='#all-departMent']").click()
    time.sleep(3)
    driver.find_element(By.XPATH,"//div[@id='all-departMent']//div[@class='left-wrap']//div[1]//label[1]//span[1]").click()
    time.sleep(3)
    driver.find_element(By.XPATH,"//div[@class='modal-body']//div//app-assign-dept-list//button[@class='success-btn'][normalize-space()='Confirm']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(7)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[1]/div[1]/img").click()
    time.sleep(4)


def test_edit_Department(org_login, take_screenshot):
    driver = org_login
    fake = Faker()
    global edepartment_name
    edepartment_name = fake.name()
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(facility_name)
    time.sleep(2)
    driver.find_element(By.XPATH, "//img[@class='collapse-btn']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//tbody/tr[2]/td[4]/div[1]/img[2]").click()
    time.sleep(3)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[2]/div[1]/div/div/div/div/app-department-operations/div/div[2]/div/form/div[1]/label/input").clear()
    time.sleep(3)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[2]/div[1]/div/div/div/div/app-department-operations/div/div[2]/div/form/div[1]/label/input").send_keys(edepartment_name)
    time.sleep(3)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[2]/div[1]/div/div/div/div/app-department-operations/div/div[2]/div/form/div[2]/div/div/div/img").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[2]/div[1]/div/div/div/div/app-department-operations/div/div[2]/div/form/div[2]/div/div/ul/li[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[2]/div[1]/div/div/div/div/app-department-operations/div/div[2]/div/form/div[3]/div").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(7)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-organization-view/div[1]/div[1]/img").click()
    time.sleep(4)

def test_delete_Department(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(edepartment_name)
    time.sleep(2)
    driver.find_element(By.XPATH, "//img[@class='collapse-btn']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//tbody/tr[2]/td[4]/div[1]/img[3]").click()
    time.sleep(3)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[4]/div/div/div/div/div[3]/button[2]").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(7)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-organization-view/div[1]/div[1]/img").click()
    time.sleep(4)

def test_Refresh_facility(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(2)
    take_screenshot()

def test_Search_facility(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(facility_name)
    time.sleep(2)
    take_screenshot()

def test_Assign_facility(org_login, take_screenshot):
    driver = org_login
    time.sleep(2)
    driver.find_element(By.XPATH, "//img[@src='./assets/images/assign.png']").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[@id='all-facility']//div[@class='left-wrap']//div[1]//label[1]//span[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[10]/div[1]/div/div/div/div/app-assign-facility-list/div/div[4]/button").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(5)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-organization-view/div[1]/div[1]/img").click()
    time.sleep(4)

def test_Unassign_facility(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(facility_name)
    time.sleep(2)
    driver.find_element(By.XPATH, "//img[@src='./assets/images/assign.png']").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[@id='all-facility']//div[@class='left-wrap']//div[1]//label[1]//span[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[10]/div[1]/div/div/div/div/app-assign-facility-list/div/div[4]/button").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(5)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-organization-view/div[1]/div[1]/img").click()
    time.sleep(4)

def test_Edit_facility(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(facility_name)
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[4]/div/img[2]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[2]/div[1]/div/div/div/div/app-facility-operations/div/div[2]/div/form/div[1]/label/input").clear()
    time.sleep(2)
    fake = Faker()
    global efacility_name
    efacility_name = fake.name()
    facility_address = fake.address()
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[2]/div[1]/div/div/div/div/app-facility-operations/div/div[2]/div/form/div[1]/label/input").send_keys(efacility_name)
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[2]/div[1]/div/div/div/div/app-facility-operations/div/div[2]/div/form/div[2]/label/input").clear()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[2]/div[1]/div/div/div/div/app-facility-operations/div/div[2]/div/form/div[2]/label/input").send_keys(facility_address)
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[2]/div[1]/div/div/div/div/app-facility-operations/div/div[2]/div/form/div[3]/div").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(5)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-organization-view/div[1]/div[1]/img").click()
    time.sleep(4)

def test_delete_facility(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(efacility_name)
    time.sleep(2)
    driver.find_element(By.XPATH,"//img[@src='./assets/images/delete.png']").click()
    time.sleep(3)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-organization-view/div[3]/div/div/div/div/div[3]/button[2]").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(5)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-organization-view/div[1]/div[1]/img").click()
    time.sleep(4)


