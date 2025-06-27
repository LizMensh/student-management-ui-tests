from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = (By.NAME, "login")
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON = (By.ID, "add-btn")

    def load(self):
        self.driver.get(f"{BASE_URL}/login")
        return self

    def login(self, username: str, password: str):
        self.find(self.USERNAME_INPUT).send_keys(username)
        self.find(self.PASSWORD_INPUT).send_keys(password)
        self.find(self.SUBMIT_BUTTON).click()
        return self
