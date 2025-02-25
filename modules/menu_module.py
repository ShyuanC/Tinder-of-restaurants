import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def format_yelp_url(restaurant_name, city_name):
    """Formats the Yelp menu URL based on restaurant and city name"""
    restaurant_name_formatted = "-".join(restaurant_name.lower().split())
    city_name_formatted = "-".join(city_name.lower().split())
    yelp_url = f"https://www.yelp.com/menu/{restaurant_name_formatted}-{city_name_formatted}"
    print(f"Fetching menu from: {yelp_url}")
    return yelp_url


def scrape_yelp_menu(restaurant_name, city_name):
    """Scrapes Yelp menu using Selenium and returns items with both name and price"""
    url = format_yelp_url(restaurant_name, city_name)

    # Configure Selenium WebDriver options
    options = Options()
    options.add_argument("--headless")  # Enable headless mode to run without GUI
    options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent bot detection
    options.add_argument("--window-size=1920x1080")
    options.add_argument("start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds for elements to load

        # Wait for menu items to be present
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//h4 | //td[contains(@class, 'menu-item-price-amount')]")))

        # Scrape menu items
        menu_items = []
        names = driver.find_elements(By.XPATH, "//h4 | //h3")  # Menu item names
        prices = driver.find_elements(By.XPATH,
                                      "//td[contains(@class, 'menu-item-price-amount')] | //li[contains(@class, 'menu-item-price-amount')]")  # Prices

        # Extract menu data, ensuring both name and price are present
        for i in range(min(len(names), len(prices))):  # Ensure we only check pairs
            name = names[i].text.strip()
            price = prices[i].text.strip()

            if name and price:  # Only include items with both name and price
                menu_items.append({"name": name, "price": price})

        return menu_items

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

    finally:
        driver.quit()  # Close the browser


if __name__ == "__main__":
    restaurant = "Earl of Sandwich"
    city = "Tampa"
    menu = scrape_yelp_menu(restaurant, city)

    if menu:
        for item in menu:
            print(f"{item['name']}: {item['price']}")
    else:
        print("No menu items found.")