from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path = "chromedriver.exe")
driver = webdriver.Chrome(service = service)

driver.get("https://cookieclicker.eu/cookieclicker/")

cookie_id = "bigCookie"
cookiesCounter_id = "cookies"
product_price_prefix = "productPrice"
product_prefix = "product"
product_name_id_prefix = "productName"
upgrade_id_prefix = "upgrade"

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Português')]"))
)
language = driver.find_element(By.XPATH, "//*[contains(text(), 'Português')]")
time.sleep(1)
language.click()

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, cookie_id))
)

time.sleep(1)

while True:
    try:
        cookie = driver.find_element(By.ID, cookie_id)
        cookie.click()

        cookies_count = driver.find_element(By.ID, cookiesCounter_id).text.split(" ")[0].replace(","," ")
        cookies_count = int(cookies_count)

        try:
            upgrade_available = driver.find_element(By.CSS_SELECTOR, "#upgrade0.crate.upgrade.enabled")
            if upgrade_available:
                upgrade_available.click()
                print("Comprou um upgrade disponível!")
        except Exception:
            pass

        for i in range(50):
            product_price = driver.find_element(By.ID, product_price_prefix + str(i)).text.split(" ")[0].replace(","," ")
            product_price = int(product_price)

            if cookies_count >= product_price:
                product = driver.find_element(By.ID, product_prefix + str(i))
                product.click()
                product_name = driver.find_element(By.ID, product_name_id_prefix + str(i)).text
                print(f"Comprou {product_name} por {product_price} cookies!")
                print(f"Total de Cookies atualmente: {cookies_count - product_price}")
                break

    except Exception as e:
        continue