import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pandas as pd
import os
from datetime import datetime

@pytest.fixture(scope="module")
def userprofile_specialist():
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
    driver.find_element(By.XPATH,"//div[@class='p-element blurry-text']").click()
    driver.find_element(By.XPATH,"//a[@id='Specialist']").click()
    time.sleep(3)
    yield driver  # Yielding the driver instance
    driver.quit()

@pytest.fixture
def take_screenshot(userprofile_specialist, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = userprofile_specialist
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = r"D:\Testcase\screenshots/Specialist"

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
            screenshots_dir = r"D:\Testcase\screenshots/Specialist"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_Avg_Stride_Length(userprofile_specialist, take_screenshot):
    driver = userprofile_specialist
    Avg_Stride_Length = driver.find_element(By.XPATH, f"//span[normalize-space()='Avg. Stride Length']").text
    assert Avg_Stride_Length == "Avg. Stride Length"
    time.sleep(2)
    take_screenshot()
    time.sleep(1)


def test_Stride_Pattern_Analysis(userprofile_specialist, take_screenshot):
    driver = userprofile_specialist
    Avg_Stride_Length = driver.find_element(By.XPATH, f"//span[normalize-space()='Stride Pattern Analysis']").text
    assert Avg_Stride_Length == "Stride Pattern Analysis"
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Stride_Duration_Analysis(userprofile_specialist, take_screenshot):
    driver = userprofile_specialist
    Stride_Duration_Analysis = driver.find_element(By.XPATH, f"//span[normalize-space()='Stride Duration Analysis']").text
    assert Stride_Duration_Analysis == "Stride Duration Analysis"
    time.sleep(2)
    take_screenshot()
    time.sleep(1)
def test_Discomfort_Level(userprofile_specialist, take_screenshot):
    driver = userprofile_specialist
    Discomfort_Level = driver.find_element(By.XPATH, f"//span[normalize-space()='Discomfort Level']").text
    assert Discomfort_Level == "Discomfort Level"
    time.sleep(2)
    take_screenshot()
    time.sleep(1)


def test_AICVD_Score(userprofile_specialist_analysis, take_screenshot):
    driver = userprofile_specialist_analysis
    AICVD_Score = driver.find_element(By.XPATH, f"//span[normalize-space()='AICVD Score']").text
    assert AICVD_Score == "AICVD Score"
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Stride_Level_Analysis(userprofile_specialist_analysis, take_screenshot):
    driver = userprofile_specialist_analysis
    Stride_Level_Analysis = driver.find_element(By.XPATH, f"//span[normalize-space()='Stride-Level Analysis']").text
    assert Stride_Level_Analysis == "Stride-Level Analysis"
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Discomfort_Level(userprofile_specialist_analysis, take_screenshot):
    driver = userprofile_specialist_analysis
    Discomfort_Level = driver.find_element(By.XPATH, f"//span[normalize-space()='Discomfort Level']").text
    assert Discomfort_Level == "Discomfort Level"
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Stride_Length(userprofile_specialist_analysis, take_screenshot):
    driver = userprofile_specialist_analysis
    Stride_Length = driver.find_element(By.XPATH, f"//span[normalize-space()='Stride Length']").text
    assert Stride_Length == "Stride Length"
    time.sleep(2)
    take_screenshot()
    time.sleep(1)

def test_Discomfort_Log(userprofile_specialist_analysis, take_screenshot):
    driver = userprofile_specialist_analysis
    Discomfort_Log = driver.find_element(By.XPATH, f"//span[normalize-space()='Discomfort Log']").text
    assert Discomfort_Log == "Discomfort Log"
    time.sleep(2)
    take_screenshot()
    time.sleep(1)