from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys, os

if __name__ == "__main__":
    pathname = os.path.dirname(sys.argv[0])    
    browser = webdriver.Firefox(executable_path=pathname+'/geckodriver')
    browser.get('https://gabrielecirulli.github.io/2048/')
    body = browser.find_element_by_xpath('/html/body')
    while True:
        body.send_keys(Keys.UP)
        body.send_keys(Keys.RIGHT)
        body.send_keys(Keys.DOWN)
        body.send_keys(Keys.LEFT)

    
