import os
import pandas as pd
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from faker import Faker
import re
from datetime import datetime


@pytest.fixture(scope="module")
def userprofile_Alerts_nudge():
    driver = webdriver.Chrome()
    driver.maximize_window()
    file_path = r"D:\userinfo\login info.xlsx"
    df = pd.read_excel(file_path)
    url = df.iloc[0, 1]
    stm1_userid = df.iloc[4, 1]
    stm1_pass = df.iloc[4, 2]
    otp = df.iloc[4, 3]
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
    screenshots_dir = r"D:\Testcase\screenshots/alerts_Nudge"

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
            screenshots_dir = r"D:\Testcase\screenshots/alerts_Nudge"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_assign_nudge_or_alerts(userprofile_Alerts_nudge, take_screenshot):
    driver = userprofile_Alerts_nudge
    fake = Faker()
    global description
    description = fake.sentence()
    driver.find_element(By.XPATH, "//a[@id='Alerts/Nudges']").click()
    driver.find_element(By.XPATH, "//div[@class='invite-new-patient-btn ng-star-inserted']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//body[1]/app-root[1]/div[3]/app-profile[1]/div[1]/div[2]/div[1]/app-alerts[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/app-add-alerts[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/app-alert-templates[1]/form[1]/div[1]/div[2]/label[1]/span[1]").click()
    driver.find_element(By.XPATH, "//*[@id='add-alert']/div/div/div/div/app-add-alerts/div/div/div[2]/div[2]/div/div/div[2]/app-alert-templates/form/div[2]/div[2]/div[2]/app-template-item[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='next-btn']").click()
    driver.find_element(By.XPATH, "//textarea[@id='description']").clear()
    driver.find_element(By.XPATH, "//textarea[@id='description']").send_keys(description)
    driver.find_element(By.XPATH, "//div[@class='next-btn']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-alerts/div[2]/div/div/div/div/div/app-add-alerts/div/div/div[2]/div[2]/div/div/div[2]/app-alert-messages/div[3]/div[2]").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(2)

def test_edit_nudge_or_alerts(userprofile_Alerts_nudge, take_screenshot):
    driver = userprofile_Alerts_nudge
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-alerts/div[1]/div[2]/div[1]/div[2]/input").send_keys(description)
    driver.find_element(By.XPATH, "//img[@src='../../../assets/images/edit.png']").click()
    time.sleep(1)
    fake = Faker()
    global new_template_name
    new_template_name = fake.name()
    driver.find_element(By.XPATH, "//input[@id='name']").clear()
    driver.find_element(By.XPATH,"//input[@id='name']").send_keys(new_template_name)
    driver.find_element(By.XPATH, "//img[@src='./assets/images/downarrow.png']").click()
    driver.find_element(By.XPATH,"//span[normalize-space()='Scheduled']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='next-btn']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//img[@src='./assets/images/edit.png']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//img[@src='./assets/images/downarrow.png']").click()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-alerts/div[2]/div/div/div/div/div/app-edit-alerts/div/div/div[2]/div[2]/div/div[2]/app-alert-messages/div[1]/div/div[2]/app-alert-message/div/form/div[1]/div/div/ul/li[2]/label/span").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-alerts/div[2]/div/div/div/div/div/app-edit-alerts/div/div/div[2]/div[2]/div/div[2]/app-alert-messages/div[1]/div/div[2]/app-alert-message/div/form/div[4]/div/button[2]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-profile/div[1]/div[2]/div/app-alerts/div[2]/div/div/div/div/div/app-edit-alerts/div/div/div[2]/div[2]/div/div[2]/app-alert-messages/div[3]/div[2]").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(2)


def test_remove_nudge_or_alerts(userprofile_Alerts_nudge, take_screenshot):
    driver = userprofile_Alerts_nudge
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys(new_template_name)
    time.sleep(1)
    driver.find_element(By.XPATH, "//img[@src='../../../assets/images/delete.png']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[normalize-space()='Delete Alert/Nudge']").click()
    time.sleep(3)
    take_screenshot()
    time.sleep(4)
    driver.find_element(By.XPATH, "//img[@title='Refresh']").click()
    time.sleep(2)