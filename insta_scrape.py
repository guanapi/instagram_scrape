from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
import json
from selenium_stealth import stealth

usernames = ["jilo", "shakira", "beyonce", "kattyperry"] #usernames to be scraped

proxy = "server:port"

output = {}

def main():
    for username in usernames: #loop going through usernames
        scrape(username)

def prepare_browser(): # set driver

    chromme_options = webdriver.ChromeOptions()
    chromme_options.add_argument(f'--proxy-server={proxy}') #add proxies to the bowser options
    chromme_options.add_argument("start-maximized")
    chromme_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chromme_options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options= chromme_options)

    #get more anonimity
    stealth(driver, user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
            languages= ["en-US", "en"],
            vendor= "Google Inc.",
            platform= "Win32",
            webgl_vendor= "Intel Inc.",
            renderer= "Intel Iris OpenGL Engine",
            fix_hairline= False,
            run_on_insecure_origins= False,)
    
    return driver

if __name__ == '__main__':
    main()
    pprint(output)
