from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
import json
from selenium_stealth import stealth
import time

usernames = ['emi.ciappi', 'shakira'] #usernames to be scraped
proxy = "server:port"
output = {}

def prepare_browser(): # set driver

    chrome_options = webdriver.ChromeOptions()
    
    chrome_options.add_argument(f'--proxy-server={proxy}') #add proxies to the bowser options
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options= chrome_options)

    #get more anonimity
    stealth(driver, 
            user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
            languages= ["en-US", "en"],
            vendor= "Google Inc.",
            platform= "Win32",
            webgl_vendor= "Intel Inc.",
            renderer= "Intel Iris OpenGL Engine",
            fix_hairline= False,
            run_on_insecure_origins= False,)
    
    return driver


def parse_data(username, user_data): #function that will get the data that I want from the json
    #get some post captions from publicly available posts
    captions = []
    if len(user_data['edge_owner_to_timeline_media']['edges']) > 0:
        for node in user_data['edge_owner_to_timeline_media']['edges']:
            if len(node['node']['edge_owner_to_caption']['edges']) > 0:
                if node['node']['edge_owner_to_caption']['edges']['0']['node']['text']:
                    captions.append(node['node']['edge_media_to_caption']['edges']['0']['node']['text'])
    
    # get full names, the category they belong to, and the number of followers they have.

    output[username] = {
        'name' : user_data['full_name'],
        'category': user_data['catergory_name'],
        'followers': user_data['edge_followed_by']['count'],
        'post': captions 
    }

def scrape(username):
    
    url = f'https://www.instagram.com/{username}/?__a=1&__d=dis'
    chrome = prepare_browser()
    chrome.get(url)
    time.sleep(5)
    
    print(f"Attemping: {chrome.current_url}")
    if "login" in chrome.current_url:
        print("Failed/ redir to login")
        chrome.quit()
        time.sleep(5)
    else:
        print("Success")
        resp_body = chrome.find_element(By.TAG_NAME, "body").text
        data_json = json.loads(resp_body)
        user_data = data_json['graphql']['user']
        parse_data(username, user_data)
        chrome.quit()
        time.sleep(5)

def main():
    for username in usernames: #loop going through usernames
        scrape(username)



if __name__ == '__main__':
    main()
    pprint(output)
