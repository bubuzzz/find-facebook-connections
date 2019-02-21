import requests
from bs4 import BeautifulSoup
from selenium import webdriver

facebook_url = 'https://m.facebook.com/'
DEPTH = 3


def login_firefox():
    firefox_profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(firefox_profile=firefox_profile)
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
    formatted = {}
    for cook in cookies:
        formatted[cook['name']] = cook['value']

    return formatted


def extract_friends(raw_html):
    friends = {}
    next_link = None

    content = BeautifulSoup(raw_html).find('div', {"id": "root"})
    links = content.find_all("a")

    for l in links:
        href = l.get('href')
        if href and 'fref=fr_tab' in href.encode("utf-8"):
            username = href[1:].replace('?fref=fr_tab', '')
            friends[username] = {'name': l.text, 'username': username}
        if "See more friends" in str(l):
            next_link = href

    return friends, next_link


def get_friends_of(friend_url, cookies):
    startidx = 0
    friends = {}
    done = False
    while not done:
        r = requests.get(friend_url, cookies=cookies)
        new_friends, next_link = extract_friends(r.text)
        friends.update(new_friends)
        if next_link == None:
            done = True
        else:
            friend_url = facebook_url + next_link

    return friends


def crawl_friends():
    raw_cookies = login_firefox()
    cookies = parse_cookies(raw_cookies)

    r = requests.get('https://m.facebook.com/me', cookies=cookies)
    username = r.url.split('/')[-1].split('?')[0]
    url = facebook_url + username + '/friends'

    friends = get_friends_of(url, cookies)
    print friends


class FacebookClient:
    def __init__(self, cookies=None):
        if cookies:
            self.cookies = cookies
        else:
            print "No cookies provided, start logging in..."
            raw_cookies = login_firefox()
            self.cookies = parse_cookies(raw_cookies)
            print "cookies: ", self.cookies

    def get_children(self, username):
        url = facebook_url + username + '/friends'
        return get_friends_of(url, self.cookies)

    def get_myself_username(self):
        r = requests.get('https://m.facebook.com/me', cookies=self.cookies)
        username = r.url.split('/')[-1].split('?')[0]
        return {'username': username}
