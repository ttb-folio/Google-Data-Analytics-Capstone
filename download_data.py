from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import chromedriver_binary
from selenium.webdriver.common.by import By

def download_data(directory):
    
    data_url = "https://divvy-tripdata.s3.amazonaws.com/index.html"

    options = webdriver.ChromeOptions() 
    prefs = {"download.default_directory":directory}
    options.add_experimental_option("prefs",prefs)
    
    driver = webdriver.Chrome(options = options)
    driver.get(data_url)
    sleep(2)
    
    table = driver.find_element_by_xpath("//table[@class='hide-while-loading table table-striped']")
    
    for row in table.find_elements(By.XPATH, ".//tr")[1:]:
        sleep(1)
        row.find_elements(By.TAG_NAME, 'a')[0].click()
    
    sleep(2)
    driver.close()