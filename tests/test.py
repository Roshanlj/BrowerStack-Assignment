import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions

# The webdriver management will be handled by the browserstack-sdk
# so this will be overridden and tests will run browserstack -
# without any changes to the test files!
options = ChromeOptions()
options.set_capability('sessionName', 'BStack Sample Test')
driver = webdriver.Chrome(options=options)

try:
    driver.get('https://www.flipkart.com/')
    
    # Search for the product "Samsung Galaxy S10"
    search_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'q')))
    search_input.click()
    search_input.send_keys('Samsung Galaxy S10')
    search_input.submit()

    # Click on "Mobiles" in categories
    mobiles_category = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//div[@class="esFpML"]')))
    mobiles_category.click()

    # Apply filters
    brand_checkbox = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//div[@class="XqNaEv"]')))
    brand_checkbox.click()
    
    flipkart_assured_filter = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//div[@class="XqNaEv eJE9fb"]')))
    flipkart_assured_filter.click()

    # Sort by Price - High to Low
    price_high_to_low = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.XPATH, '//div[text()="Price -- High to Low"]')))
    price_high_to_low.click()

    # Extract product details
    products = []
    product_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="cPHDOP col-12-12"]')))
    for product_element in product_elements:
        try:
            product_name = WebDriverWait(product_element, 5).until(EC.presence_of_element_located((By.XPATH, './/div[@class="KzDlHZ"]'))).text
            display_price = WebDriverWait(product_element, 5).until(EC.presence_of_element_located((By.XPATH, './/div[@class="hl05eU"]'))).text
            product_link = WebDriverWait(product_element, 5).until(EC.presence_of_element_located((By.XPATH, './/a[@class="CGtC98"]'))).get_attribute('href')
        
            products.append({
                'Product Name': product_name.strip(),
                'Display Price': display_price.strip(),
                'Link to Product Details Page': product_link
            })
        except Exception as e:
            print("An error occurred:", e)

    # Print the list of products
    for product in products:
        print(product)

    # Set the status of test as 'passed'
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Test executed successfully"}}')

except NoSuchElementException as err:
    message = 'Exception: ' + str(err.__class__)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
except Exception as err:
    message = 'Exception: ' + str(err.__class__)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
finally:
    # Stop the driver
    driver.quit()
