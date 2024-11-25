import pytest
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
from datetime import datetime


@pytest.fixture(scope="module")
def application_tacker():
    file_path = r"D:\userinfo\login info.xlsx"
    df = pd.read_excel(file_path)
    driver = webdriver.Chrome()
    driver.maximize_window()
    url = df.iloc[0, 1]
    stm1_userid = df.iloc[1, 1]
    stm1_pass = df.iloc[1, 2]
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, "//div[@class='login-form']//div[1]//label[1]").send_keys(stm1_userid)
    driver.find_element(By.XPATH, "//div[@class='divisions']//div[2]//label[1]//input[1]").send_keys(stm1_pass)
    driver.find_element(By.XPATH, "//input[@value='Sign In']").click()
    time.sleep(3)
    otp = 111222
    driver.find_element(By.XPATH, "//input[@id='inp']").send_keys(otp)
    driver.find_element(By.XPATH, "//input[@value='Submit']").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//span[normalize-space()='Application Tracker']").click()
    time.sleep(3)
    yield driver  # Yielding the driver instance
    time.sleep(5)
    driver.quit()

@pytest.fixture
def take_screenshot(application_tacker, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = application_tacker
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = "D:\Testcase\screenshots\Application_Tracker"

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
            screenshots_dir = "D:\Testcase\screenshots\Application_Tracker"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_click_history_datepicker(application_tacker, take_screenshot):
    driver = application_tacker
    driver.find_element(By.XPATH, "//input[@id='history-datepicker']").click()
    time.sleep(2)
    take_screenshot()

def test_click_dropdown_multiselect(application_tacker, take_screenshot):
    driver = application_tacker
    driver.find_element(By.XPATH, "//span[@class='dropdown-multiselect__caret']").click()
    time.sleep(2)
    take_screenshot()

def test_click_reset_button(application_tacker, take_screenshot):
    driver = application_tacker
    driver.find_element(By.XPATH, "//button[@class='btn btn-primary reset-button']").click()
    time.sleep(2)
    take_screenshot()

def test_click_active_tab(application_tacker, take_screenshot):
    driver = application_tacker
    driver.find_element(By.XPATH, "//a[@class='tab active']").click()
    time.sleep(2)
    take_screenshot()

def test_open_exception_alerting(application_tacker, take_screenshot):
    driver = application_tacker
    driver.find_element(By.XPATH, "//a[normalize-space()='Exception Alerting']").click()
    time.sleep(2)
    take_screenshot()

# def test_open_exception_alerting_filter(application_tacker):
#     driver = application_tacker
#     driver.find_element(By.XPATH, "//button[normalize-space()='Filter']").click()
#     driver.find_element(By.XPATH, "//input[@formcontrolname='userId']").send_keys("User1")
#     driver.find_element(By.XPATH, "//input[@formcontrolname='eventType']").send_keys("Type 1")
#     driver.find_element(By.XPATH, "//input[@formcontrolname='action']").send_keys("Null")
#     driver.find_element(By.XPATH, "//button[@type='submit']").click()

def test_exception_alerting_sort(application_tacker, take_screenshot):
    driver = application_tacker
    driver.find_element(By.XPATH, "//button[normalize-space()='Sort']").click()
    driver.find_element(By.XPATH, "//body[1]/app-root[1]/div[3]/app-application-tracker[1]/div[2]/div[1]/div[2]/app-exception-alerting[1]/div[1]/div[1]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[7]/button[1]").click()
    time.sleep(2)
    take_screenshot()

def test_open_engagements(application_tacker, take_screenshot):
    driver = application_tacker
    driver.find_element(By.XPATH, "//a[normalize-space()='Engagements']").click()
    time.sleep(3)
    take_screenshot()

def test_get_active_users_today(application_tacker, take_screenshot):
    driver = application_tacker
    active_users_today = driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-application-tracker/div[2]/div/div[2]/app-overview/div[2]/div[1]/app-active-users-today//h3[1]").text
    assert active_users_today == "Active Users - Today"
    time.sleep(2)
    take_screenshot()

def test_get_active_users_today_alternate(application_tacker, take_screenshot):
    driver = application_tacker
    active_users_today = driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-application-tracker/div[2]/div/div[2]/app-overview/div[2]/div[1]/app-active-user-today//h3").text
    assert active_users_today == "Active Users - Today"
    time.sleep(2)
    take_screenshot()

def test_get_active_users_by_city(application_tacker, take_screenshot):
    driver = application_tacker
    active_users_by_city = driver.find_element(By.XPATH, "//h3[normalize-space()='Active Users - By City']").text
    assert active_users_by_city == "Active Users - By City"
    time.sleep(2)
    take_screenshot()

def test_get_active_users_by_country(application_tacker, take_screenshot):
    driver = application_tacker
    active_users_by_country = driver.find_element(By.XPATH, "//h3[normalize-space()='Active Users - By Country']").text
    assert active_users_by_country == "Active Users - By Country"
    time.sleep(2)
    take_screenshot()

def test_get_retention_info(application_tacker, take_screenshot):
    driver = application_tacker
    retention = driver.find_element(By.XPATH, "//h3[normalize-space()='Retention - How many user return each week']").text
    assert retention == "Retention - How many user return each week"
    time.sleep(2)
    take_screenshot()

def test_get_date_wise_compare_sessions(application_tacker, take_screenshot):
    driver = application_tacker
    date_wise_compare_sessions = driver.find_element(By.XPATH, "//h3[normalize-space()='Date wise Compare the sessions']").text
    assert date_wise_compare_sessions == "Date wise Compare the sessions"
    time.sleep(2)
    take_screenshot()

def test_get_event_wise_total_sessions(application_tacker, take_screenshot):
    driver = application_tacker
    event_wise_total_sessions = driver.find_element(By.XPATH, "//h3[normalize-space()='Event Wise - Total Sessions']").text
    assert event_wise_total_sessions == "Event Wise - Total Sessions"
    time.sleep(2)
    take_screenshot()

def test_mobile_option(application_tacker, take_screenshot):
    driver = application_tacker
    driver.find_element(By.XPATH,"//a[@id='mobile-option']").click()
    time.sleep(2)
    take_screenshot()