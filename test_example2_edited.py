# ФИО: Щетинин Сергей Витальевич
# Дата: 2026-11-12
# Время: 20:41
# Описание изменений: Я существенно доработал исходный пример из раздела "Writing tests".
# 1. проверка видимости заголовка Installation (expect(heading).to_be_visible()), чтобы убедиться в полной загрузке раздела.
# 2. сделал полный сценарий поиска по документации: клик по кнопке Search, ввод запроса "locators", нажатие Enter для перехода к статье и проверку нового URL (.*locators) с заголовком Locators.
# 3. Добавил сохранение итогового скриншота (page.screenshot) и вывод финального адреса страницы в фикстуре
# Зачем: до этого код проверял только базовый переход по одной ссылке,а вариант имитирует полноценный путь поиска нужной документации человеком с проверкой результата на каждом шаге.

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
    page.get_by_role("button", name="Search").click()
    search_input = page.get_by_placeholder("Search docs")
    search_input.fill("locators")
    expect(page.locator(".DocSearch-Dropdown")).to_be_visible()

    # переход по первому результату поиска и проверка открытой страницы
    search_input.press("Enter")
    expect(page).to_have_url(re.compile(".*locators"))
    expect(page.get_by_role("heading", name="Locators", exact=True)).to_be_visible()
