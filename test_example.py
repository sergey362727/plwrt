# ФИО: Щетинин Сергей Витальевич
# Дата: 2026-11-10
# Время: 21:20
# Описание: 
# 
# Я скопировал пример из раздела "Writing tests" и запустил его локально.

import pytest
from playwright.sync_api import Page, expect

# Фикстура которая работавет автоматически
@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    # Код перед запуском самого теста
    print("before the test runs")
    page.goto("https://playwright.dev/")
    
    yield
    
    # Код, который сработает сразу после окончания теста
    print("after the test runs")

# Тест проверяет, что браузер перешел по нужному адресу
def test_main_navigation(page: Page):
    expect(page).to_have_url("https://playwright.dev/")