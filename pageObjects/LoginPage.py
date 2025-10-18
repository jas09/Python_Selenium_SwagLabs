from selenium.webdriver.common.by import By
from pageObjects.ProductsPage import ProductsPage
from utils.BrowserUtils import BrowserUtils

class LoginPage(BrowserUtils):
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver
        self.username = (By.NAME, "user-name")
        self.password = (By.ID, "password")
        self.loginButton = (By.CSS_SELECTOR, "input[type='submit']")

    def login(self,username,password):
        self.driver.find_element(*self.username).send_keys(username)
        self.driver.find_element(*self.password).send_keys(password)
        self.driver.find_element(*self.loginButton).click()
        productsPage = ProductsPage(self.driver)
        return productsPage


