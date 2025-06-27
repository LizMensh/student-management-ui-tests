import pytest
import utils.helpers as helpers

# Позитивные тестовые данные
POSITIVE_DATA = [
    (
        helpers.generate_first_name(),
        helpers.generate_age(),
        helpers.generate_gender(),
        "2023-09-01",
        True
    ),
    (
        helpers.generate_first_name(),
        helpers.generate_age(),
        helpers.generate_gender(),
        None,
        False
    )
]

# Негативные тестовые данные
NEGATIVE_DATA = [
    (None, helpers.generate_age(), helpers.generate_gender(), None, False),
    (helpers.generate_first_name(), None, helpers.generate_gender(), None, False)
]


@pytest.mark.parametrize("name,age,gender,birthday,is_active", POSITIVE_DATA)
def test_add_student_successfully(add_student_page, name, age, gender, birthday, is_active):
    add_student_page.add_student(name, age, gender, birthday, is_active)
    assert "Пользователь успешно добавлен!" in add_student_page.get_success_message()


@pytest.mark.parametrize("name,age,gender,birthday,is_active", NEGATIVE_DATA)
def test_add_student_negative_cases(add_student_page, name, age, gender, birthday, is_active):
    add_student_page.add_student(name, age, gender, birthday, is_active)
    errors = add_student_page.get_error_messages()
    assert any("Поле обязательно" in error for error in errors)
    assert len(errors) >= 1


def test_add_student_without_required_fields(add_student_page):
    add_student_page.add_student()
    errors = add_student_page.get_error_messages()
    assert len(errors) >= 2
    assert all("Поле обязательно" in error for error in errors[:2])
