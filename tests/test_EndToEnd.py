import json

import pytest

from pageObjects.LoginPage import LoginPage

test_data_path = '/data/test_EndToEnd.json'
with open(test_data_path) as f:
    test_data = json.load(f)
    test_data_list = test_data["data"]
    test_data_list_invalidLogin = test_data["data_invalidLogin"]

@pytest.mark.smoke
@pytest.mark.parametrize("test_data_list_item",test_data_list)
def test_EndToEndTestcase(browserInstance,test_data_list_item):
    driver = browserInstance
    loginPage = LoginPage(driver)
    productsPage = loginPage.login(test_data_list_item["Username"],test_data_list_item["Password"])
    productsPage.sort_products(test_data_list_item["sort_type"])
    productsPage.add_product_to_cart(test_data_list_item["productName"])
    yourCartPage = productsPage.click_Basket()
    informationPage = yourCartPage.click_Checkout()
    overviewPage = informationPage.information_form_fill(test_data_list_item["firstName"],test_data_list_item["lastName"],test_data_list_item["postalCode"])
    finishPage = overviewPage.click_finish()
    finishPage.get_successMessageText()
    finishPage.click_menu_button()
    finishPage.logOut()


@pytest.mark.smoke
@pytest.mark.parametrize("invalidLogin_data",test_data_list_invalidLogin)
def test_invalidLogin(browserInstance,invalidLogin_data):
    driver = browserInstance
    loginPage = LoginPage(driver)
    loginPage.login(invalidLogin_data["Username"],invalidLogin_data["Password"])
    #loginPage.get_locked_out_message()
    loginPage.get_error_message()