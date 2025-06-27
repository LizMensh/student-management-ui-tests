import requests
from config import BASE_URL, ADMIN_CREDS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pytest


@pytest.fixture(scope="function")
def browser():
    """Фикстура для инициализации браузера в CI"""
    chrome_options = Options()

    chrome_options.add_argument("--headless=new")  # Новый headless-режим (Chrome 112+)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )

    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def auth_admin():
    register_url = f"{BASE_URL}/api/register"
    register_data = {
        "login": ADMIN_CREDS["username"],
        "password": ADMIN_CREDS["password"],
    }
    response = requests.post(register_url, json=register_data)
    assert response.status_code == 200, "Не удалось зарегистрировать администратора"

    login_url = f"{BASE_URL}/api/auth"
    login_data = {
        "login": ADMIN_CREDS["username"],
        "password": ADMIN_CREDS["password"]
    }
    response = requests.post(login_url, json=login_data)
    assert response.status_code == 200, "Не удалось авторизоваться"

    return response.json()["token"]


@pytest.fixture
def login_ui(browser, auth_admin):
    browser.get(f"{BASE_URL}/login")

    username_field = browser.find_element(By.NAME, "login")
    password_field = browser.find_element(By.NAME, "password")
    submit_button = browser.find_element(By.ID, "add-btn")

    username_field.send_keys(ADMIN_CREDS["username"])
    password_field.send_keys(ADMIN_CREDS["password"])
    submit_button.click()

    WebDriverWait(browser, 10).until(
        EC.url_contains("/users-page")
    )


@pytest.fixture
def add_student_page(browser, login_ui):
    browser.get(f"{BASE_URL}/add-user")
    return browser
