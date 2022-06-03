import os.path
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
import re

login = 'vitaliy1234564'
password = 'Ildar0880'
link =  'https://steamcommunity.com/'
skin_arr = ["https://steamcommunity.com/market/listings/730/SG%20553%20%7C%20Army%20Sheen%20%28Factory%20New%29"]

chrome_options = Options()
chrome_options.add_extension('/Users/danilserbakov/Downloads/extension_2_4_3_0.crx')
chrome_options.add_extension('/Users/danilserbakov/Downloads/extension_4_4_0_0.crx')
# инициализируем драйвер браузера. После этой команды вы должны увидеть новое открытое окно браузера

class Bot:

    def __init__(self):
        self.user = login
        self.password = password
        self.driver = webdriver.Chrome(options=chrome_options)
        self.cookie = "cookies.pickle"
        self.skins_array = skin_arr

    def quit(self):
        self.driver.close()
        self.driver.quit()

    def log_in(self):
        driver = self.driver
        driver.get(link)
        time.sleep(1)
        if os.path.exists(self.cookie):
            self.load_cookie()
            self.driver.refresh()
            time.sleep(1)
        else:
            self.driver.find_element(By.CLASS_NAME, 'global_action_link').click()
            time.sleep(2)

            self.driver.find_element(By.NAME, 'username').send_keys(login)
            time.sleep(1)

            self.driver.find_element(By.NAME, 'password').send_keys(password)
            time.sleep(1)

            self.driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
            time.sleep(2)

            self.guard()
            time.sleep(5)
            self.save_cookie()

    def guard(self):
        code = input("steam guard")
        self.driver.find_element(By.XPATH, "//input[@id='twofactorcode_entry']").send_keys(code)
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "div[type=submit]").click()
        time.sleep(3)

    def save_cookie(self):
        with open(self.cookie, "wb") as f:
            pickle.dump(self.driver.get_cookies(), f)

    def load_cookie(self):
        with open(self.cookie, "rb") as f:
            cookies = pickle.load(f)
            for cook in cookies:
                self.driver.add_cookie(cook)

    def trade_hub(self):
        community = self.driver.find_element(By.XPATH, "//a[@class='menuitem supernav username persona_name_text_content'][contains(text(),'данила афтершок')]")
        ActionChains(self.driver).move_to_element(community).perform()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//div[@class='supernav_content']//a[@class='submenuitem'][contains(text(),'Инвентарь')]").click()

    def skin(self, url):
        self.driver.get(url)
        time.sleep(2)
        select = Select(self.driver.find_element(By.XPATH,"//select[@id='pageSize']"))
        select.select_by_visible_text('100')
        time.sleep(2)
        def_price = self.min_price()
        time.sleep(2)
        min_price_page=self.min_price()
        while  min_price_page < def_price * 1.25:
            self.page( def_price)
            time.sleep(4)
            min_price_page = self.min_price()

    def page(self, def_price ):
        item_arr = self.driver.find_elements(By.CLASS_NAME, "market_listing_item_name_block")[0:100]
        for item in item_arr:
            skin_float = float(item.find_element(By.CLASS_NAME, "csgofloat-itemfloat").text[7:])
            id = item.find_element(By.CSS_SELECTOR, ".market_listing_item_name.economy_item_hoverable").get_attribute(
                'id')
            id  = re.sub("[^0-9]", "", id)
            skin_price = float(self.driver.find_element(By.XPATH,
                                                        "//div[@id='listing_" + id + "']//span[@class='market_listing_price market_listing_price_with_fee']").text[
                               :-5].replace(",", "."))
            if skin_float < 0.027 and skin_price < 1.25 * def_price:
                print(skin_price)
        self.driver.find_element(By.XPATH, "//span[@id='searchResults_btn_next']").click()

    def min_price(self):
        price = min(map(lambda item: float(item.text[:-5].replace(",", ".")), self.driver.find_elements(By.CSS_SELECTOR,".market_listing_price.market_listing_price_with_fee")))
        return price

    def float_auto(self):
        for link in self.skins_array:
            self.skin(link)
            time.sleep(2)


bot = Bot()

if __name__ == "__main__":
    bot.log_in()
    time.sleep(3)
    bot.float_auto()
    time.sleep(5)
    bot.quit()
