import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

channel_list = []
max_channels = 25


# Build Channel list
def build_channel_list():
    print("In Build Channel List")
    channel_numbr = 1
    while channel_numbr <= 30:
        channel_xpath = """//*[@id="contents"]/ytd-channel-renderer[""" + str(channel_numbr) + "]/a"
        channel_list.append(driver.find_element_by_xpath(channel_xpath).get_attribute('href'))
        channel_numbr += 1
    return channel_list


def validate_channels(channel_listt):
    updated_list = []
    for chan in channel_listt:
        # driver.get(chan + "/videos")
        print(chan, "is currently being processed")
        if check_to_process(chan):
            updated_list.append(chan)
            #print(chan, "is removed")
            #channel_listt.remove(chan)
        # driver.back()
    return updated_list


# Checks for topic relevance in
def check_to_process(chan):
    total_count = 0
    relevance_count = 0
    rel_tot = 0
    relevance_percent = 0
    video_views = []
    driver.get(chan + "/videos")
    video_title_elements = driver.find_elements_by_xpath("""//*[@id="video-title"]""")
    for elements in video_title_elements:
        if total_count >= 10:
            break

        # Check for relevance with related terms
        rel_tot += relevant_topics(elements)

        # Check for views
        video_views.append(check_views(elements))

        total_count += 1
    print(rel_tot)
    print
    total_count
    if total_count > 0:
        relevance_percent = (float(rel_tot) / total_count) * 100
    if relevance_percent >= 70:
        print("Relevance_percent : ", relevance_percent, "Relevance Percent Satisfied")
        for v in video_views:
            print
            v
            if int(v) > 2000 or int(v) < 1:
                print("In False")
                return False
        print("In true")
        return True
    else:
        print("Relevance_percent : ", relevance_percent, "Relevance Percent Not Satisfied")
        return False


def relevant_topics(title):
    title_string = title.get_attribute('title')
    if any(s in title_string for s in ("Dota 2", "DOTA 2", "Dota2", "DOTA2")):
        return 1
    else:
        return 0


def check_views(views):
    video_views_raw = views.get_attribute('aria-label')
    return (int(video_views_raw.split(' ')[-2].replace(",", "")))


# Main Starts here

##Base URL contains channel filter
url_base = "https://www.youtube.com/results?sp=EgIQAkIECAESAA%253D%253D&search_query="
url_search_query = "dota+2+heroes+gameplay"

##Invoke Driver and get URL
driver = webdriver.Chrome(r"C:\Users\adhei\Anaconda2\selenium\webdriver\chrome\chromedriver.exe")
driver.get(url_base + url_search_query)

##Scroll down page to load and get more results and retrieve all results
elem = driver.find_element_by_tag_name("body")
no_of_pagedowns = 20

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns -= 1

channel_listt = build_channel_list()
print("Completed Build Channel List")
empt_list = []
empt_list = validate_channels(channel_listt)
print (empt_list)

##Extract titles
# title = driver.find_elements_by_xpath('//*[@id="channel-title"]/span')
# for t in title:
#    print t.text

