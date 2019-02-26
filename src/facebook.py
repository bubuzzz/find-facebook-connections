import requests
from bs4 import BeautifulSoup
from selenium import webdriver

FACEBOOK_URL = 'https://m.facebook.com/'
FACEBOOK_MAIN_URL = "https://www.facebook.com/"
DEPTH = 3
FACEBOOK_FRIENDS_THRESHOLD = 50


def login_firefox():
    """
    Use Selenium to open firefox and wait for user to login
    """
    firefox_profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(firefox_profile=firefox_profile)
    driver.get(FACEBOOK_MAIN_URL)

    while True:
        try:
            login_signifier = driver.find_element_by_class_name("innerWrap")
            break
        except:
            continue

    cookies = driver.get_cookies()
    driver.quit()

    return cookies


def parse_cookies(cookies):
    """
    Parse the cookies from selenium to the correct format of Facebook
    """
    formatted = {}
    for cook in cookies:
        formatted[cook['name']] = cook['value']

    return formatted


def extract_friends(raw_html):
    """
    Extract the friend list of the current friend page. Return the friend list
    and the next pagination link
    """
    friends = {}
    next_link = None

    content = BeautifulSoup(raw_html, features="html.parser").find('div', {"id": "root"})
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
    """
    Go to the friend page of a user, then continue to navigate through the
    list of the friend
    """
    startidx = 0
    friends = {}
    done = False
    while not done:
        r = requests.get(friend_url, cookies=cookies)
        new_friends, next_link = extract_friends(r.text)
        friends.update(new_friends)
        if next_link is None or len(friends) >= FACEBOOK_FRIENDS_THRESHOLD:
            done = True
        else:
            friend_url = FACEBOOK_URL + next_link

    return friends


def crawl_friends():
    raw_cookies = login_firefox()
    cookies = parse_cookies(raw_cookies)

    r = requests.get('%sme' % FACEBOOK_MAIN_URL, cookies=cookies)
    username = r.url.split('/')[-1].split('?')[0]
    url = FACEBOOK_URL + username + '/friends'

    friends = get_friends_of(url, cookies)
    print friends


class Node:
    def __init__(self, username, children=None):
        self.username = username
        self.children = children

    def generate_tree(self):
        tree     = dict()
        current  = tree[self.username] = dict()
        friends  = current['friends'] = dict()
        children = self.children

        if children:
            for child in children:
                friends.update(child.generate_tree())
        return tree


class FacebookClient:
    def __init__(self, cookies=None):
        if cookies:
            self.cookies = cookies
        else:
            print "No cookies provided, start logging in..."
            raw_cookies = login_firefox()
            self.cookies = parse_cookies(raw_cookies)
            print "Cookies: ", self.cookies

    def get_friends(self, username):
        url = FACEBOOK_URL + username + '/friends'
        friends = get_friends_of(url, self.cookies)
        return [Node(friend_username) for friend_username in friends.keys()]

    def get_myself_username(self):
        r = requests.get('%sme' % FACEBOOK_URL, cookies=self.cookies)
        username = r.url.split('/')[-1].split('?')[0]
        return Node(username)
