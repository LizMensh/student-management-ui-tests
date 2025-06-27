from faker import Faker
import random
from datetime import datetime, timedelta


fake = Faker('ru_RU')


def generate_email():
    """Генерация случайного email"""
    return fake.unique.email()


def generate_password(min_length=8, max_length=16):
    """Генерация сложного пароля"""
    return fake.unique.password(length=random.randint(min_length, max_length),
                                special_chars=True, digits=True, upper_case=True, lower_case=True)


def generate_first_name():
    """Генерация имени"""
    return fake.first_name()


def generate_last_name():
    """Генерация фамилии"""
    return fake.last_name()


def generate_middle_name():
    """Генерация отчества (для русских имен)"""
    return fake.middle_name()


def generate_full_name():
    """Генерация полного ФИО"""
    return f"{generate_last_name()} {generate_first_name()} {generate_middle_name()}"


def generate_birth_date(min_age=18, max_age=70):
    """Генерация даты рождения в формате YYYY-MM-DD"""
    end_date = datetime.now() - timedelta(days=min_age * 365)
    start_date = datetime.now() - timedelta(days=max_age * 365)
    return fake.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')


def generate_admission_date(start_year=2015):
    """Генерация даты поступления (не раньше указанного года)"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    return fake.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')


def generate_gender():
    """Генерация пола (М/Ж)"""
    return random.choice(['М', 'Ж'])


def generate_age(min_age=16, max_age=30):
    """Генерация возраста"""
    return random.randint(min_age, max_age)
