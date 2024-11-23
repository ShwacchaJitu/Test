import pytest
import time
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime


@pytest.fixture(scope="module")
def stm_login():
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
    time.sleep(5)
    driver.find_element(By.XPATH, "//input[@id='inp']").send_keys(otp)
    driver.find_element(By.XPATH, "//input[@value='Submit']").click()
    time.sleep(5)
    yield driver
    time.sleep(5)
    driver.quit()

@pytest.fixture
def take_screenshot(stm_login, request):
    """Fixture to capture a screenshot at specific points in the test."""
    driver = stm_login
    test_name = request.node.name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshots_dir = "D:/pytest/screenshots/challenge"

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
        driver = item.funcargs.get('stm_login')
        if driver:
            test_name = item.name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshots_dir = "D:/pytest/screenshots/challenge"
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{test_name}_failed_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(file_path)
            print(f"Screenshot for failed test saved at {file_path}")

def test_challenge_page(stm_login, take_screenshot):
    driver = stm_login
    driver.find_element(By.XPATH, "//span[normalize-space()='Programme Management']").click()
    driver.find_element(By.XPATH, "//a[normalize-space()='Challenges']").click()
    time.sleep(2)
    take_screenshot()
    time.sleep(1)


def test_create_coustom_challenge(stm_login, take_screenshot):
    driver = stm_login
    fake = Faker()
    fake = Faker()
    global challenge_name
    challenge_name = fake.name()
    description = fake.sentence()
    unit = fake.random_number(2)
    notes = fake.words()
    time.sleep(2)
    Ongoing_Challenges = driver.find_element(By.XPATH, "//div[@class='add-template-challenge-btn']").click()
    time.sleep(2)
    custom_challenge_template = driver.find_element(By.XPATH, "//img[@src='./assets/images/downarrow.png']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//li[normalize-space()='Custom Challenge']").click()
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-challenge-calender/div[3]/div/div/div/div/div/app-add-challenge/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-type/form/div[2]/div").click()
    driver.find_element(By.XPATH,"/html/body/app-root/div[3]/app-challenge-calender/div[3]/div/div/div/div/div/app-add-challenge/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details/form/div[1]/label/input").send_keys(
        challenge_name)
    time.sleep(1)
    driver.find_element(By.XPATH,
                        "/html/body/app-root/div[3]/app-challenge-calender/div[3]/div/div/div/div/div/app-add-challenge/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details/form/div[2]/textarea").send_keys(
        description)
    time.sleep(1)
    # Start date
    driver.find_element(By.XPATH,
                        "//body[1]/app-root[1]/div[3]/app-challenge-calender[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/app-add-challenge[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/app-challenge-details[1]/form[1]/div[3]/div[1]/div[1]/div[1]/label[1]/img[1]").click()
    driver.find_element(By.XPATH,
                        "/html/body/app-root/div[3]/app-challenge-calender/div[3]/div/div/div/div/div/app-add-challenge/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details/form/div[3]/div/div/div[1]/label/nz-date-picker/div/input").clear()
    driver.find_element(By.XPATH,
                        "/html/body/app-root/div[3]/app-challenge-calender/div[3]/div/div/div/div/div/app-add-challenge/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details/form/div[3]/div/div/div[1]/label/nz-date-picker/div/input").send_keys(
        '30 Oct 2024')
    time.sleep(1)
    driver.find_element(By.XPATH,
                        "/html/body/app-root/div[3]/app-challenge-calender/div[3]/div/div/div/div/div/app-add-challenge/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details/form/div[3]/div/div/div[2]/div/div/div/img").click()
    driver.find_element(By.XPATH,
                        "//*[@id='add-template']/div/div/div/div/app-add-challenge/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details/form/div[3]/div/div/div[2]/div/div/ul/li[1]").click()
    # End Date
    driver.find_element(By.XPATH,
                        "//body[1]/app-root[1]/div[3]/app-challenge-calender[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/app-add-challenge[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/app-challenge-details[1]/form[1]/div[3]/div[1]/div[1]/div[1]/label[1]/img[1]").click()
    driver.find_element(By.XPATH,
                        "/html/body/app-root/div[3]/app-challenge-calender/div[3]/div/div/div/div/div/app-add-challenge/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details/form/div[3]/div/div/div[1]/label/nz-date-picker/div/input").clear()
    driver.find_element(By.XPATH,
                        "/html/body/app-root/div[3]/app-challenge-calender/div[3]/div/div/div/div/div/app-add-challenge/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-details/form/div[3]/div/div/div[1]/label/nz-date-picker/div/input").send_keys(
        '30 Oct 2024')
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='next-btn']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//img[@src='./assets/images/Plus Btn.png']").click()
    driver.find_element(By.XPATH,
                        "//body[1]/app-root[1]/div[3]/app-challenge-calender[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/app-add-challenge[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/app-template-goals[1]/div[2]/app-template-preset-goal[1]/div[1]/form[1]/div[1]/div[1]/div[1]/label[1]/img[1]").click()
    driver.find_element(By.XPATH,
                        "//*[@id='add-template']/div/div/div/div/app-add-challenge/div/div/div[2]/div[2]/div/div/div[2]/app-template-goals/div[2]/app-template-preset-goal/div/form/div[1]/div[1]/div/ul/li[4]").click()
    driver.find_element(By.XPATH,
                        "//div[@class='add-preset-goal-form ng-star-inserted']//div[2]//div[1]//div[1]//label[1]//img[1]").click()
    driver.find_element(By.XPATH, "//li[normalize-space()='Water Intake']").click()
    driver.find_element(By.XPATH, "//input[@id='unit']").send_keys(unit)
    driver.find_element(By.XPATH, "//div[4]//div[1]//div[1]//label[1]//input[1]").click()
    driver.find_element(By.XPATH,
                        "//*[@id='add-template']/div/div/div/div/app-add-challenge/div/div/div[2]/div[2]/div/div/div[2]/app-template-goals/div[2]/app-template-preset-goal/div/form/div[4]/div[1]/div/ul/li[1]").click()
    driver.find_element(By.XPATH, "//input[@id='notes']").send_keys(notes)
    driver.find_element(By.XPATH,
                        "/html/body/app-root/div[3]/app-challenge-calender/div[3]/div/div/div/div/div/app-add-challenge/div/div/div[2]/div[2]/div/div/div[2]/app-template-goals/div[2]/app-template-preset-goal/div/form/div[6]/div[2]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[@class='next-btn add-alert-btn']").click()
    time.sleep(2)
    text = driver.find_element(By.XPATH, "//button[normalize-space()='Participants']").text
    assert text == "Participants"
    time.sleep(2)
    take_screenshot()
    time.sleep(1)


def test_assign_custom_challenge(stm_login, take_screenshot):
    driver = stm_login
    driver.find_element(By.XPATH, "//tbody/tr[1]/td[1]/label[1]/span[1]").click()
    time.sleep(2)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='invite-btn']")))
    driver.execute_script("arguments[0].click();", element)
    time.sleep(3)
    take_screenshot()
    time.sleep(1)


def test_create_template_challenge(stm_login, take_screenshot):
    driver = stm_login
    driver.refresh()
    driver.find_element(By.XPATH, "//div[@class='add-template-challenge-btn']").click()
    driver.find_element(By.XPATH, "//img[@src='./assets/images/downarrow.png']").click()
    driver.find_element(By.XPATH, "//li[contains(text(),'Challenge Template')]").click()
    driver.find_element(By.XPATH,
                        "//*[@id='add-template']/div/div/div/div/app-add-challenge/div/div/div[2]/div[2]/div/div/div[2]/app-challenge-type/form/div[2]/div[2]/div[2]/div").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[@class='next-btn']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='next-btn']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='next-btn add-alert-btn']").click()
    text = driver.find_element(By.XPATH, "//button[normalize-space()='Participants']").text
    assert text == "Participants"
    time.sleep(3)
    take_screenshot()
    time.sleep(1)


def test_assign_template_challenge(stm_login, take_screenshot):
    driver = stm_login
    driver.find_element(By.XPATH, "//tbody/tr[1]/td[1]/label[1]/span[1]").click()
    time.sleep(2)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='invite-btn']")))
    driver.execute_script("arguments[0].click();", element)
    time.sleep(2)
    take_screenshot()
    time.sleep(1)
