from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def fill_form(driver,
              first="Sreeja",
              last="potham",
              email="Sreeja@gmail.com",
              phone="8897889948",
              gender="Female",
              country="India",
              state="Andhra Pradesh",
              city="Vijayawada",
              password="Sreeja@1234",
              accept_terms=True):
    driver.find_element(By.ID, "firstName").send_keys(first)
    driver.find_element(By.ID, "lastName").send_keys(last)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "phone").send_keys(phone)

    Select(driver.find_element(By.ID, "gender")).select_by_visible_text(gender)

    Select(driver.find_element(By.ID, "country")).select_by_visible_text(country)
    time.sleep(0.5)

    Select(driver.find_element(By.ID, "state")).select_by_visible_text(state)
    time.sleep(0.5)

    Select(driver.find_element(By.ID, "city")).select_by_visible_text(city)

    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "confirmPassword").send_keys(password)

    if accept_terms:
        driver.find_element(By.ID, "terms").click()

def test_negative_missing_lastname(driver):
    print("Running NEGATIVE test: Missing last name...")

    driver.find_element(By.ID, "firstName").send_keys("Sreeja")
    driver.find_element(By.ID, "email").send_keys("Sreeja@gmail.com")
    driver.find_element(By.ID, "phone").send_keys("8897889948")
    Select(driver.find_element(By.ID, "gender")).select_by_visible_text("Female")

    Select(driver.find_element(By.ID, "country")).select_by_visible_text("India")
    time.sleep(0.5)
    Select(driver.find_element(By.ID, "state")).select_by_visible_text("Andhra Pradesh")
    time.sleep(0.5)
    Select(driver.find_element(By.ID, "city")).select_by_visible_text("Vijayawada")

    driver.find_element(By.ID, "password").send_keys("Sreeja@1234")
    driver.find_element(By.ID, "confirmPassword").send_keys("Sreeja@1234")
    driver.find_element(By.ID, "terms").click()

    # Submit should be disabled
    submit_btn = driver.find_element(By.ID, "submitBtn")
    assert submit_btn.get_attribute("disabled") is not None

    # Trigger blur to show error
    driver.find_element(By.ID, "firstName").click()
    driver.find_element(By.ID, "email").click()

    # Screenshot
    driver.save_screenshot("error-state.png")
    print("✅ Negative test passed and screenshot saved: error-state.png")

def test_positive_valid_form(driver):
    print("Running POSITIVE test: Valid registration...")

    fill_form(driver)

    submit_btn = driver.find_element(By.ID, "submitBtn")
    assert submit_btn.get_attribute("disabled") is None

    submit_btn.click()

    # Wait for success msg
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "successMsg"))
    )

    driver.save_screenshot("success-state.png")
    print("✅ Positive test passed and screenshot saved: success-state.png")

if __name__ == "__main__":
    driver = setup_driver()

    # 🔥 CHANGE THIS PATH (your index.html full path)
    driver.get("C:\Users\srini\OneDrive\Desktop\frugal testing\index.html")


    time.sleep(1)

    try:
        test_negative_missing_lastname(driver)

        # Refresh page for clean test
        driver.refresh()
        time.sleep(1)

        test_positive_valid_form(driver)
        print("\n✅ ALL TESTS COMPLETED SUCCESSFULLY!")

    finally:
        time.sleep(2)
        driver.quit()