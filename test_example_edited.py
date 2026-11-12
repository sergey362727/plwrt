# ФИО: Щетинин Сергей Витальевич
# Дата: 2026-11-10
# Время: 22:56
# Описание изменений: 
# 1. проверяет путь обычного пользователя который зашел на сайт
# 2. ищет кнопку Get started | get_started = page.get_by_role("link", name="Get started") | get_started.click()
# 3. проверяет ссылку после нажатия кнопки Get started | expect(page).to_have_url(re.compile(".*intro"))
# 4. показывает ссылку на которой завершилась программма print(f"after the test runs (final URL: {page.url})")
# Зачем: первый код проверял только открытие главной страницы, а здесь я добавил проверку заголовка, клик по кнопке Get started и вывод итоговой ссылки.

import re
import pytest
from playwright.sync_api import Page, expect

    # автоматическая фикстура
@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    # код перед началом теста
    print("before the test runs")
    page.goto("https://playwright.dev/")

    yield

    # код который сработает после завершения теста
    print(f"after the test runs (final URL: {page.url})")


    # проверяет загрузку главной стрницы и переход в документацию
def test_main_navigation(page: Page):
    expect(page).to_have_url("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))

    # поиск кнопки Get started и переход в документацию
    get_started = page.get_by_role("link", name="Get started")
    get_started.click()
    expect(page).to_have_url(re.compile(".*intro"))