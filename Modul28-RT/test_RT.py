# python -m pytest -v --driver Chrome --driver-path c:/python/chromedriver_win32/chromedriver.exe Modul28-RT\test_RT.py

from time import sleep
from pages_base import *
from settings import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# тест 002 общий вид страницы (сохранить скриншот)
def test_002_vision(selenium):
    form = AuthForm(selenium)
    form.driver.save_screenshot('screen_001.jpg')


# тест 006 по умолчанию выбрана форма авторизации по телефону
def test_006_by_phone(selenium):
    form = AuthForm(selenium)
    assert form.placeholder.text == 'Мобильный телефон'


# тест 007 авторизация по телефону
def test_007_positive_by_phone(selenium):
    form = AuthForm(selenium)
    # ввод телефона
    form.username.send_keys(valid_phone)
    form.password.send_keys(valid_pass)
    sleep(5)
    form.btn_click()
    assert form.get_current_url() != '/account_b2c/page'


# тест 008 авторизация по почте
def test_008_positive_by_email(selenium):
    form = AuthForm(selenium)
    # ввод почты
    form.username.send_keys(valid_email)
    form.password.send_keys(valid_pass)
    sleep(5)
    form.btn_click()
    assert form.get_current_url() != '/account_b2c/page'


# тест 009 авторизация по логину
def test_009_positive_by_log(selenium):
    form = AuthForm(selenium)
    # ввод логина
    form.username.send_keys('rtkid_1666666666666')
    form.password.send_keys(valid_pass)
    sleep(5)
    form.btn_click()
    assert form.get_current_url() != '/account_b2c/page'


# тест 010 авторизация по лицевому счету
def test_010_positive_by_pers_acc(selenium):
    form = AuthForm(selenium)
    # ввод лицевому счету
    form.username.send_keys('642011642011')
    form.password.send_keys(valid_pass)
    sleep(5)
    form.btn_click()
    assert form.get_current_url() != '/account_b2c/page'


# тест 012 получения временного кода на телефон, открытие формы для ввода кода
def test_012_get_code(selenium):
    form = CodeForm(selenium)
    # ввод телефона
    form.address.send_keys(valid_phone)
    # пауза для ввода капчи
    sleep(15)
    form.get_click()
    rt_code = form.driver.find_element(By.ID, 'rt-code-0')
    assert rt_code


# тест 013 проверка автосмены типа авторизации
def test_013_change_placeholder(selenium):
    form = AuthForm(selenium)
    # ввод телефона
    form.username.send_keys('+79235250110')
    form.password.send_keys('_')
    sleep(5)
    assert form.placeholder.text == 'Мобильный телефон'
    # очистка поля логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)
    # ввод почты
    form.username.send_keys('skrab@yandex.ru')
    form.password.send_keys('_')
    sleep(5)
    assert form.placeholder.text == 'Электронная почта'
    # очистка поля логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)
    # ввод логина
    form.username.send_keys('Login')
    form.password.send_keys('_')
    sleep(5)
    assert form.placeholder.text == 'Логин'


# тест 014 открытие формы восстановления пароля
def test_014_forgot_pass(selenium):
    form = AuthForm(selenium)
    # нажатие надписи "Забыл пароль"
    form.forgot.click()
    sleep(5)
    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')
    assert reset_pass.text == 'Восстановление пароля'


# тест 015 переход и открытие формы регистрации
def test_015_register(selenium):
    form = AuthForm(selenium)
    # нажатие на надпись "Зарегистрироваться"
    form.register.click()
    sleep(5)
    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')
    assert reset_pass.text == 'Регистрация'


# тест 017 открытие пользовательского соглашения
def test_017_agreement(selenium):
    form = AuthForm(selenium)
    original_window = form.driver.current_window_handle
    # нажатие на надпись "Пользовательское соглашение" в подвале
    form.agree.click()
    sleep(5)
    WebDriverWait(form.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in form.driver.window_handles:
        if window_handle != original_window:
            form.driver.switch_to.window(window_handle)
            break
    win_title = form.driver.execute_script("return window.document.title")
    assert win_title == 'User agreement'


# тест 018 переход по ссылке авторизации через соцсеть ВК
def test_018_auth_vk(selenium):
    form = AuthForm(selenium)
    form.vk_btn.click()
    sleep(5)
    assert form.get_base_url() == 'oauth.vk.com'


# тест 019 переход по ссылке авторизации через соцсеть ОК
def test_019_auth_ok(selenium):
    form = AuthForm(selenium)
    form.ok_btn.click()
    sleep(5)
    assert form.get_base_url() == 'connect.ok.ru'


# тест 020 переход по ссылке авторизации через майлру
def test_020_auth_mailru(selenium):
    form = AuthForm(selenium)
    form.mailru_btn.click()
    sleep(5)
    assert form.get_base_url() == 'connect.mail.ru'


# тест 021 перехода по ссылке авторизации через google
def test_021_auth_google(selenium):
    form = AuthForm(selenium)
    form.google_btn.click()
    sleep(5)
    assert form.get_base_url() == 'accounts.google.com'


# тест 022 переход по ссылке авторизации через яндекс
def test_022_auth_ya(selenium):
    form = AuthForm(selenium)
    form.ya_btn.click()
    sleep(5)
    assert form.get_base_url() == 'b2c.passport.rt.ru'


# тест 025 негативный сценарй авторизации с пустыми полями
def test_025_negative_by_zero(selenium):
    form = AuthForm(selenium)
    # ввода нет
    form.username.send_keys(' ')
    form.password.send_keys(' ')
    sleep(5)
    form.btn_click()
    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# тест 026 негативный сценарй авторизации по телефону
def test_026_negative_by_phone(selenium):
    form = AuthForm(selenium)
    # ввод телефона
    form.username.send_keys('+74628375142')
    form.password.send_keys('any_password')
    sleep(5)
    form.btn_click()
    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# тест 027 негативный сценарий авторизации по почте
def test_027_negative_by_email(selenium):
    form = AuthForm(selenium)
    # ввод почты
    form.username.send_keys('gurburmur@yam.ru')
    form.password.send_keys('any_password')
    sleep(5)
    form.btn_click()
    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'

# тест 028 негативный сценарий авторизации по логину
def test_028_negative_by_log(selenium):
    form = AuthForm(selenium)
    # ввод логина
    form.username.send_keys('rtkid_1666666666666')
    form.password.send_keys('any_password')
    sleep(5)
    form.btn_click()
    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# тест 029 негативный сценарий авторизации по лицевому счету
def test_029_negative_by_pers_acc(selenium):
    form = AuthForm(selenium)
    # ввод логина
    form.username.send_keys('rtkid_1666666666666')
    form.password.send_keys('any_password')
    sleep(5)
    form.btn_click()
    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


