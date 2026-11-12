# ФИО: Щетинин Сергей Витальевич
# Дата: 2026-11-9
# Время: 21:20
# Описание: переходит по ссылке https://playwright.dev/ и проверяет что переход произошел на нужный сайт
# Я скопировал пример из раздела "Writing tests" и запустил его локально.

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
    print("after the test runs")

    # проврека ссылки по которой был произведен переход
def test_main_navigation(page: Page):
    expect(page).to_have_url("https://playwright.dev/")