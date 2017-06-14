from selenium import webdriver
import time
from settings import FB_LOGIN, FB_PASSWORD
import json
from xvfbwrapper import Xvfb
#from polyglot.detect import Detector, base

def read_from_file(filename):
    with open(filename, "r") as f:
        s = f.readlines()
        news = ''
        for stringg in s:
            news += stringg

        myjson = json.loads(news)
    return myjson

with Xvfb() as xvfb:
    browser = webdriver.Firefox()

    tips = {}


    def fb_login(browser, user):
        browser.get('https://www.facebook.com')

        login = browser.find_element_by_id('email')
        password = browser.find_element_by_id('pass')
        button = browser.find_element_by_id('u_0_q')

        login.send_keys(user['login'])
        password.send_keys(user['password'])
        button.click()


    def fb_reviews(browser, url):
        tips_one_place = []
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
                rating = block.find_element_by_css_selector("h5 .fcg i u")
                content = block.find_element_by_css_selector(".userContent")
            except:
                try:
                    name = block.find_element_by_css_selector("h5 .fwb .profileLink").text
                    profile = ''
                    rating = block.find_element_by_css_selector("h5 .fcg i u")
                    content = block.find_element_by_css_selector(".userContent")
                except:
                    continue

                print(content.text)
            if(content.text):
                # try:
                #     lang_detector = Detector(content.text)
                #     ukr = lang_detector.language.name == "Ukrainian"
                # except base.UnknownLanguage:
                #     continue
                # if ukr:
                tips_one_place.append([name, profile, content.text, rating.text])
                print(name)
                print(profile)
                print("len" + str(len(content.text)))
                print("text " + content.text)
                print(rating.text)
                print()
        return tips_one_place



    user = {'login': FB_LOGIN, 'password': FB_PASSWORD}

    # fb_login(browser, user)

    count = 0

    places = read_from_file("tips/fb_places.json")
    i = 0
    for place in places:
        tips[place] = fb_reviews(browser, places[place])
        count += len(tips[place])
        i += 1
        if i == 10:
            with open("facebook_rewiews.json", "a") as file:
                file.write(json.dumps(tips, ensure_ascii=False))
            i = 0
            tips = {}
            print("Numb of tips: " + str(count))


    time.sleep(10)
    browser.quit()

#with open("facebook_rewiews.json", "a") as file:
 #   file.write(json.dumps(tips, ensure_ascii=False))

print("Numb of tips: " + str(count))
