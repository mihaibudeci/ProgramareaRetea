import time
import json
import pickle
import pprint
import requests
import pandas as pd

from selenium import webdriver
from urllib import request as urlrequest
from selenium.webdriver.chrome.options import Options
from proxy_requests import ProxyRequests, ProxyRequestsBasicAuth

# res = requests.get(input("Enter Proxy site URL: "))
res = requests.get("https://free-proxy-list.net/") # se preia proxy de pe site-ul dat

proxies = pd.read_html(res.text)
proxies = proxies[0][:80] 
with open("proxies.txt", "w") as f:                              # aceasta lista de proxy se salveaza si se ia din fixierul dat
    for index,row in proxies.iterrows():                         # se aranjeaza in colonita
        f.write("%s:%s\n"%(row["IP Address"],int(row["Port"])))  # in formatul urmator : Ip + Port
        print("%s:%s"%(row["IP Address"],int(row["Port"])))

text_file = open("proxies.txt", 'r')   # din acest fisier se ia primul proxy care va fi folosit
first_proxy = text_file.readline()
print("We'll use:", first_proxy)

proxy = {"http": first_proxy}
url = 'https://999.md/'
resp = requests.get(url, proxies=proxy) # are loc metoda get la url de mai sus cu ajutorul proxy -ului ales
print("Get method:", resp)

r = requests.post(url, data={'number': 12524, 'type': 'issue', 'action': 'show'}, proxies=proxy)
print("Post method:", r.status_code, r.reason)
print(r.text[:300] + '...')

x = requests.head(url, proxies=proxy)
print("Head method:", x.headers)

verbs = requests.options(url, proxies=proxy)
print("Options method:", verbs.status_code)
verbs = requests.options('http://a-good-website.com/api/cats')
print(verbs.headers['allow'])

def save_cookies(driver, location): # obiectul driver de care avem nevoie este trecut mai jos si primim cookies
                                    # iar ce primim din "get_cookies" este o lista de dictionare
    pickle.dump(driver.get_cookies(), open(location, "wb"))

def load_cookies(driver, location, url=None):
    cookies = pickle.load(open(location, "rb"))
    driver.delete_all_cookies() # ne asiguram ca nu avem alte cookie-uri
    driver.get("https://google.com" if url is None else url) # trebuie să fie pe o pagină înainte de a putea adăuga orice cookie-uri
    for cookie in cookies:
        if isinstance(cookie.get('expiry'), float): # Verifică dacă instanța expiră un float
            cookie['expiry'] = int(cookie['expiry']) # convertește cookie-ul de expirare în int
        driver.add_cookie(cookie)

# functia preia driver-ul si lista de domenii
def delete_cookies(driver, domains=None):
    cookies = driver.get_cookies()         # dacă lista de domenii este trecută, va merge înainte și va primi cookie-urile din browser
    for cookie in cookies:
        if domains is not None:
            if str(cookie["domain"]) in domains:
                cookies.remove(cookie)     # sterge domeniile de care nu avem nevoie

         # ștergerea tuturor și adăugarea obiectului cookie modificat
        else:
            driver.delete_all_cookies()
            return
    driver.delete_all_cookies()
    # cautarea cookie in lista si adaugarea in driver
    for cookie in cookies:
        driver.add_cookie(cookie)

# Încărcarea inițială a domeniului pentru care dorim să salvăm cookie-urile
cookies_location = "D:/Univer/progRetea/programmation-des-reseaux/TravaillePratiqueNr.3/cookies.txt"
driver = webdriver.Chrome('D:/SHIT/chromedriver.exe')
driver.get("https://999.md/")
elem = driver.find_element_by_xpath("/html/body/div[4]/header/div[2]/nav/ul/li[2]/a")
elem.click()
elem = driver.find_element_by_name('login')
elem.send_keys("email")
elem = driver.find_element_by_name('password')
elem.send_keys("password")
elem = driver.find_element_by_xpath("/html/body/div/div[1]/form/div[4]/button")
elem.click()
save_cookies(driver, cookies_location)
time.sleep(7)
driver.close()

# Încărcarea paginii la care nu puteți accesa fără cookie-uri
driver = webdriver.Chrome('D:/SHIT/chromedriver.exe')
load_cookies(driver, cookies_location)
driver.get("https://999.md/")
time.sleep(3)
driver.quit()
