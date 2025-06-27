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

from pages.add_student_page import AddStudentPage
from pages.login_page import LoginPage


@pytest.fixture(scope="function")
def browser():
    """Фикстура для инициализации браузера"""
    chrome_options = Options()

    # Настройки для CI
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # Дополнительные параметры для стабильности
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def register_admin():
    """Регистрация администратора через API"""
    register_url = f"{BASE_URL}/api/register"
    response = requests.post(
        register_url,
        json={
            "login": ADMIN_CREDS["username"],
            "password": ADMIN_CREDS["password"]
        }
    )
    assert response.status_code == 200, f"Ошибка регистрации: {response.text}"
    return response.json()


@pytest.fixture
def login_page(browser, register_admin):
    """Фикстура для страницы логина"""
    return LoginPage(browser)


@pytest.fixture
def logged_in_browser(browser, login_page, register_admin):
    """Браузер с выполненным логином через UI"""
    login_page.load()
    login_page.login(ADMIN_CREDS["username"], ADMIN_CREDS["password"])

    # Проверяем успешный логин
    WebDriverWait(browser, 10).until(
        EC.url_contains("/users-page")
    )
    return browser


@pytest.fixture
def add_student_page(logged_in_browser):
    """Фикстура для страницы добавления студента"""
    logged_in_browser.get(f"{BASE_URL}/add-user")
    return AddStudentPage(logged_in_browser)