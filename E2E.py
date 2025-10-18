import time

from selenium import webdriver
from selenium.webdriver.common.by import By

#ProductList = ['Sauce Labs Backpack', 'Sauce Labs Bike Light', 'Sauce Labs Bolt T-Shirt', 'Sauce Labs Fleece Jacket', 'Sauce Labs Onesie', 'Test.allTheThings() T-Shirt (Red)']
driver = webdriver.Edge()
driver.implicitly_wait(3)
driver.get("https://www.saucedemo.com/v1/index.html")
driver.find_element(By.NAME,"user-name").send_keys("standard_user")
driver.find_element(By.ID,"password").send_keys("secret_sauce")
driver.find_element(By.CSS_SELECTOR,"input[type='submit']").click()
actualText = driver.find_element(By.XPATH,"//div[text()='Products']").text
assert "Products" == actualText
products = driver.find_elements(By.XPATH,"//*[@class='inventory_item']")
for product in products:
    productName = product.find_element(By.XPATH,"div[2]/a").text
    if productName == "Sauce Labs Backpack":
        product.find_element(By.XPATH,"div/button").click()
driver.find_element(By.CSS_SELECTOR,"a[href='./cart.html']").click()
driver.find_element(By.CSS_SELECTOR,".checkout_button").click()
driver.find_element(By.ID,"first-name").send_keys("Azharulla")
driver.find_element(By.ID,"last-name").send_keys("Mohammed")
driver.find_element(By.ID,"postal-code").send_keys("560036")
driver.find_element(By.CSS_SELECTOR,"input[type='submit']").click()
driver.find_element(By.XPATH,"//a[text()='FINISH']").click()
actualMessage = driver.find_element(By.CSS_SELECTOR,"h2").text
assert "THANK YOU FOR YOUR ORDER" == actualMessage
driver.find_element(By.CSS_SELECTOR,".bm-burger-button").click()
driver.find_element(By.XPATH,"//nav[@class='bm-item-list']/a[3]").click()



