import time
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from amazon_config import(
    get_chrome_web_driver,
    get_web_driver_options,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    NAME,
    CURRENCY,
    FILTERS,
    BASE_URL,
    DIRECTORY,
)

class GenerateReport:
    def __init__(self):
        pass

class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = currency 
        self.price_filter = f"&rh=p_36%3A{ filters['min']}00-{filters['max']}00"

        pass
    def run(self):
        print("Starting script.....")
        print(f"Looking for {self.search_term} products...")
        links = self.get_products_links()
        time.sleep(3)
        if not links:
            print("Stopped script.")
            return
        print(f"Got {len(links)} links to products...")
        print("Getting info about products...")
        products = self.get_products_info(links)

        self.driver.quit()

    def get_products_info(self, links):
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            product = self.get_single_product_info(asin)

    def get_single_product_info(self, asin):
        print(f"Product ID: {asin} - Getting Data...")
        product_short_url = self.shorten_url(asin)
        self.driver.get(f'{product_short_url}?language=en_GB')
        time.sleep(2)
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()

    def get_title(self):
        try:
            return self.driver.find_element(By.ID, ('productTitle').text)
        except Exception as e:
            print(e)
            print(f"Can't get title of a product - {self.driver.current_url}")
            return None
    def get_seller(self):
        try:
            return self.driver.find_element(By.ID, ('bylineInfo').text)
        except Exception as e:
            print(e)
            print(f"Can't get the seller of a product - {self.driver.current_url}")
            return None

    def get_price(self):
        return '99$'
    
    def shorten_url(self, asin):
        return self.base_url + 'dp/' + asin


    def get_asins(self, links):
        return [self.get_asins(links) for link in links]

    def get_asin(self, product_link):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]


    def get_products_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER) 
        time.sleep(2)
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        time.sleep(2)
        result_list = self.driver.find_element(By.CLASS_NAME, 's-result-list')
        
        links = [] 
        try:
            results = result_list.find_elements(By.XPATH,
               ('//div/span/div/div/div[2]/div[2]/div/div/div[1]/h2/a')[0])
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print("Didn't get any products...")
            print(e)
            return links


if __name__ == '__main__':
    print("Hey!! ")
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL , CURRENCY)
    amazon.run()