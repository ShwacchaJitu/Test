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
    time.sleep(5)
    driver.quit()


@pytest.fixture
def take_screenshot(org_login, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = org_login
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = r"D:\Testcase\screenshots/Physiotherapy_Equipments"

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
            screenshots_dir = r"D:\Testcase\screenshots/Physiotherapy_Equipments"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_Equipments_page(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//span[normalize-space()='Programme Management']").click()
    driver.find_element(By.XPATH, "//a[normalize-space()='Physiotherapy']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[normalize-space()='Exercises']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[@id='dropdown']/ul/li[2]/a").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_create_Equipments(org_login, take_screenshot):
    driver = org_login
    fake = Faker()  # Specify 'en_GB' for UK locale
    global equipment_name
    equipment_name = fake.name()
    size = fake.random_number(1)
    weight_resistance = fake.random_number(2)
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[@class='add-patient-btn']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='form-wrap']//input[@id='inp']").send_keys(equipment_name)
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[normalize-space()='Add Specification']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='input-wrapper size']//input[@id='inp']").send_keys(size)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[normalize-space()='cm']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='dropdown-wrapper size']//li[1]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='input-wrapper weight']//input[@id='inp']").send_keys(weight_resistance)
    driver.find_element(By.XPATH, "//button[normalize-space()='kg']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='dropdown-wrapper weight']//li[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='btn']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)


def test_Search_Equipments(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(equipment_name)
    time.sleep(1)
    equipment = driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-exercise/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[1]").text
    assert equipment == equipment_name
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Refresh_Equipments(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_edit_Equipments(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//img[@src='./assets/images/edit.png']").click()
    time.sleep(2)
    fake = Faker()  # Specify 'en_GB' for UK locale
    global new_equipment_name
    new_equipment_name = fake.name()
    size = fake.random_number(1)
    weight_resistance = fake.random_number(2)
    driver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div/mat-dialog-container/div/div/app-edit-equipment/div/div/div/form/div[1]/label/input").clear()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div/mat-dialog-container/div/div/app-edit-equipment/div/div/div/form/div[1]/label/input").send_keys(new_equipment_name)
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='input-wrapper size']//input[@id='inp']").clear()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='input-wrapper size']//input[@id='inp']").send_keys(size)
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div/mat-dialog-container/div/div/app-edit-equipment/div/div/div/form/div[3]/div/div[1]/div[2]/div/button").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div/mat-dialog-container/div/div/app-edit-equipment/div/div/div/form/div[3]/div/div[1]/div[2]/div/ul/li[2]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='input-wrapper weight']//input[@id='inp']").clear()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='input-wrapper weight']//input[@id='inp']").send_keys(weight_resistance)
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div/mat-dialog-container/div/div/app-edit-equipment/div/div/div/form/div[3]/div/div[1]/div[4]/div/button").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div/mat-dialog-container/div/div/app-edit-equipment/div/div/div/form/div[3]/div/div[1]/div[4]/div/ul/li[1]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div/mat-dialog-container/div/div/app-edit-equipment/div/div/div/form/div[5]/div").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(2)

def test_delete_Equipments(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH,"//input[@placeholder='Search']").clear()
    time.sleep(2)
    driver.find_element(By.XPATH,"//input[@placeholder='Search']").send_keys(new_equipment_name)
    time.sleep(2)
    driver.find_element(By.XPATH, "//img[@src='./assets/images/delete.png']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-exercise/div/div[3]/div[1]/div/div/div/div/app-disable-exercise/div/div[3]/button[2]").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(2)





