import json
import os
import requests
import settings
from fake_useragent import UserAgent
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from sys import platform

ua = UserAgent()

cookies = {}
convert = 0
total_page = 0

def reg():
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    window = str()
    driver.get(settings.buff_reg)
    print('=' * 50)
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/ul/li/a').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="j_login_other"]').click()
    time.sleep(1)

    for i in driver.window_handles:
        if i == driver.current_window_handle:
            window += i
        else:
            driver.switch_to.window(i)

    name = str(input('>Никнейм Steam :'))
    driver.find_element(By.XPATH, '//*[@id="steamAccountName"]').send_keys(name)
    password = str(input('>Пароль Steam :'))
    driver.find_element(By.XPATH, '//*[@id="steamPassword"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="imageLogin"]').click()
    guard_s = str(input('>Steam Guard :')).upper()
    driver.find_element(By.XPATH, '//*[@id="twofactorcode_entry"]').send_keys(guard_s)
    driver.find_element(By.XPATH, '//*[@id="login_twofactorauth_buttonset_entercode"]/div[1]').click()
    # driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/ul/li[2]/a').click()
    driver.switch_to.window(window)
    time.sleep(3)
    driver.refresh()
    time.sleep(1)
    driver_cookies = driver.get_cookies()
    driver.close()
    driver.quit()
    for cookie in driver_cookies:
        cookies[cookie['name']] = cookie['value']
    with open('cookies.json', 'w') as file:
        json.dump(cookies, file)
    file.close()
    steam()

def steam():
    balance = float(requests.get('https://buff.163.com/api/asset/get_brief_asset/', cookies=cookies).json()['data']['alipay_amount'])*convert
    if platform == "linux" or platform == "linux2":
        os.system('clear')
    elif platform == "win32":
        os.system('cls')
    try:
        for i in range(1, total_page):
            r = requests.get(f'https://buff.163.com/api/market/goods?game=csgo&page_num={i}', cookies=cookies).json()['data']
            for item in r['items']:
                name = item['name']
                buff_price = float(item['sell_min_price']) * convert
                steam_price = float(item['goods_info']['steam_price'])
                sell_num = int(item['sell_num'])
                steam_link = item['steam_market_url']
                buff_link = f'https://buff.163.com/goods/{item["id"]}?from=market#tab=selling'
                if shop == 1:
                    if (value := (buff_price / steam_price) * 100) < 69 and sell_num >= 200 and buff_price <= balance:
                        print(f'{name}\nSell : {sell_num}\n{(100-value):.2f} %\n>BUFF : {buff_price:.2f} $\nBuff Link : {buff_link}\n>STEAM : {steam_price:.2f} $\nSteam Link : {steam_link}')
                        print('-'*20)
                    else:
                        continue
                elif shop == 2:
                    if (value := (buff_price / steam_price) * 100) > 100 and sell_num >= 120:
                        print(f'{name}\nSell : {sell_num}\n{(value-100):.2f} %\n>BUFF : {buff_price:.2f} $\nBuff Link : {buff_link}\n>STEAM : {steam_price:.2f} $\nSteam Link : {steam_link}')
                        print('-'*20)
                    else:
                        continue
    except:
        print('EXIT')


if __name__ == '__main__':
    print('[1] BUFF -> STEAM\n[2] STEAM -> BUFF')
    shop = int(input('=>'))
    r = requests.get(settings.buff_json).json()['data']
    total_page = r['total_page']
    cost = requests.get(settings.money).json()['rates']
    convert = cost['USD']
    try:
        cookies = json.load(open("cookies.json", "r"))
        steam()
    except:
        reg()
