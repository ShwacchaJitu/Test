import pytest
import time
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pandas as pd
from datetime import datetime

@pytest.fixture(scope="module")
def org_login():
    driver = webdriver.Chrome()
    driver.maximize_window()
    file_path = r"D:\pytest\login info.xlsx"
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
    screenshots_dir = "D:/pytest/screenshots/Specialised Nutrition"

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
            screenshots_dir = "D:/pytest/screenshots/Specialised Nutrition"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_Specialised_Nutrition_page(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH, "//span[normalize-space()='Programme Management']").click()
    driver.find_element(By.XPATH, "//a[normalize-space()='Specialised Nutrition']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(1)

def test_Create_Specialised_Nutrition(org_login, take_screenshot):
    driver = org_login
    fake = Faker()
    global Specialised_Nutrition
    Specialised_Nutrition = fake.name()
    brand = fake.name()
    flavor = fake.name()
    consistency = fake.name()
    stock_left = fake.random_number(2)
    strength = fake.random_number(2)
    driver.find_element(By.XPATH, "//div[@class='add-patient-btn']").click()
    time.sleep(3)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-add-nutrition/div/div/div[2]/div[2]/form/div[1]/label/input").send_keys(Specialised_Nutrition)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-add-nutrition/div/div/div[2]/div[2]/form/div[2]/label/input").send_keys(brand)
    driver.find_element(By.XPATH,"//input[@formcontrolname='flavor']").send_keys(flavor)
    driver.find_element(By.XPATH,"//label[@class='schedule-drop-value inp']//img").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//*[@id='add-nutrition']/div/div/div/div/app-add-nutrition/div/div/div[2]/div[2]/form/div[3]/div[2]/div/ul/li[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[@formcontrolname='consistency']").send_keys(consistency)
    driver.find_element(By.XPATH, "//input[@formcontrolname='stockLeft']").send_keys(stock_left)
    driver.find_element(By.XPATH, "//input[@formcontrolname='tempStrength']").send_keys(strength)
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='schedule-drop-value duration']//img").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//*[@id='add-nutrition']/div/div/div/div/app-add-nutrition/div/div/div[2]/div[2]/form/div[4]/div[2]/div/ul/li[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-add-nutrition/div/div/div[2]/div[2]/form/div[10]/div").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-add-nutrition/div/div[3]/button[2]").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-nutrition/div[1]/div[1]/img").click()
    time.sleep(2)

def test_search_Specialised_Nutrition(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH,"//input[@placeholder='Search']").send_keys(Specialised_Nutrition)
    Specialised_Nutrition_name = driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-view-nutrition/div[1]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[2]").text
    time.sleep(2)
    assert Specialised_Nutrition_name == Specialised_Nutrition
    time.sleep(1)
    take_screenshot()
    time.sleep(2)


def test_refresh_Specialised_Nutrition(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH,"//img[@title='Refresh']").click()
    take_screenshot()
    time.sleep(2)


def test_Edit_Specialised_Nutrition(org_login, take_screenshot):
    driver = org_login
    time.sleep(2)
    fake = Faker() # Specify 'en_GB' for UK locale
    global new_Specialised_Nutrition
    new_Specialised_Nutrition = fake.name()
    brand = fake.name()
    flavor = fake.name()
    consistency = fake.name()
    stock_left = fake.random_number(1)
    strength = fake.random_number(2)
    driver.find_element(By.XPATH, "//img[@src='./assets/images/edit.png']").click()
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[1]/label/input").clear()
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[1]/label/input").send_keys(new_Specialised_Nutrition)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[2]/label/input").clear()
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[2]/label/input").send_keys(brand)
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[3]/label[1]/input").clear()
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[3]/label[1]/input").send_keys(flavor)
    driver.find_element(By.XPATH,"//*[@id='add-nutrition']/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[3]/div/div[2]/div/img").click()
    driver.find_element(By.XPATH,"//*[@id='add-nutrition']/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[3]/div/div[2]/ul/li[3]").click()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[3]/label[2]/input").clear()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[3]/label[2]/input").send_keys(consistency)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[4]/label[1]/input").clear()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[4]/label[1]/input").send_keys(stock_left)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[4]/label[2]/input").clear()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[4]/label[2]/input").send_keys(strength)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[4]/div/div/div/img").click()
    driver.find_element(By.XPATH, "//*[@id='add-nutrition']/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[4]/div/div/ul/li[3]").click()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-nutrition/div[2]/div/div/div/div/div/app-edit-nutrition/div/div[2]/div/form/div[10]/div").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-nutrition/div[1]/div[1]/img").click()
    time.sleep(2)

def test_delete_Specialised_Nutrition(org_login, take_screenshot):
    driver = org_login
    driver.find_element(By.XPATH,"//input[@placeholder='Search']").send_keys(new_Specialised_Nutrition)
    time.sleep(2)
    driver.find_element(By.XPATH, "//img[@src='./assets/images/delete.png']").click()
    driver.find_element(By.XPATH, "//button[normalize-space()='Delete Specialised Nutrition']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-view-nutrition/div[1]/div[1]/img").click()
    time.sleep(2)


