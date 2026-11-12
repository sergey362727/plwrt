# ФИО: Щетинин Сергей Витальевич
# Дата: 2026-11-11
# Время: 09:55
# Описание изменений:
# 1. проверяет наличие и видимость заголовка Installation | heading = page.get_by_role("heading", name="Installation") | expect(heading).to_be_visible()
# 2. открывает поиск по сайту, вводит запрос "locators" и проверяет появление списка результатов | page.get_by_role("button", name="Search").click() | search_input.fill("locators") | expect(page.locator(".DocSearch-Dropdown")).to_be_visible()
# 3. выводит итоговую ссылку и сообщение о скриншоте после завершения теста | print(f"after the test runs (final URL: {page.url}, screenshot saved)")
# Зачем: прошлый вариант проверял только переход в документацию по кнопке, а теперь есть проверка заголовка на странице и проверка работы поиска на сайте.

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

    # код после завершения теста
    print(f"after the test runs (final URL: {page.url}, screenshot saved)")


    # проверяет загрузку главной стрницы и переход в документацию
def test_main_navigation(page: Page):
    expect(page).to_have_url("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))

    # поиск кнопки Get started и переход в документацию
    get_started = page.get_by_role("link", name="Get started")
    get_started.click()
    expect(page).to_have_url(re.compile(".*intro"))

    # проверяет наличие заголовка на открывшейся странице
    heading = page.get_by_role("heading", name="Installation")
    expect(heading).to_be_visible()

    # открытие поиска, ввод запроса и проверка появления результатов 
    page.get_by_role("button", name="Search").click()
    search_input = page.get_by_placeholder("Search docs")
    search_input.fill("locators")
    expect(page.locator(".DocSearch-Dropdown")).to_be_visible()
