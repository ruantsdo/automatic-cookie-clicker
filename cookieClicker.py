from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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

def clickOnSuperCookie():
    cookie = driver.find_element(By.ID, cookie_id)
    cookie.click()

def getCookiesCount():
    cookies_count = driver.find_element(By.ID, cookiesCounter_id).text.split(" ")[0].replace(","," ")
    cookies_count = int(cookies_count)
    return cookies_count

def checkUpgradeAvailability():
        try:
            upgrade_available = driver.find_element(By.CSS_SELECTOR, "#upgrade0.crate.upgrade.enabled")
            if upgrade_available:
                upgrade = driver.find_element(By.CSS_SELECTOR, ".upgrade")
                ActionChains(driver).move_to_element(upgrade).perform()

                wait = WebDriverWait(driver, 10)

                upgrade_name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#tooltip .name"))).text
                upgrade_price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#tooltip .price"))).text

                upgrade_available.click()
                print(f"Comprou o upgrade '{upgrade_name}' por {upgrade_price} cookies!")
        except Exception:
            pass

def checkProductAvailability():
    searchProductsAvailable = driver.find_elements(By.CLASS_NAME, "product.unlocked.enabled")
    productsAvailable = len(searchProductsAvailable)

    cookies_count = getCookiesCount()

    for i in range(productsAvailable, -1, -1):
            product_price = driver.find_element(By.ID, product_price_prefix + str(i)).text.split(" ")[0].replace(","," ")
            product_price = int(product_price)

            if cookies_count >= product_price:
                product = driver.find_element(By.ID, product_prefix + str(i))
                product.click()
                product_name = driver.find_element(By.ID, product_name_id_prefix + str(i)).text
                print(f"Comprou '{product_name}' por {product_price} cookies!")
                break


WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Português')]"))
)
language = driver.find_element(By.XPATH, "//*[contains(text(), 'Português')]")
language.click()

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, cookie_id))
)

time.sleep(1)

while True:
    try:
        clickOnSuperCookie()
        checkUpgradeAvailability()
        checkProductAvailability()

    except Exception as e:
        continue