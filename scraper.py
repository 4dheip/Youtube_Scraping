import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


##Base URL contains channel filter
url_base = "https://www.youtube.com/results?sp=EgIQAkIECAESAA%253D%253D&search_query="
url_search = "dota+2+heroes+gameplay"

##Invoke Driver and get URL
driver = webdriver.Chrome(r"C:\Users\adhei\Anaconda2\selenium\webdriver\chrome\chromedriver.exe")
driver.get(url_base+url_search)

##Scroll down page to load and get more results
#elem = driver.find_element_by_tag_name("body")
#no_of_pagedowns = 20
#while no_of_pagedowns:
#    elem.send_keys(Keys.PAGE_DOWN)
#    time.sleep(0.2)
#    no_of_pagedowns-=1


#Checks for topic relevance in 
def check_to_process():
    total_count = 0
    relevance_count = 0
    rel_tot = 0
    video_titles = driver.find_elements_by_xpath("""//*[@id="video-title"]""")
    for titles in video_titles:
        if total_count >= 10:
            break
        rel_tot += relevant_topics(titles,relevance_count)
        print("Rel to",rel_tot," Total Iterations:",total_count)
        #title_string = titles.get_attribute('title')
        video_views = titles.get_attribute('aria-label')
        #print title_string
        total_count += 1
        #if any(s in title_string for s in ("Dota 2","DOTA 2","Dota2","DOTA2")):
        #if "Dota 2" or "DOTA 2" or "Dota2" or "DOTA2" in str:
        #if "Dota 2" in title_string:
            #relevance_count += 1
    print rel_tot
    relevance_percent = (float(rel_tot)/total_count) * 100
    print relevance_percent,
    if relevance_percent > 70:
        return True
    else:
        return False

def relevant_topics(titles,relevance_count):
    title_string = titles.get_attribute('title')
    if any(s in title_string for s in ("Dota 2","DOTA 2","Dota2","DOTA2")):
        return 1
    else:
        return 0
        
def check_views():
    video_views = titles.get_attribute('aria-label')
    video_views.split()

##Build indexed Xpaths and retrieve URL value from each in href attribute
i=1
while i < 10:
    channel_xpath ="""//*[@id="contents"]/ytd-channel-renderer["""+str(i)+"]/a"
    channel = driver.find_element_by_xpath(channel_xpath)
    print channel.get_attribute('href')
    
    channel_videos = channel.get_attribute('href') + "/videos"
    driver.get(channel_videos)
        
    if check_to_process():
        print ("Check for number of views")
    else:
        print("Do not check for relevant views")
    
    
    driver.back()
    time.sleep(1)
    i += 1
    



##Extract titles 
#title = driver.find_elements_by_xpath('//*[@id="channel-title"]/span')
#for t in title:
#    print t.text

