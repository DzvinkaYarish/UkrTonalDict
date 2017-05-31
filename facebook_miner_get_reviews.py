from selenium import webdriver
import time
from settings import FB_LOGIN, FB_PASSWORD
from facebook_miner_get_places import get_places

browser = webdriver.Firefox()


def fb_login(browser, user):
    browser.get('https://www.facebook.com')

    login = browser.find_element_by_id('email')
    password = browser.find_element_by_id('pass')
    button = browser.find_element_by_id('u_0_q')

    login.send_keys(user['login'])
    password.send_keys(user['password'])
    button.click()


def fb_reviews(browser, url):
    #url = "https://www.facebook.com/pg/%s/reviews/" % pg_name
    browser.get(url)

    while len(browser.find_elements_by_css_selector('.uiMorePager')) > 2:
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    blocks = browser.find_elements_by_css_selector('.fbUserContent')
    # print(len(blocks))
    for block in blocks:
        try:
            name_block = block.find_element_by_css_selector("h5 .fwb a")
            profile = name.get_attribute('href')
            name = name_block.text
        except:
            name = block.find_element_by_css_selector("h5 .fwb .profileLink").text
            profile = ''
        rating = block.find_element_by_css_selector("h5 .fcg i u")
        content = block.find_element_by_css_selector(".userContent")
        print(name)
        print(profile)
        print(content.text)
        print(rating.text)
        print()


user = {'login': FB_LOGIN, 'password': FB_PASSWORD}

# fb_login(browser, user)
places  = get_places()
for place in places:

    fb_reviews(browser, places[place])

time.sleep(10)
browser.quit()
