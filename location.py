from selenium import webdriver
import time
import os

options = webdriver.ChromeOptions()
options.add_argument('--headless')

def content(name):
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com/maps")
    time.sleep(2)

    driver.find_element(by='css selector', value='button.VfPpkd-LgbsSe').click()

    time.sleep(2)

    folder_name = 'images'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    screenshot_path = os.path.join(folder_name, f"location-{name}.png")
    driver.save_screenshot(screenshot_path)

    time.sleep(2)

    driver.quit()

if __name__ == "__main__":
    if not os.path.exists('images'):
        os.makedirs('images')
