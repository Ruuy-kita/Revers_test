import time
import csv

import pyautogui
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")  #на весь экран
    options.add_argument("--disable-blink-features=AutomationControlled")  #3 опции включая эту отвечают за анонимность драйвера
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    return driver


def move_to_element(driver, xpath_selector):
    element = driver.find_element(By.XPATH, xpath_selector)
    achains = ActionChains(driver)
    achains.move_to_element(element).perform()
    return driver


def pars_data(driver):
    result_list = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    table_elements = soup.find('tbody').find_all('tr')

    for item in table_elements:
        name = item.findAll('td')[1].text
        price = item.findAll('td')[6].text
        if price != '':
            result_list.append([name, price])

    return result_list


def write_data(data):
    with open("result.csv", mode="w", encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
        file_writer.writerow(["Имя", "Цена"])
        for itm in data:
            file_writer.writerow(itm)


def check_element_visibility(element):
    element_location = element.location
    element_size = element.size

    # Получаем координаты элемента
    element_x = element_location['x']
    element_y = element_location['y']
    element_width = element_size['width']
    element_height = element_size['height']

    # Получаем текущие координаты курсора
    cursor_x, cursor_y = pyautogui.position()

    if element_x < cursor_x < element_x + element_width and element_y < cursor_y < element_y + element_height:
        return True
    else:
        return False


# парс данных

driver = init_driver()  # инициализация хром драйвера
driver.get('https://www.nseindia.com/')

move_to_element(driver, '(//a[text()="Market Data"])[1]')  #навестись на элемент
PreOpenMarket_xpath = '(//a[text()="Pre-Open Market"])[1]'
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, PreOpenMarket_xpath)))  #ждем на элемент
driver.find_element(By.XPATH, PreOpenMarket_xpath).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//td[@class="togglecpm plus"]')))
data = pars_data(driver)  #парсим данные
write_data(data)  #записываем данные

# пользовательский сценарий использования сайта

driver.get('https://www.nseindia.com/')
time.sleep(1)
driver.find_element(By.XPATH, '//p[@id="NIFTY BANK"]').click()
view_all_xpath = '(//a[@href="/market-data/live-equity-market?symbol=NIFTY BANK"])[1]'

footer = driver.find_element(By.XPATH, "//footer")
view_all = driver.find_element(By.XPATH, view_all_xpath)

scroll_js = "window.scrollBy(0, 100);"  # x, y на сколько скролим вниз
for _ in range(5):
    driver.execute_script(scroll_js)
    time.sleep(1)
    if check_element_visibility(view_all):  #проверяем, виден ли элемент на экране пользователем
        break

view_all.click()
time.sleep(3)
driver.find_element(By.XPATH, '//select[@id="equitieStockSelect"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//option[@value="NIFTY LARGEMIDCAP 250"]').click()
time.sleep(10)

for _ in range(1000):  #скролим до тех пор, пока не будет конца страницы
    driver.execute_script(scroll_js)
    time.sleep(0.2)  # замедоение между скролами
    end_of_page = driver.execute_script("return document.body.scrollHeight")
    current_value = driver.execute_script("return window.pageYOffset + window.innerHeight")
    if current_value >= end_of_page:
        break

