# ФИО: Щетинин Сергей Витальевич
# Дата: 2026-11-12
# Время: 20:41
# Описание изменений:
# 1. добавляет реальное сохранение итогового скриншота в фикстуре после теста | page.screenshot(path="final_result.png")
# 2. нажимает Enter в поле поиска для перехода на страницу найденной статьи | search_input.press("Enter")
# 3. проверяет новый адрес страницы и видимость главного заголовка Locators | expect(page).to_have_url(re.compile(".*locators")) | expect(page.get_by_role("heading", name="Locators", exact=True)).to_be_visible()
# Зачем: прошлый вариант только вводил запрос в поиск и писал в консоль о скриншоте, а здесь тест реально переходит в статью по нажатию Enter, проверяет ее заголовок и сохраняет файл скриншота на диск.

import re
import pytest
from playwright.sync_api import Page, expect

# автоматическая фикстура
@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    # код перед началом теста
    print("before the test runs")
    page.goto("https://playwright.dev")

    yield

    # код после завершения теста
    page.screenshot(path="final_result.png")  # добавлено: сохранение скриншота итоговой страницы
    print(f"after the test runs (final URL: {page.url}, screenshot saved)")


# проверяет загрузку главной страницы и сквозной сценарий поиска в документации
def test_main_navigation(page: Page):
    expect(page).to_have_url("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))

    # поиск кнопки Get started и переход в документацию
    get_started = page.get_by_role("link", name="Get started")
    get_started.click()
    expect(page).to_have_url(re.compile(".*intro"))

    # проверка наличия заголовка на открывшейся странице
    heading = page.get_by_role("heading", name="Installation")
    expect(heading).to_be_visible()

    # открытие поиска, ввод запроса и проверка выпадающего списка
    page.get_by_role("button", name="Search").click()
    search_input = page.get_by_placeholder("Search docs")
    search_input.fill("locators")
    dropdown = page.locator(".DocSearch-Dropdown")
    expect(dropdown).to_be_visible()
    expect(dropdown.locator(".DocSearch-Hit").first).to_be_visible()  # добавить ожидание первой подсказки

    # переход по первому результату поиска и проверка открытой страницы
    search_input.press("Enter")

    expect(page).to_have_url(re.compile(".*locators"))
    expect(page.get_by_role("heading", name="Locators", exact=True)).to_be_visible()
