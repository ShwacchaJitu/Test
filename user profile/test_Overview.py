import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pandas as pd
import os
from datetime import datetime

@pytest.fixture(scope="module")
def userprofile():
    driver = webdriver.Chrome()
    driver.maximize_window()
    file_path = r"D:\pytest\login info.xlsx"
    df = pd.read_excel(file_path)
    url = df.iloc[0, 1]
    stm1_userid = df.iloc[4, 1]
    stm1_pass = df.iloc[4, 2]
    otp = df.iloc[3, 3]
    driver.get(url)
    driver.implicitly_wait(100)
    driver.find_element(By.XPATH, "//div[@class='login-form']//div[1]//label[1]").send_keys(stm1_userid)
    driver.find_element(By.XPATH, "//div[@class='divisions']//div[2]//label[1]//input[1]").send_keys(stm1_pass)
    driver.find_element(By.XPATH, "//input[@value='Sign In']").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//input[@id='inp']").send_keys(otp)
    driver.find_element(By.XPATH, "//input[@value='Submit']").click()
    user = df.iloc[10, 1]
    driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(user)
    driver.find_element(By.XPATH,"//div[@class='p-element blurry-text']").click()
    time.sleep(3)
    yield driver  # Yielding the driver instance
    time.sleep(5)
    driver.quit()

@pytest.fixture
def take_screenshot(org_login, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = org_login
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = "D:/pytest/screenshots/Overview"

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
            screenshots_dir = "D:/pytest/screenshots/Overview"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")

def test_bmi(userprofile, take_screenshot):
    driver = userprofile
    bmi = driver.find_element(By.XPATH,"//p[normalize-space()='BMI']").text
    assert bmi == bmi
    take_screenshot()
    time.sleep(1)


def test_bmi_calculation(userprofile, take_screenshot):
    driver = userprofile
    bmi_element = driver.find_element(By.XPATH, "//div[@id='profile-bmi']/p[2]").text
    weight_element = driver.find_element(By.XPATH, "//p[@id='user-weight']").text
    height_element = driver.find_element(By.XPATH, "//p[@id='user-height']").text
    if bmi_element == "--":
        assert bmi_element == weight_element and bmi_element == height_element
    else:
        bmi = float(bmi_element)
        weight = float(weight_element.split()[0])
        height = float(height_element.split()[0])
        height = height / 100
        bmi_calculation = weight / (height ** 2)
        bmi_calculation = round(bmi_calculation, 2)
        assert bmi_calculation == bmi
        take_screenshot()
        time.sleep(1)


def test_Heart_Rate(userprofile, take_screenshot):
    driver = userprofile
    try:
        element = driver.find_element(By.XPATH, f"//div[normalize-space()='Heart Rate']").text
    except:
        element = driver.find_element(By.XPATH, f"//div[normalize-space()='Resting Heart Rate']").text
    assert element == "Heart Rate" or element == "Resting Heart Rate"
    take_screenshot()
    time.sleep(1)

def test_Sleep(userprofile, take_screenshot):
    driver = userprofile
    element = driver.find_element(By.XPATH, f"//div[normalize-space()='Sleep']").text
    assert element == "Sleep"
    take_screenshot()
    time.sleep(1)

def test_Walk(userprofile, take_screenshot):
    driver = userprofile
    element = driver.find_element(By.XPATH, f"//div[normalize-space()='Walk']").text
    assert element == "Walk"
    take_screenshot()
    time.sleep(1)

def test_Floors_Climbed(userprofile, take_screenshot):
    driver = userprofile
    element = driver.find_element(By.XPATH, f"//div[normalize-space()='Floors Climbed']").text
    assert element == "Floors Climbed"
    take_screenshot()
    time.sleep(1)

def test_Blood_Pressure(userprofile, take_screenshot):
    driver = userprofile
    element = driver.find_element(By.XPATH, f"//div[normalize-space()='Blood Pressure']").text
    assert element == "Blood Pressure"
    take_screenshot()
    time.sleep(1)

def test_Blood_Glucose_and_HbA1c(userprofile, take_screenshot):
    driver = userprofile
    element = driver.find_element(By.XPATH, f"//div[normalize-space()='Blood Glucose and HbA1c']").text
    assert element == "Blood Glucose and HbA1c"
    take_screenshot()
    time.sleep(1)

def test_Wellness_Score(userprofile, take_screenshot):
    driver = userprofile
    element = driver.find_element(By.XPATH, f"//div[normalize-space()='Wellness Score']").text
    assert element == "Wellness Score"
    take_screenshot()
    time.sleep(1)

def test_wellness_Calculation(userprofile, take_screenshot):
    driver =  userprofile
    score_p_Data = driver.find_element(By.XPATH,"//*[@id='overview-dashboards']/div[2]/div[3]/app-overview-wellness-score/div/div/div[2]/div[1]/div[3]").text
    score_n_Data = driver.find_element(By.XPATH,"//*[@id='overview-dashboards']/div[2]/div[3]/app-overview-wellness-score/div/div/div[2]/div[2]/div[3]").text
    score_p_Data = int(score_p_Data.strip('%'))
    score_n_Data = int(score_n_Data.strip('%'))
    wellness_score = score_n_Data + score_p_Data
    assert wellness_score == 100
    take_screenshot()
    time.sleep(1)


def test_Schedule(userprofile, take_screenshot):
    driver = userprofile
    element = driver.find_element(By.XPATH, f"//div[normalize-space()='Schedule']").text
    assert element == "Schedule"
    take_screenshot()
    time.sleep(1)

def test_Schedule_calculation(userprofile, take_screenshot):
    driver = userprofile
    dashboard_schedule = float(driver.find_element(By.CSS_SELECTOR, "div[class='highcharts-label highcharts-data-label highcharts-data-label-color-0 highcharts-tracker'] div:nth-child(2)").text.replace("%", ""))
    schedule_elements = driver.find_elements(By.XPATH, "//*[@id='overview-dashboards']/div[2]/div[4]/app-overall-status/div/div/div[2]/div/div/div/span[1]")
    total_schedule_data = [float(element.text.replace("%", "")) for element in schedule_elements if element.text.strip() != '--']
    assert dashboard_schedule == sum(total_schedule_data)
    take_screenshot()
    time.sleep(1)


def test_Vital_Signs_from_Most_Recent_Sleep(userprofile, take_screenshot):
    driver = userprofile
    element = driver.find_element(By.XPATH, f"//div[normalize-space()='Vital Signs from Most Recent Sleep']").text
    assert element == "Vital Signs from Most Recent Sleep"
    take_screenshot()
    time.sleep(1)

def test_Activity_and_Sedentary_Classification(userprofile, take_screenshot):
    driver = userprofile
    element = driver.find_element(By.XPATH, f"//div[normalize-space()='Activity and Sedentary Classification']").text
    assert element == "Activity and Sedentary Classification"
    take_screenshot()
    time.sleep(1)


def test_Activity_and_Sedentary_Classification_calculation(userprofile, take_screenshot):
    driver = userprofile
    activity_sedentarys = driver.find_elements(By.XPATH, "//*[@id='overview-dashboards']/div[2]/div[6]/app-activity-overview/div/div[3]/div/div[3]")
    sedentarytime = driver.find_element(By.XPATH, "//*[@id='overview-dashboards']/div[2]/div[6]/app-activity-overview/div/div[4]/div[1]/div[3]")
    data_without_percent = float(sedentarytime.text.replace("%", ""))
    total_activity = [data_without_percent]
    for activity_sedentary in activity_sedentarys:
        data_without_percent_activity = float(activity_sedentary.text.replace("%", ""))
        total_activity.append(data_without_percent_activity)
    total_sum = sum(total_activity)
    assert total_sum == 100.0 or total_sum == 0.0
    take_screenshot()
    time.sleep(1)


def test_Lipids(userprofile, take_screenshot):
    driver = userprofile
    element = driver.find_element(By.XPATH, f"//div[normalize-space()='Lipids']").text
    assert element == "Lipids"
    take_screenshot()
    time.sleep(1)

def test_Geolocation(userprofile, take_screenshot):
    driver = userprofile
    element = driver.find_element(By.XPATH, f"//div[normalize-space()='Geolocation']").text
    assert element == "Geolocation"
    take_screenshot()
    time.sleep(1)

def test_Status_Report_Tracker(userprofile, take_screenshot):
    driver = userprofile
    element = driver.find_element(By.XPATH, f"//div[normalize-space()='Status Report Tracker']").text
    assert element == "Status Report Tracker"
    take_screenshot()
    time.sleep(1)