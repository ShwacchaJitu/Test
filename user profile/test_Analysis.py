import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pandas as pd
import os
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture(scope="module")
def userprofile_analysis():
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
    driver.find_element(By.XPATH, "//a[@id='Analysis']").click()
    time.sleep(3)
    yield driver  # Yielding the driver instance
    driver.quit()

@pytest.fixture
def take_screenshot(userprofile_analysis, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = userprofile_analysis
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = r"D:\Testcase\screenshots/Analysis"

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
            screenshots_dir = r"D:\Testcase\screenshots/Analysis"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_Wellness_Score(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Wellness_Score = driver.find_element(By.XPATH, "//span[@class='card-title-history'][contains(text(),'Wellness Score')]").text
    assert Wellness_Score == "Wellness Score   7 Days"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Exercise(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Exercise = driver.find_element(By.XPATH, "//span[@class='card-title-history'][contains(text(),'Exercise')]").text
    assert Exercise == "Exercise"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Exercise_Calculation(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    try:
        driver.find_element(By.XPATH,"//div[@id='exercise-enhancement-dashboard']//div[@class='no-data-message ng-star-inserted'][normalize-space()='No Data']").text
    except:
        exercise_elements = driver.find_elements(By.XPATH, "//*[@id='exercise-enhancement-dashboard']/div[2]/div[1]/div[1]/app-exercise-cirlce/div[2]/div/div/div[2]")
        Total_Exercise_data = []
        for exercise_data in exercise_elements:
            exercise_data_value = float(exercise_data.text.replace("%", ""))
            Total_Exercise_data.append(exercise_data_value)
        total_sum_Exercise_data = sum(Total_Exercise_data)
        # Using the last value from the loop for calculation
        complate_data = total_sum_Exercise_data - Total_Exercise_data[-1] if Total_Exercise_data else 0
        complate_data_rount = round(complate_data, 1)

        dashboard_exercise_sp = driver.find_element(By.XPATH, "//*[@id='exercise-enhancement-dashboard']/div[2]/div[1]/div[1]/app-exercise-cirlce/div[1]")
        dashboard_exercise_data_value = float(dashboard_exercise_sp.text.split("%")[0])

        assert total_sum_Exercise_data == 100.0 or total_sum_Exercise_data == 0.0
        assert complate_data_rount == dashboard_exercise_data_value
        time.sleep(2)
        take_screenshot()
        time.sleep(2)

def test_Activity_Classification(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Activity_Classification = driver.find_element(By.XPATH,"//span[@class='card-title-history'][normalize-space()='Activity Classification']").text
    assert Activity_Classification == "Activity Classification"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Activity_Classification_calculation(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    total_Classification = 0.0
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@id='activity-analysis-dashboard']//img[@alt='Expand']").click()
    time.sleep(2)
    elements = driver.find_elements(By.XPATH, "//*[@id='activity-analysis-dashboard']/div[2]/div/div[2]//th")
    for element in elements:
        pattern = r'\b\d+\.\d+\b'
        float_numbers = re.findall(pattern, element.text)
        if float_numbers:
            float_data = float(float_numbers[0])
            total_Classification = total_Classification + float_data
        else:
            float_data = 0.0
            total_Classification = total_Classification + float_data
    driver.find_element(By.XPATH, "//div[@id='activity-analysis-dashboard']//img[@alt='Minimize']").click()
    assert total_Classification == 100 or total_Classification == 0.0
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Sedentary_Classification(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Sedentary_Classification = driver.find_element(By.XPATH,"//span[@class='card-title-history'][normalize-space()='Sedentary Classification']").text
    assert Sedentary_Classification == "Sedentary Classification"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Sedentary_Classification_calculation(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    total_sedentary = 0.0
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@id='activity-sedentary-analysis-dashboard']//img[@alt='Expand']").click()
    time.sleep(2)
    elements = driver.find_elements(By.XPATH, "//*[@id='activity-sedentary-analysis-dashboard']/div[2]/div/div[2]//th")
    for element in elements:
        if element.text == "Total Sedentary Time NaN%":
            total_sedentary = 0.0
            break
        else:
            pattern = r'\b\d+\.\d+\b'
            float_numbers = re.findall(pattern, element.text)
            if float_numbers:
                float_data = float(float_numbers[0])
                total_sedentary = total_sedentary + float_data
            else:
                float_data = 0.0
                total_sedentary = total_sedentary + float_data
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='activity-sedentary-analysis-dashboard']/div[1]/img")))
        driver.execute_script("arguments[0].click();", element)
        # driver.find_element(By.XPATH, "//div[@id='activity-sedentary-analysis-dashboard']//img[@alt='Minimize']").click()
        assert total_sedentary == 100.0 or total_sedentary == 0.0
        time.sleep(2)
        take_screenshot()
        time.sleep(2)

def test_Status_Report_Tracker(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Status_Report_Tracker = driver.find_element(By.XPATH, "//div[normalize-space()='Status Report Tracker']").text
    assert  Status_Report_Tracker == "Status Report Tracker"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Medicine_and_Specialist_Nutrition_Intake(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Medicine_Specialist_Nutrition_Intake = driver.find_element(By.XPATH,"//span[normalize-space()='Medicine & Specialist Nutrition Intake']").text
    assert Medicine_Specialist_Nutrition_Intake == "Medicine & Specialist Nutrition Intake"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Medicine_and_Specialist_Nutrition_Intake_calculation(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    try:
        driver.find_element(By.XPATH, "//div[@class='no-data-message ng-star-inserted']")
    except:
        medicine_specialists = driver.find_elements(By.XPATH,
                                                    "//*[@id='medicine-adherence-dashboard']/div[2]/div[1]/div[1]/div/div[2]/div/div[2]")
        Total_medicine_specialist = []
        for medicine_specialist in medicine_specialists:
            medicine_specialist_value = float(medicine_specialist.text.replace("%", ""))
            Total_medicine_specialist.append(medicine_specialist_value)
            print("Total_medicine_specialist", Total_medicine_specialist)
            total_sum_medicine_specialist = sum(Total_medicine_specialist)
            taken_data = total_sum_medicine_specialist - Total_medicine_specialist[-1]  # Use the last element
            taken_data_rounded = round(taken_data, 1)
            print("taken_data_rounded", taken_data_rounded)

            dashboard_medicine_sp = driver.find_element(By.XPATH,
                                                        "//*[@id='medicine-adherence-dashboard']/div[2]/div[1]/div[1]/div/div[1]")
            dashboard_medicinedata = float(dashboard_medicine_sp.text.split()[0].replace("%", ""))  # Extract the number
            assert total_sum_medicine_specialist == 100.0 or total_sum_medicine_specialist == 0.0
            print("total_sum_medicine_specialist", total_sum_medicine_specialist)
            assert dashboard_medicinedata == taken_data_rounded
            print("dashboard_medicinedata", dashboard_medicinedata)
            print("taken_data_rounded", taken_data_rounded)
            time.sleep(2)
            take_screenshot()
            time.sleep(2)


def test_Location(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Location = driver.find_element(By.XPATH, " //div[@class='log-minimize']//span[1]//img[1]").text
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Heart_Rates(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Heart_Rates = driver.find_element(By.XPATH, "//span[normalize-space()='Heart Rates']").text
    assert Heart_Rates == "Heart Rates"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Heart_Rate_Variability(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Heart_Rate_Variability = driver.find_element(By.XPATH,"//span[@class='card-title-history'][normalize-space()='Heart Rate Variability']").text
    assert Heart_Rate_Variability == "Heart Rate Variability"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Blood_Pressure(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Blood_Pressure = driver.find_element(By.XPATH,"//span[@class='card-title-history'][normalize-space()='Blood Pressure']").text
    assert Blood_Pressure == "Blood Pressure"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Blood_Glucose(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Blood_Glucose = driver.find_element(By.XPATH,"//span[@class='card-title-history'][normalize-space()='Blood Glucose']").text
    assert Blood_Glucose == "Blood Glucose"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)


def test_Sleep_reported_and_Self_reported_SpO2_PR(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Sleep_reported_SpO2_Self_reported_SpO2_PR_bpm = driver.find_element(By.XPATH, "//span[normalize-space()='Sleep-reported SpO2 , Self-reported SpO2 & PR bpm']").text
    assert Sleep_reported_SpO2_Self_reported_SpO2_PR_bpm == "Sleep-reported SpO2 , Self-reported SpO2 & PR bpm"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Body_Shape(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Body_shape = driver.find_element(By.XPATH, "//span[@class='card-title-history'][normalize-space()='Body shape']").text
    assert Body_shape == "Body shape"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Walk(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Walk = driver.find_element(By.XPATH, "//span[normalize-space()='Walk']").text
    assert Walk == "Walk"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Floors_Climbed(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Floors_Climbed = driver.find_element(By.XPATH, "//span[normalize-space()='Floors Climbed']").text
    assert Floors_Climbed == "Floors Climbed"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Water_Intake(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Water_Intake = driver.find_element(By.XPATH, "//span[normalize-space()='Water Intake']").text
    assert Water_Intake == "Water Intake"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Sleep_Analysis_and_Breathing_Rate(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Sleep_Analysis_Breathing_Rate = driver.find_element(By.XPATH,"//span[normalize-space()='Sleep Analysis and Breathing Rate']").text
    assert Sleep_Analysis_Breathing_Rate == "Sleep Analysis and Breathing Rate"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)

def test_Lipids(userprofile_analysis, take_screenshot):
    driver = userprofile_analysis
    Lipids = driver.find_element(By.XPATH, "//span[@class='card-title-history'][normalize-space()='Lipids']").text
    assert Lipids == "Lipids"
    time.sleep(2)
    take_screenshot()
    time.sleep(2)