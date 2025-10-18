from selenium.webdriver.common.by import By

from pageObjects.FinishPage import FinishPage
from utils.BrowserUtils import BrowserUtils


class OverviewPage(BrowserUtils):
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver
        self.finishButton = (By.XPATH, "//a[text()='FINISH']")


    def click_finish(self):
        self.driver.find_element(*self.finishButton).click()
        finishPage = FinishPage(self.driver)
        return finishPage