import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from proxy_auth_extension import create_proxy_auth_extension
from concurrent.futures import ThreadPoolExecutor
import requests

def setup_driver():
    """Sets up the Selenium WebDriver with a proxy extension."""

    # Load environment variables from .env file
    load_dotenv()

    """Retrieve proxy authentication details from environment variables
        If you haven't, buy residential proxies from Oxylabs:
            https://oxylabs.io/
            then create user credentials
                to be able to scrape the target website. Otherwise, your requests will return 403.
    """
    username = os.getenv("OXYLABS_USERNAME")
    password = os.getenv("OXYLABS_PASSWORD")
    proxy_host = "pr.oxylabs.io"
    proxy_port = 7777

    """Create the proxy authentication extension for Selenium. 
        Full extension details on GitHub: 
            https://github.com/Stevealila/Proxy-Auth-Extension"""
    proxy_auth_extension = create_proxy_auth_extension(proxy_host, int(proxy_port), username, password)

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_extension(proxy_auth_extension)  # Add proxy extension
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    # Return the configured WebDriver instance
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

def scrape_images(animal_type, driver, max_images=100):
    """Scrapes a specified number of images for a given animal type from Pexels."""

    # Construct the search URL for the animal type
    url = f"https://www.pexels.com/search/{animal_type}/"
    driver.get(url)

    # Wait until images are loaded on the page
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "img[src^='https://images.pexels.com/photos/']"))
    )

    # Use a set to store unique image URLs
    image_urls = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(image_urls) < max_images:
        # Find image elements on the page
        img_elements = driver.find_elements(By.CSS_SELECTOR, "img[src^='https://images.pexels.com/photos/']")
        
        # Extract and store the image URLs
        for img in img_elements:
            src = img.get_attribute('src')
            if src:
                image_url = src.split('?')[0]  # Remove query parameters
                if image_url.endswith(('.jpg', '.jpeg', '.png')):
                    image_urls.add(image_url)  # Add to set for uniqueness
                    if len(image_urls) >= max_images:
                        return list(image_urls)  # Return early if max images reached

        # Scroll down to load more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new images to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # Break loop if no more images are loaded
            break
        last_height = new_height

    return list(image_urls)  # Convert set to list and return

def download_image(url, folder_path, file_name):
    """Downloads an image from the given URL and saves it to the specified folder."""

    try:
        # Send a GET request to download the image
        response = requests.get(url, timeout=10)
        if response.status_code == 200:  # Check if request was successful
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'wb') as f:
                f.write(response.content)  # Save image content to file
            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download: {url}. Status code: {response.status_code}")
    except Exception as e:
        # Handle exceptions during download
        print(f"Failed to download: {url}. Error: {str(e)}")

def download_images(image_urls, animal_type):
    """Downloads all images for a given animal type using multithreading."""

    # Create directory to save images
    folder_path = os.path.join("datasets/animal_images", animal_type)
    os.makedirs(folder_path, exist_ok=True)
    
    # Use ThreadPoolExecutor to download images concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(download_image, url, folder_path, f"{animal_type}_{i+1}{os.path.splitext(url)[1]}")
            for i, url in enumerate(image_urls)
        ]
        for future in futures:
            future.result()  # Wait for all downloads to complete

def main():
    """Main function to scrape and download images for different animal types."""

    # Define the types of animals to search for
    animal_types = ["cat", "dog", "monkey", "cow", "bird"]
    driver = setup_driver()  # Initialize the WebDriver

    try:
        for animal in animal_types:
            print(f"Scraping images for: {animal}")
            image_urls = scrape_images(animal, driver, max_images=100)
            if image_urls:
                download_images(image_urls, animal)  # Download the images if found
                print(f"Finished scraping {animal} images\n")
            else:
                print(f"No images found for {animal}\n")
            time.sleep(3)  # Wait between scraping different animal types
    finally:
        driver.quit()  # Ensure the WebDriver is properly closed

if __name__ == "__main__":
    main()
