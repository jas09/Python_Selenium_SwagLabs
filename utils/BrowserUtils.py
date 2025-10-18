from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class BrowserUtils:
    def __init__(self,driver):
        self.driver = driver

    def get_error_message(self):
        error_text = self.driver.find_element(By.CSS_SELECTOR, "h3").text
        expected_errors = {
            "Username": "Epic sadface: Username is required",
            "Password": "Epic sadface: Password is required",
            "match": "Epic sadface: Username and password do not match any user in this service",
            "locked out": "Epic sadface: Sorry, this user has been locked out."
        }
        for key, expected in expected_errors.items():
            if key in error_text:
                assert expected in error_text
                break
        else:
            raise AssertionError(f"Unexpected error message: {error_text}")

    def sort_products(self, sort_type: str):
        sort_values = {
            "name_az": "az",
            "name_za": "za",
            "price_low_high": "lohi",
            "price_high_low": "hilo"
        }
        if sort_type not in sort_values:
            raise ValueError(f"Invalid sort type: {sort_type}")

        dropdown_element = self.driver.find_element(By.CSS_SELECTOR, ".product_sort_container")
        select = Select(dropdown_element)
        select.select_by_value(sort_values[sort_type])
