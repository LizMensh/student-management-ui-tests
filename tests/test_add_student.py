import utils.helpers as helpers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_add_student_successfully(add_student_page):
    browser = add_student_page

    browser.find_element(By.ID, "name").send_keys(helpers.generate_first_name())
    browser.find_element(By.ID, "age").send_keys(helpers.generate_age())
    browser.find_element(By.ID, "gender").send_keys(helpers.generate_gender())
    browser.find_element(By.ID, "date_birthday").send_keys("2023-09-01")
    browser.find_element(By.ID, "isActive").click()

    browser.find_element(By.XPATH, "//button[@type='submit']").click()

    success_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    )
    assert "Пользователь успешно добавлен!" in success_message.text


def test_add_student_without_required_fields(add_student_page):
    browser = add_student_page

    browser.find_element(By.XPATH, "//button[@type='submit']").click()

    error_messages = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "text-danger"))
    )

    assert len(error_messages) >= 2
    assert "Поле обязательно" in error_messages[0].text


def test_add_student_without_name(add_student_page):
    browser = add_student_page

    browser.find_element(By.ID, "age").send_keys(helpers.generate_age())

    browser.find_element(By.XPATH, "//button[@type='submit']").click()

    error_message = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "text-danger"))
    )

    assert len(error_message) == 2
    assert "Поле обязательно" in error_message[0].text
