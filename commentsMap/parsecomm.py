import time
import sqlite3 as sql
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver.common.proxy import *


def get_data_with_selenium(cr1):
    try:
        con = sql.connect('db.sqlite3')

        # myProxy = "91.240.190.131:8085"
        # proxy = Proxy({
        #     'proxyType': ProxyType.MANUAL,
        #     'httpProxy': myProxy,
        #     'ftpProxy': myProxy,
        #     'sslProxy': myProxy,
        #     'noProxy': ''})
        # # options = driver.add_argument("start-maximized")
        # driver = webdriver.Firefox(proxy=proxy)
        # driver.set_page_load_timeout(30)
        #
        # driver.set_window_size(1920, 1080)

        # driver = webdriver.Firefox()
        # driver.set_window_size(1920, 1080)

        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches",["enable-automation"])
        options.add_experimental_option('useAutomationExtension',False)
        driver = webdriver.Chrome(options=options)

        stealth(driver,
                languages=["ru"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True
        )

        # driver.set_window_size(1920, 1080)
        urlsite = f"https://www.google.com/maps/search/%D0%B1%D0%B0%D0%BD%D0%BA/@{cr1}"
        driver.get(urlsite)
        driver.set_page_load_timeout(30)
        time.sleep(10)
        how = 0

        try:
            ActionChains(driver).click(driver.find_elements(By.CSS_SELECTOR, ".ie0N9b ")[0]).perform()
            ActionChains(driver).click(driver.find_elements(By.CSS_SELECTOR, ".ie0N9b")[1]).perform()
            time.sleep(1)
            ActionChains(driver).click(driver.find_elements(By.CSS_SELECTOR, ".Tc0rEd")[0]).perform()
            time.sleep(5)
        except:
            pass
        while True:
            try:
                driver.execute_script(f'document.querySelectorAll(".Nv2PK")[{how}].scrollIntoView()')
                how += 1
            except:
                try:
                    time.sleep(3)
                    driver.execute_script(f'document.querySelectorAll(".Nv2PK")[{how}].scrollIntoView()')
                    how += 1
                except:
                    break
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        href = []

        for elements in soup.findAll('div', {'class': 'Nv2PK'}):
            try:
                comms = int(elements.find('span', {'class': 'UY7F9'}).text.replace('(', '').replace(')', ''))
                bank = elements.find('a', {'class': 'hfpxzc'})['aria-label']
                # adres = elements.find('div', {'class': 'Io6YTe '})
                url = elements.find('a', {'class': 'hfpxzc'})['href']
                href.append([bank, url, comms])
            except:
                pass

        for j in range(len(href)):
            driver.get(href[j][1])
            time.sleep(5)
            cur = con.cursor()
            adress = driver.find_element(By.CSS_SELECTOR, '.Io6YTe').text

            while True:
                try:
                    ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR, ".F7nice")).perform()
                    break
                except:
                    time.sleep(3)
                    print('No')
            time.sleep(5)
            data = []
            urlcomm = ''
            i = 0
            if href[j][2] != 0:
                while True:
                    try:
                        driver.execute_script(f'document.querySelectorAll(".jftiEf")[{i}].scrollIntoView();')
                        i += 1
                    except:
                        try:
                            time.sleep(3)
                            driver.execute_script(f'document.querySelectorAll(".jftiEf")[{i}].scrollIntoView();')
                            i += 1
                        except:
                            break
                i = 0
                ii = 1
                for q in range(href[j][2]):
                    time.sleep(1)
                    # try:
                    #     driver.execute_script(f'document.querySelectorAll(".jftiEf")[{i}].scrollIntoView();')
                    #     time.sleep(1)
                    # except:
                    #     pass
                    # driver.execute_script('document.querySelector(".DxyBCb").scrollTop=21000000000;')
                    # time.sleep(5)

                    try:
                        name = driver.find_elements(By.CSS_SELECTOR, '.d4r55 > span')[i].text
                        date = driver.find_elements(By.CSS_SELECTOR, '.rsqaWe')[i].text
                        star = driver.find_elements(By.CSS_SELECTOR, '.kvMYJc')[i].get_attribute('aria-label')
                    except:
                        name = ''
                        date = ''
                        star = ''
                        pass
                    # Комментарий развернуть
                    try:
                        ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR, ".w8nwRe")).perform()
                    except:
                        pass
                        # Комментарий текст
                    try:
                        # text = driver.find_elements(By.CSS_SELECTOR, '.wiI7pd')[i].text.split('(Оригинал)\n')[1]
                        text = driver.find_elements(By.CSS_SELECTOR, '.MyEned')[i].text
                    except:
                        text = ''
                    # Ссылка
                    if text!='':
                        try:
                            ActionChains(driver).click(driver.find_elements(By.CSS_SELECTOR, ".GBkF3d")[ii]).perform()
                            try:
                                urlcomm = driver.find_element(By.CLASS_NAME, 'vrsrZe').get_attribute('value')
                                ii += 2
                            except:
                                try:
                                    time.sleep(5)
                                    urlcomm = driver.find_element(By.CLASS_NAME, 'vrsrZe').get_attribute('value')
                                    ii += 2
                                except:
                                    urlcomm = ''
                                    break
                            ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR, ".AmPKde")).perform()
                        except:
                            urlcomm = ''
                            pass
                    else:
                        urlcomm=''

                    i += 1

                    cur.execute(
                        "INSERT INTO commentsMap_comment (content, author, date_comm, stars, url, bank, department) VALUES(?, ?, ?, ?, ?, ?, ?)",
                        (text, name, date, star, urlcomm, href[j][0], adress))
                    con.commit()
                    data.append([text, name, date, star, urlcomm, href[j][0], adress])
    except:
        driver.close()
        driver.quit()
        return data
    finally:
        driver.close()
        driver.quit()
        return data

        # cur.close()
        # con.close()
