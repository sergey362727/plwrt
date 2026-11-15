# ФИО: Щетинин Сергей Витальевич
# Дата: 2026-11-15
# Время: 13:34
# Описание изменений:
# 1. проверяет активность кнопки Search перед нажатием на нее | expect(search_button).to_be_enabled()
# 2. кликает по первому результату из выпадающего списка вместо нажатия Enter | first_result = dropdown.locator(".DocSearch-Hit").first | expect(first_result).to_be_visible() | first_result.click()
# 3. проверяет наличие загруженного текста статьи на открывшейся странице | expect(page.locator("article")).not_to_be_empty()
# 4. сохраняет полный скриншот всей страницы с именем теста в названии файла | screenshot_name = f"final_{request.node.name}.png" | page.screenshot(path=screenshot_name, full_page=True)
# Зачем: прошлый вариант нажимал Enter вслепую и делал скриншот только видимой части экрана, а здесь тест проверяет кликабельность подсказок, наличие текста в статье и сохраняет полный скриншот для каждого теста отдельно.

import re
import pytest
from playwright.sync_api import Page, expect


# автоматическая фикстура
@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page, request: pytest.FixtureRequest):
    # код перед началом теста
    print(f"before the test runs ({request.node.name})")
    page.goto("https://playwright.dev")

    yield

    # код после завершения теста
    screenshot_name = f"final_{request.node.name}.png"
    page.screenshot(path=screenshot_name, full_page=True)  # добавлено: скриншот всей страницы с именем теста
    print(f"after the test runs (final URL: {page.url}, screenshot: {screenshot_name})")


# проверяет загрузку главной страницы и сквозной сценарий поиска в документации
def test_main_navigation(page: Page):
    expect(page).to_have_url("https://playwright.dev")
    expect(page).to_have_title(re.compile("Playwright"))

    # поиск кнопки Get started и переход в документацию
    get_started = page.get_by_role("link", name="Get started")
    get_started.click()
    expect(page).to_have_url(re.compile(".*intro"))

    # проверка наличия заголовка на открывшейся странице
    heading = page.get_by_role("heading", name="Installation")
    expect(heading).to_be_visible()

    # открытие поиска, ввод запроса и проверка выпадающего списка
    search_button = page.get_by_role("button", name="Search")
    expect(search_button).to_be_enabled()
    search_button.click()

    search_input = page.get_by_placeholder("Search docs")
    search_input.fill("locators")
    dropdown = page.locator(".DocSearch-Dropdown")
    expect(dropdown).to_be_visible()

    # клик по первому результату из списка и проверка открытой страницы
    first_result = dropdown.locator(".DocSearch-Hit").first
    expect(first_result).to_be_visible()
    first_result.click()

    expect(page).to_have_url(re.compile(".*locators"))
    expect(page.get_by_role("heading", name="Locators", exact=True)).to_be_visible()
    expect(page.locator("article")).not_to_be_empty()  # проверка, что текст статьи загрузился
