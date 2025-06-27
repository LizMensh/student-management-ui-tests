
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AddStudentPage(BasePage):
    NAME_INPUT = (By.ID, "name")
    AGE_INPUT = (By.ID, "age")
    GENDER_SELECT = (By.ID, "gender")
    BIRTHDAY_INPUT = (By.ID, "date_birthday")
    IS_ACTIVE_CHECKBOX = (By.ID, "isActive")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "alert-success")
    ERROR_MESSAGES = (By.CLASS_NAME, "text-danger")

    def add_student(self, name=None, age=None, gender=None, birthday=None, is_active=False):
        if name:
            self.find(self.NAME_INPUT).send_keys(name)
        if age:
            self.find(self.AGE_INPUT).send_keys(age)
        if gender:
            self.find(self.GENDER_SELECT).send_keys(gender)
        if birthday:
            self.find(self.BIRTHDAY_INPUT).send_keys(birthday)
        if is_active:
            self.find(self.IS_ACTIVE_CHECKBOX).click()

        self.find(self.SUBMIT_BUTTON).click()
        return self

    def get_success_message(self):
        return self.find(self.SUCCESS_MESSAGE).text

    def get_error_messages(self):
        return [msg.text for msg in self.find_all(self.ERROR_MESSAGES)]