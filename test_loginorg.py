import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://example.com/login"


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# 1. Valid Login
def test_valid_login(driver):

    driver.get(BASE_URL)

    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("test123")

    driver.find_element(By.ID, "login").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("dashboard")
    )

    assert "dashboard" in driver.current_url.lower()


# 2. Invalid Username
def test_invalid_username(driver):

    driver.get(BASE_URL)

    driver.find_element(By.ID, "username").send_keys("wronguser")
    driver.find_element(By.ID, "password").send_keys("test123")

    driver.find_element(By.ID, "login").click()

    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "error-message")
        )
    )

    assert error.is_displayed()


# 3. Invalid Password
def test_invalid_password(driver):

    driver.get(BASE_URL)

    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("wrongpassword")

    driver.find_element(By.ID, "login").click()

    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "error-message")
        )
    )

    assert error.is_displayed()


# 4. Empty Username
def test_empty_username(driver):

    driver.get(BASE_URL)

    driver.find_element(By.ID, "password").send_keys("test123")
    driver.find_element(By.ID, "login").click()

    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "username-error")
        )
    )

    assert error.is_displayed()


# 5. Empty Password
def test_empty_password(driver):

    driver.get(BASE_URL)

    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "login").click()

    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "password-error")
        )
    )

    assert error.is_displayed()


# 6. Both Fields Empty
def test_empty_login(driver):

    driver.get(BASE_URL)

    driver.find_element(By.ID, "login").click()

    username_error = driver.find_element(
        By.ID, "username-error"
    )

    password_error = driver.find_element(
        By.ID, "password-error"
    )

    assert username_error.is_displayed()
    assert password_error.is_displayed()
