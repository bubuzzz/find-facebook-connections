from selenium import webdriver
import requests
from bs4 import BeautifulSoup

def login_firefox():
    firefox_profile = webdriver.FirefoxProfile()
    driver          = webdriver.Firefox(firefox_profile=firefox_profile)
    driver.get("http://www.facebook.com")

    while True:
        try:
            loginSignifier = driver.find_element_by_class_name("innerWrap")
            break
        except:
            continue

    cookies = driver.get_cookies()
    driver.quit()

    return cookies

def parse_cookies(cookies):
    formatted= {}
    for cook in cookies:
        formatted[cook['name']] = cook['value']

    return formatted

def extract_friends(raw_html):
    content   = BeautifulSoup(raw_html).find('div', {"id": "root"})
    links     = content.find_all("a")

    friends   = {}
    next_link = None

    for l in links:
        href     = l['href']
        if 'fref=fr_tab' in str(href):
            user = {}
            username = href[1:].split('?')[0]
            friends[href] = l.text
        if "See more friends" in str(l):
            next_link = href

    return friends, next_link

def get_friends_of(username, cookies):
    startidx = 0
    friends  = {}
    done     = False
    facebook_url = 'https://m.facebook.com/'
    url =  facebook_url + username + '/friends'
    while not done:
        r = requests.get(url, cookies=cookies)
        new_friends, next_link = extract_friends(r.text)
        friends.update(new_friends)
        if next_link == None:
            done =  True
        else:
            url = facebook_url + next_link

    return friends

def crawl_friends():
    raw_cookies = login_firefox()
    cookies     = parse_cookies(raw_cookies)
    r           = requests.get('https://m.facebook.com/me', cookies = cookies)
    username    = r.url.split('/')[-1].split('?')[0]

    return get_friends_of(username, cookies)

