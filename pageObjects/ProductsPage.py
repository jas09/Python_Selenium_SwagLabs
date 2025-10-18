from selenium.webdriver.common.by import By

from pageObjects.YourCartPage import YourCartPage
from utils.BrowserUtils import BrowserUtils


class ProductsPage(BrowserUtils):
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver
        self.productCards = (By.XPATH, "//*[@class='inventory_item']")
        self.basketButton = (By.CSS_SELECTOR, "a[href='./cart.html']")
        self.sortDropDown = (By.CSS_SELECTOR,".product_sort_container")

    def add_product_to_cart(self,productName):
        products = self.driver.find_elements(*self.productCards)
        for product in products:
            productName = product.find_element(By.XPATH, "div[2]/a").text
            if productName == productName:
                product.find_element(By.XPATH, "div/button").click()

    def click_Basket(self):
        self.driver.find_element(*self.basketButton).click()
        yourCartPage = YourCartPage(self.driver)
        return yourCartPage