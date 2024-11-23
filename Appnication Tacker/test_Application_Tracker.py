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
def userprofile():
    file_path = r"D:\pytest\login info.xlsx"
    df = pd.read_excel(file_path)
    driver = webdriver.Chrome()
    driver.maximize_window()
    url = df.iloc[0, 1]
    stm1_userid = df.iloc[4, 1]
    stm1_pass = df.iloc[4, 2]
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
    driver.find_element(By.XPATH, "//span[normalize-space()='Analytics']").click()
    time.sleep(3)
    yield driver  # Yielding the driver instance
    time.sleep(5)
    driver.quit()

@pytest.fixture
def take_screenshot(userprofile, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = userprofile
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = "D:/pytest/screenshots/analytics"

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
            screenshots_dir = "D:/pytest/screenshots/analytics"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")


def test_Population_Wellness_Score_1(userprofile, take_screenshot):
    driver = userprofile
    Population_Wellness_Score = driver.find_element(By.XPATH,"//div[@class='shadow-paper ng-star-inserted']//h3[@class='icon-heading'][normalize-space()='Population Wellness Score']").text
    assert Population_Wellness_Score == "Population Wellness Score"
    take_screenshot ()


def test_Population_Engagement_1(userprofile,take_screenshot):
    driver = userprofile
    Population_Engagement = driver.find_element(By.XPATH,"//div[@class='shadow-paper ng-star-inserted']//h3[@class='icon-heading'][normalize-space()='Population Engagement']").text
    assert Population_Engagement == "Population Engagement"
    take_screenshot ()


def test_Users(userprofile,take_screenshot):
    driver = userprofile
    Users = driver.find_element(By.XPATH,"//h3[normalize-space()='Users']").text
    assert Users == "Users"
    take_screenshot()

def test_wellness_score_Calculation(userprofile,take_screenshot):
    driver =  userprofile
    tests = driver.find_elements(By.XPATH, "//body[1]/app-root[1]/div[3]/app-population-overview[1]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/app-participants-chart[1]/div[1]/div[1]/div[1]/*[name()='svg']/*[name()='g']/*[name()='g']/*[name()='g']/*[name()='g']/*[name()='text']")
    total = 0
    for test in tests:
        text = test.text
        numbers = re.findall(r"\d+\.\d+", text)
        numbers = [float(num) for num in numbers]
        total += sum(numbers)
    assert total == 100.0
    take_screenshot()

def test_Ongoing_Challenges(userprofile,take_screenshot):
    driver = userprofile
    Ongoing_Challenges = driver.find_element(By.XPATH,"//h3[normalize-space()='Ongoing Challenges']").text
    assert Ongoing_Challenges == "Ongoing Challenges"
    take_screenshot()


def test_ongoing_Challenges_dropdown(userprofile,take_screenshot):
    driver = userprofile
    time.sleep(5)
    driver.refresh()
    driver.find_element(By.XPATH,"//div[@class='shadow-paper']//div[@class='d-flex-center-between']/div[2]/div").click()
    driver.find_element(By.XPATH,"//div[@class='dropdown black d-block open']//ul[@class='dropdown-menu']//li[1]").click()
    take_screenshot()

# Population Analysis
def test_Population_Wellness_Score_2(userprofile,take_screenshot):
    driver = userprofile
    Population_Wellness_Score = driver.find_element(By.XPATH,"//div[@class='shadow-paper']//h3[@class='icon-heading'][normalize-space()='Population Wellness Score']").text
    assert Population_Wellness_Score == "Population Wellness Score"
    take_screenshot()

def test_User_Wellness_Segment(userprofile,take_screenshot):
    driver = userprofile
    User_Wellness_Segment = driver.find_element(By.XPATH,"//h3[normalize-space()='User Wellness Segment']").text
    assert User_Wellness_Segment == "User Wellness Segment"
    take_screenshot()

def test_Population_Engagement_2(userprofile,take_screenshot):
    driver = userprofile
    Population_Engagement = driver.find_element(By.XPATH,"//h3[normalize-space()='Population Engagement']").text
    assert Population_Engagement == "Population Engagement"
    take_screenshot()

def test_Groups(userprofile,take_screenshot):
    driver = userprofile
    Groups = driver.find_element(By.XPATH,"//h3[normalize-space()='Groups']").text
    assert Groups == "Groups"
    take_screenshot()

def test_Challenges_1(userprofile,take_screenshot):
    driver = userprofile
    Challenges = driver.find_element(By.XPATH,"//h3[normalize-space()='Challenges']").text
    assert Challenges == "Challenges"
    take_screenshot()

def test_Challenges_2(userprofile,take_screenshot):
    driver = userprofile
    Challenges = driver.find_element(By.XPATH,"//h3[normalize-space()='Challenges']").text
    assert Challenges == "Challenges"
    take_screenshot()

def test_BMI_analytics(userprofile,take_screenshot):
    driver =  userprofile
    driver.find_element(By.XPATH, "//a[@id='Population Data Distribution']").click()
    bmi =  driver.find_element(By.XPATH, "//h3[normalize-space()='BMI']").text
    assert  bmi == "BMI"
    take_screenshot()

def test_waist_circumference_analytics(userprofile,take_screenshot):
    driver =  userprofile
    waist_Circumference =  driver.find_element(By.XPATH, "//h3[normalize-space()='Waist Circumference']").text
    assert  waist_Circumference  == "Waist Circumference"
    take_screenshot()

def test_High_Intensity_Exercise_analytics(userprofile,take_screenshot):
    driver =  userprofile
    High_Intensity_Exercise =  driver.find_element(By.XPATH, "//h3[normalize-space()='High-Intensity Exercise']").text
    assert  High_Intensity_Exercise == "High-Intensity Exercise"
    take_screenshot()

def test_Excess_Sedentary_Time_analytics(userprofile,take_screenshot):
    driver =  userprofile
    Excess_Sedentary_Time =  driver.find_element(By.XPATH, "//h3[normalize-space()='Excess Sedentary Time']").text
    assert  Excess_Sedentary_Time == "Excess Sedentary Time"
    take_screenshot()

def test_Steps_Time_analytics(userprofile,take_screenshot):
    driver =  userprofile
    Steps =  driver.find_element(By.XPATH, "//h3[normalize-space()='Steps']").text
    assert  Steps == "Steps"
    take_screenshot()

def test_Active_Zone_Minutes_analytics(userprofile,take_screenshot):
    driver =  userprofile
    Active_Zone_Minutes =  driver.find_element(By.XPATH, "//h3[normalize-space()='Active Zone Minutes']").text
    assert  Active_Zone_Minutes == "Active Zone Minutes"
    take_screenshot()

def test_Distance_Covered_analytics(userprofile,take_screenshot):
    driver =  userprofile
    Distance_Covered =  driver.find_element(By.XPATH, "//h3[normalize-space()='Distance Covered']").text
    assert Distance_Covered == "Distance Covered"
    take_screenshot()

def test_Sleep_analytics(userprofile,take_screenshot):
    driver =  userprofile
    Sleep =  driver.find_element(By.XPATH, "//h3[normalize-space()='Sleep']").text
    assert Sleep == "Sleep"
    take_screenshot()

def test_water_intake_analytics(userprofile,take_screenshot):
    driver =  userprofile
    water_intake =  driver.find_element(By.XPATH, "//h3[normalize-space()='Water Intake']").text
    assert water_intake == "Water Intake"
    take_screenshot()

def test_Mood_and_Stress_analytics(userprofile,take_screenshot):
    driver =  userprofile
    Mood_and_Stress =  driver.find_element(By.XPATH, "//h3[normalize-space()='Mood and Stress']").text
    assert Mood_and_Stress == "Mood and Stress"
    take_screenshot()

def test_Healthy_Diet_analytics(userprofile,take_screenshot):
    driver =  userprofile
    Healthy_Diet =  driver.find_element(By.XPATH, "//h3[normalize-space()='Healthy Diet']").text
    assert Healthy_Diet == "Healthy Diet"
    take_screenshot()

def test_Alcohol_analytics(userprofile,take_screenshot):
    driver =  userprofile
    Alcohol =  driver.find_element(By.XPATH, "//h3[normalize-space()='Alcohol']").text
    assert Alcohol == "Alcohol"
    take_screenshot()

def test_Smoking_analytics(userprofile,take_screenshot):
    driver =  userprofile
    Smoking =  driver.find_element(By.XPATH, "//h3[normalize-space()='Smoking']").text
    assert Smoking == "Smoking"
    take_screenshot()

def test_widgets(userprofile,take_screenshot):
    driver = userprofile
    driver.find_element(By.XPATH, "//img[@src='../../../assets/images/widget-setting.png']").click()
    driver.find_element(By.XPATH,"//div[@class='d-flex justify-content-between']//li[1]").click()
    driver.find_element(By.XPATH,"//div[@class='d-flex justify-content-between']//li[1]").click()
    take_screenshot()


def test_Create_Ongoing_Challenges_coustom(userprofile,take_screenshot):
    driver = userprofile
    driver.find_element(By.XPATH, "//button[normalize-space()='+ Create a New Challenge']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-type-population/form/div[1]/div/div/div/label/img").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-type-population/form/div[1]/div/div/div/ul/li[2]").click()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-type-population/form/div[2]/div").click()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details-population/form/div[1]/label/input").send_keys("Test Challenge for Testing")
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details-population/form/div[2]/textarea").send_keys("Test")
    time.sleep(1)
    # Start date
    driver.find_element(By.XPATH, "//div[@class='details-container']//div[1]//label[1]//img[1]").click()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details-population/form/div[3]/div/div/div[1]/label/nz-date-picker/div/input").clear()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details-population/form/div[3]/div/div/div[1]/label/nz-date-picker/div/input").send_keys('25 Oct 2024')
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details-population/form/div[3]/div/div/div[2]/div[2]/div/div/img").click()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details-population/form/div[3]/div/div/div[2]/div[2]/div/ul/li[1]").click()
    # End Date
    driver.find_element(By.XPATH, "//div[@class='details-container']//div[1]//label[1]//img[1]").click()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details-population/form/div[3]/div/div/div[1]/label/nz-date-picker/div/input").clear()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details-population/form/div[3]/div/div/div[1]/label/nz-date-picker/div/input").send_keys('26 Oct 2024')
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details-population/form/div[8]/div[2]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//img[@src='./assets/images/Plus Btn.png']").click()
    driver.find_element(By.XPATH, "//div[@class='add-template-goal']//div[1]//div[1]//div[1]//label[1]//img[1]").click()
    driver.find_element(By.XPATH, "//li[contains(text(),'Water intake')]").click()
    driver.find_element(By.XPATH, "//div[@class='add-preset-goal-form ng-star-inserted']//div[2]//div[1]//div[1]//label[1]//img[1]").click()
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-goals-population/div[2]/app-challenge-preset-goals-population/div/form/div[2]/div/div/ul/li").click()
    driver.find_element(By.XPATH, "//input[@id='unit']").send_keys("100")
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-goals-population/div[2]/app-challenge-preset-goals-population/div/form/div[4]/div[1]/div/label/img").click()
    driver.find_element(By.XPATH, "//li[normalize-space()='Total']").click()
    driver.find_element(By.XPATH, "//input[@id='notes']").send_keys("Drink Water")
    driver.find_element(By.XPATH, "/html/body/app-root/div[3]/app-population-overview/div[2]/div/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-goals-population/div[2]/app-challenge-preset-goals-population/div/form/div[6]/div[2]").click()
    driver.find_element(By.XPATH, "//div[@class='next-btn add-alert-btn']").click()
    take_screenshot()
    time.sleep(3)

def test_invite_Ongoing_Challenges_coustom(userprofile,take_screenshot):
    driver = userprofile
    driver.find_element(By.XPATH, "//th//span[@class='checkmark']").click()
    time.sleep(4)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='invite-btn']"))
    )
    driver.execute_script("arguments[0].click();", element)
    take_screenshot()

def test_Create_Ongoing_Challenges_template(userprofile,take_screenshot):
    driver = userprofile
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[@class='button-text min-w-112 plus']").click()
    driver.find_element(By.XPATH,"//div[@class='ng-star-inserted']//div[@class='ng-star-inserted']//div[@class='ng-star-inserted']//div[@class='ng-star-inserted']//img").click()
    driver.find_element(By.XPATH,"//div[@class='dropdown open']//li[@class='ng-star-inserted'][normalize-space()='Challenge Template']").click()
    driver.find_element(By.XPATH,"//*[@id='show-add-template']/div/div/div/div/app-add-challenge-population/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-type-population/form/div[2]/div[2]/div[2]/div[1]").click()
    driver.find_element(By.XPATH,"//form[@class='ng-pristine ng-touched ng-valid']//div[@class='next-btn'][normalize-space()='Next']").click()
    driver.find_element(By.XPATH,"//form[@class='ng-untouched ng-pristine ng-valid']//div[@class='next-btn'][normalize-space()='Next']").click()
    driver.find_element(By.XPATH, "//div[@class='next-btn add-alert-btn']").click()
    take_screenshot()


def test_invite_Ongoing_Challenges_template(userprofile,take_screenshot):
    driver = userprofile
    time.sleep(3)
    driver.find_element(By.XPATH, "//tbody/tr[1]/td[1]/label[1]/span[1]").click()
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='invite-btn']")))
    driver.execute_script("arguments[0].click();", element)
    take_screenshot ()