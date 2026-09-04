from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_valid_login():

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://example.com/login")
        driver.maximize_window()

        # Username
        wait.until(
            EC.visibility_of_element_located((By.ID, "username"))
        ).send_keys("testuser")

        # Password
        driver.find_element(By.ID, "password").send_keys("test123")

        # Login button
        wait.until(
            EC.element_to_be_clickable((By.ID, "login"))
        ).click()

        # Verify dashboard
        wait.until(
            EC.title_contains("Dashboard")
        )

        assert "Dashboard" in driver.title

    finally:
        driver.quit()
