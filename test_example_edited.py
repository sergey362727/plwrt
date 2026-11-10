# ФИО: Щетинин Сергей Витальевич
# Дата: 2026-11-10
# Время: 21:55
# Описание изменений: Я модифицировал исходный тестовый скрипт pytest + playwright.
# 1. Изменил фикстуру before_each_after_each: вместо простого print добавил проверку, что страница успешно загрузилась (expect).
# 2. Добавил дополнительную проверку (assert) внутри самого теста test_main_navigation, контролирующую наличие слова "Playwright" в теге <title>.
# 3. Добавил новые комментарии к измененным строкам кода.
# Зачем: В исходном примере проверялся только URL. Модификация усложняет тест, делает его более комплексным и приближенным к реальным e2e-тестам (проверяется и адрес, и метаданные страницы).
import re
import pytest
from playwright.sync_api import Page, expect

# Фикстура, которая работает автоматически для каждого теста
@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    print("before the test runs")
    page.goto("https://playwright.dev/")
    # Изменено: добавлена валидация того, что страница дошла до стабильного состояния готовности
    page.wait_for_load_state("domcontentloaded") 
    yield
    print("after the test runs")

# Тест проверяет адрес и контент страницы
def test_main_navigation(page: Page):
    # Проверка 1 (исходная): проверка корректности URL
    expect(page).to_have_url("https://playwright.dev/")
    
    # Изменено (Добавлено): Проверка 2 — контроль заголовка вкладки для защиты от пустых страниц
    expect(page).to_have_title(re.compile(r"Playwright"))