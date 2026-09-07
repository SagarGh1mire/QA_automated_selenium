"""
Complete Selenium Navigation Testing Template
Author: Sagar Ghimire

Install:
    pip install selenium pytest requests

Run:
    pytest test_navigation.py -v -s

IMPORTANT:
    Change BASE_URL and the locators/expected paths to match your website.
"""

import requests
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://example.com"
TIMEOUT = 10


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def wait_for_page(driver):
    WebDriverWait(driver, TIMEOUT).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


# 1. Test all links on the webpage.
def test_all_navigation_links(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    links = driver.find_elements(By.TAG_NAME, "a")
    valid_links = []

    for link in links:
        href = link.get_attribute("href")
        text = link.text.strip() or "[No link text]"

        if href and href.startswith(("http://", "https://")):
            valid_links.append((text, href))

    print(f"\nTotal links found: {len(valid_links)}")

    for text, href in valid_links:
        print(f"Testing: {text} -> {href}")

        driver.get(href)
        wait_for_page(driver)

        assert driver.current_url, f"Page did not load: {href}"
        print("PASS")


# 2. Test header/navbar links
def test_header_navigation(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    # Change these menu names to match your website.
    menu_items = [
        "Home",
        "About",
        "Services",
        "Contact",
        "Login",
    ]

    for menu in menu_items:
        driver.get(BASE_URL)
        wait_for_page(driver)

        element = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.LINK_TEXT, menu))
        )

        element.click()
        wait_for_page(driver)

        assert driver.current_url != BASE_URL or menu == "Home"
        print(f"{menu} navigation: PASS")


# 3. Test footer links
def test_footer_navigation(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    footer = driver.find_element(By.TAG_NAME, "footer")
    links = footer.find_elements(By.TAG_NAME, "a")

    assert len(links) > 0, "No footer links found"

    for link in links:
        href = link.get_attribute("href")
        text = link.text.strip() or "[No link text]"

        if href:
            print(f"Footer: {text} -> {href}")

            driver.get(href)
            wait_for_page(driver)

            assert driver.current_url
            print("PASS")


# 4. Test broken links
def test_broken_links(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    links = driver.find_elements(By.TAG_NAME, "a")
    broken_links = []

    for link in links:
        href = link.get_attribute("href")

        if not href:
            continue

        if href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue

        try:
            response = requests.get(
                href,
                timeout=10,
                allow_redirects=True
            )

            print(f"{response.status_code} -> {href}")

            if response.status_code >= 400:
                broken_links.append(
                    f"{response.status_code}: {href}"
                )

        except requests.RequestException as error:
            broken_links.append(f"ERROR: {href} ({error})")

    assert not broken_links, "Broken links found:\n" + "\n".join(broken_links)


# 5. Browser Back and Forward
def test_browser_back_forward(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    home_url = driver.current_url

    # Change this path to a page that exists.
    driver.get(BASE_URL.rstrip("/") + "/about")
    wait_for_page(driver)

    about_url = driver.current_url

    driver.back()
    wait_for_page(driver)

    assert driver.current_url == home_url
    print("Browser Back: PASS")

    driver.forward()
    wait_for_page(driver)

    assert driver.current_url == about_url
    print("Browser Forward: PASS")


# 6. Test dropdown navigation
def test_dropdown_navigation(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    # Change "country" to your dropdown's ID.
    dropdown_element = driver.find_element(By.ID, "country")
    dropdown = Select(dropdown_element)

    options = dropdown.options

    assert len(options) > 0, "No dropdown options found"

    for option in options:
        text = option.text.strip()

        if text:
            dropdown.select_by_visible_text(text)

            selected = dropdown.first_selected_option.text
            assert selected == text

            print(f"Dropdown '{text}': PASS")


# 7. Test links opening in new tabs
def test_new_tab_navigation(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    original_window = driver.current_window_handle
    original_windows = set(driver.window_handles)

    # Change "About" to your target link.
    link = driver.find_element(By.LINK_TEXT, "About")
    link.click()

    WebDriverWait(driver, TIMEOUT).until(
        lambda d: len(d.window_handles) > len(original_windows)
    )

    new_windows = set(driver.window_handles) - original_windows

    assert new_windows, "No new tab/window opened"

    for window in new_windows:
        driver.switch_to.window(window)
        wait_for_page(driver)

        assert driver.current_url
        print(f"New tab URL: {driver.current_url}")
        print("New tab navigation: PASS")

        driver.close()

    driver.switch_to.window(original_window)


# 8. Test internal links without leaving the website
def test_internal_navigation(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    links = driver.find_elements(By.TAG_NAME, "a")

    base_domain = BASE_URL.split("//")[1].split("/")[0]

    internal_links = []

    for link in links:
        href = link.get_attribute("href")

        if href and base_domain in href:
            internal_links.append(href)

    for href in set(internal_links):
        driver.get(href)
        wait_for_page(driver)

        assert base_domain in driver.current_url
        print(f"Internal link PASS: {href}")


# 9. Test links with valid URLs
def test_url_validation(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    links = driver.find_elements(By.TAG_NAME, "a")

    for link in links:
        href = link.get_attribute("href")

        if not href:
            continue

        if href.startswith(("http://", "https://")):
            assert " " not in href
            print(f"Valid URL: {href}")


# 10. Test navigation elements are visible and enabled
def test_navigation_elements(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    links = driver.find_elements(By.TAG_NAME, "a")

    assert len(links) > 0, "No navigation links found"

    for link in links:
        text = link.text.strip() or "[No text]"
        assert link.is_displayed(), f"Link not visible: {text}"
        assert link.is_enabled(), f"Link not enabled: {text}"

        print(f"Navigation element PASS: {text}")


# 11. Test logo/home navigation
def test_logo_navigation(driver):
    driver.get(BASE_URL + "/about")
    wait_for_page(driver)

    # Change the locator to match your logo.
    logo = WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.logo"))
    )

    logo.click()
    wait_for_page(driver)

    assert driver.current_url.rstrip("/") == BASE_URL.rstrip("/")
    print("Logo/Home navigation: PASS")


# 12. Test links using CSS selectors
def test_css_navigation(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    # Example:
    # Change the selector to your actual navigation selector.
    nav_links = driver.find_elements(
        By.CSS_SELECTOR,
        "nav a"
    )

    assert len(nav_links) > 0, "No nav links found"

    for link in nav_links:
        assert link.is_displayed()
        print(f"CSS navigation element: {link.text.strip()}")


# 13. Test links using XPath
def test_xpath_navigation(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    # Finds links inside navigation.
    nav_links = driver.find_elements(
        By.XPATH,
        "//nav//a"
    )

    assert len(nav_links) > 0, "No navigation links found"

    for link in nav_links:
        assert link.is_displayed()
        print(f"XPath navigation element: {link.text.strip()}")


# 14. Test links with target="_blank"
def test_target_blank_links(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    links = driver.find_elements(
        By.CSS_SELECTOR,
        'a[target="_blank"]'
    )

    for link in links:
        href = link.get_attribute("href")

        assert href, "target=_blank link has no href"

        print(f"New-tab link found: {href}")


# 15. Test empty/invalid navigation links.
def test_invalid_navigation_links(driver):
    driver.get(BASE_URL)
    wait_for_page(driver)

    links = driver.find_elements(By.TAG_NAME, "a")

    invalid_links = []

    for link in links:
        href = link.get_attribute("href")
        text = link.text.strip() or "[No text]"

        if not href:
            invalid_links.append(
                f"Empty href: {text}"
            )

        elif href.strip() == "#":
            invalid_links.append(
                f"Placeholder link: {text}"
            )

    assert not invalid_links, (
        "Invalid navigation links found:\n"
        + "\n".join(invalid_links)
    )
