from selenium.webdriver.common.by import By

from pageObjects.OverviewPage import OverviewPage
from utils.BrowserUtils import BrowserUtils


class InformationPage(BrowserUtils):
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver
        self.firstName = (By.ID, "first-name")
        self.lastName = (By.ID, "last-name")
        self.postalCode = (By.ID, "postal-code")
        self.continueButton = (By.CSS_SELECTOR, "input[type='submit']")

    def information_form_fill(self,firstName,lastName,postalCode):
        self.driver.find_element(*self.firstName).send_keys(firstName)
        self.driver.find_element(*self.lastName).send_keys(lastName)
        self.driver.find_element(*self.postalCode).send_keys(postalCode)
        self.driver.find_element(*self.continueButton).click()
        overviewPage = OverviewPage(self.driver)
        return overviewPage
