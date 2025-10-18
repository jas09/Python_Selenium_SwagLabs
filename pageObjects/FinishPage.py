from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from utils.BrowserUtils import BrowserUtils


class FinishPage(BrowserUtils):
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver
        self.orderSuccess = (By.CSS_SELECTOR, "h2")
        self.menuButton = (By.CSS_SELECTOR, ".bm-burger-button")
        self.logOutButton = (By.XPATH, "//nav[@class='bm-item-list']/a[3]")

    def get_successMessageText(self):
        actualMessage = self.driver.find_element(*self.orderSuccess).text
        assert "THANK YOU FOR YOUR ORDER" == actualMessage

    def click_menu_button(self):
        self.driver.find_element(*self.menuButton).click()

    def logOut(self):
        wait = WebDriverWait(self.driver,5)
        wait.until(expected_conditions.presence_of_element_located(self.logOutButton))
        self.driver.find_element(*self.logOutButton).click()