from selenium.webdriver.common.by import By

from pageObjects.InformationPage import InformationPage
from utils.BrowserUtils import BrowserUtils


class YourCartPage(BrowserUtils):
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver
        self.checkOutButton = (By.CSS_SELECTOR, ".checkout_button")

    def click_Checkout(self):
        self.driver.find_element(*self.checkOutButton).click()
        informationPage = InformationPage(self.driver)
        return informationPage