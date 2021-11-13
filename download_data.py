from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import chromedriver_binary
from selenium.webdriver.common.by import By
import os
import zipfile

def download_data(directory, data_url):
    options = webdriver.ChromeOptions() 
    prefs = {"download.default_directory":directory}
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(options = options)
    # Open page
    driver.get(data_url)
    sleep(2)
    # Go through each relevant row on page and download files from past twelve months
    table = driver.find_element(By.XPATH, "//table[@class='hide-while-loading table table-striped']")
    for row in table.find_elements(By.XPATH, ".//tr")[1:]:
        row_element = row.find_elements(By.TAG_NAME, 'a')[0]
        # Using try/except because older files do not share the same naming format.
        try: 
            year_month = int(row_element.text[:6])
            if year_month >= 202011:
                row_element.click()
                sleep(1)
        except: 
            continue
    # Give time to let files finish downloading
    sleep(10)
    # Unzip files
    for file_name in os.listdir(directory).copy():
        file_path = os.path.join(directory,file_name)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(directory)
        os.remove(file_path)
    # Close page
    driver.close()