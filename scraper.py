##Imports
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

channel_list = []

# Build Channel list
def build_channel_list():
    channel_numbr = 1
    while channel_numbr <= 50:
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
        if total_count >= 5:
            break

        # Check for relevance with related terms
        rel_tot += relevant_topics(elements)

        # Check for views
        video_views.append(check_views(elements))

        total_count += 1
#     print(rel_tot)
#     print
#     total_count
    if total_count > 0:
        relevance_percent = (float(rel_tot) / total_count) * 100
    if relevance_percent >= 60:
        print("Relevance_percent : ", relevance_percent, "Relevance Percent Satisfied")
        for v in video_views:
            print v
            if int(v) > 500000 or int(v) < 10000:
                print("In False")
                return False
        print("Views Range Satisfied")
        return True
    else:
        print("Relevance_percent : ", relevance_percent, "Relevance Percent Not Satisfied")
        return False


def relevant_topics(title):
    title_string = title.get_attribute('title')
    if any(s in title_string for s in ("Dota 2", "DOTA 2", "Dota2", "DOTA2")):
    #if any(s in title_string for s in ("Minecraft", "MINECRAFT", "MineCraft", "mineCraft")):
        return 1
    else:
        return 0


def check_views(views):
    video_views_raw = views.get_attribute('aria-label')
    if video_views_raw.split(' ')[-2] == 'No':
        return 0
    else:
        return int(video_views_raw.split(' ')[-2].replace(",", ""))


# Main Starts here

#Base URL contains channel filter

url_base = "https://www.youtube.com/results?sp=EgIQAkIECAESAA%253D%253D&search_query="
#url_search_query = "minecraft+skins+servers+gameplay+mods"
url_search_query = "dota+2+heroes+gameplay"

##Invoke Driver and get URL

driver = webdriver.Chrome(r"C:\Users\adhei\Anaconda2\selenium\webdriver\chrome\chromedriver.exe")
driver.get(url_base + url_search_query)

##Scroll down page to load and get more results and retrieve all results
elem = driver.find_element_by_tag_name("body")
no_of_pagedowns = 50

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns -= 1

chnl_lst = build_channel_list()
print("Completed Build Channel List")
new_list = []
new_list = validate_channels(chnl_lst)
print(new_list)

# ########################
#driver = webdriver.Chrome(r"C:\Users\adhei\Anaconda2\selenium\webdriver\chrome\chromedriver.exe")

#new_list_test = ["https://www.youtube.com/user/noobfromua"]
#new_list_test = ["https://www.youtube.com/channel/UCV7lBBz6G20d87WoKFPjsPw","https://www.youtube.com/user/noobfromua"]

iter1 = 0

f = open('youtube_channel_info.csv','ab')
writer = csv.writer(f)


csv_header = ["Topic","Channel_Name","Join_Date", "No_of_Days","No._of_Subscribers","No._of_views_total",
              "Video_Link_1","Views_1","Likes_1","Dislikes_1","Commments_1","Engagement_1","Popularity_1","Sentiment_1","Growth_1",
              "Video_Link_2","Views_2","Likes_2","Dislikes_2","Commments_2","Engagement_2","Popularity_2","Sentiment_2","Growth_2",
              "Video_Link_3","Views_3","Likes_3","Dislikes_3","Commments_3","Engagement_3","Popularity_3","Sentiment_3","Growth_3",
             "Average_Engagement","Average_Popularity","Averge_Sentiment","Average_Growth"]

if iter1 == 0:
    writer.writerow(csv_header)
    iter1 = 1

output_list = []
for chan in new_list:
    
    #Global variable declarations
    #topic = 'Minecraft'
    topic = 'Dota 2'
    tot_videos = 0
    i = 0
    total_c = 0
    engagement = 0
    popularity = 0
    sentiment = 0
    growth = 0
    video_list = []
    del output_list[:]
    
    #Retrieve Channel Join Date and Total View, Calculate Number of days 
    driver.get(chan + "/about")
    channel_start_date = driver.find_element_by_xpath("""//*[@id="right-column"]/yt-formatted-string[2]""")
    join_date = channel_start_date.text.replace(',','').split(' ')
    join_date.remove(join_date[0])
    join_date_new = '-'.join(join_date)
    chn_join_date = datetime.datetime.strptime(join_date_new,"%b-%d-%Y")
    now = datetime.datetime.now()
    chn_days =  now - chn_join_date
    chn_days_final = str(chn_days).split(' ')[0]
    
    channel_views_element = driver.find_element_by_xpath("""//*[@id="right-column"]/yt-formatted-string[3]""")
    chn_views = int(channel_views_element.text.split(' ')[0].replace(',',''))
    
    #Retrieve Channel Name and subscribers
    print (chan + "/videos")
    driver.get(chan + "/videos")
    channel_name = driver.find_element_by_xpath("""//*[@id="channel-title"]""")
    channel_subscribers = driver.find_element_by_xpath("""//*[@id="subscriber-count"]""")
    
    chn_name = channel_name.text
    chn_sub = int(channel_subscribers.text.split(' ')[0].replace(',',''))
    
    #Need to write chn_text, chn_sub
    print ("Channel Name:" + str(chn_name))
    print ("Subscriber Count:" + str(chn_sub))
    video_title_elements = driver.find_elements_by_xpath("""//*[@id="video-title"]""")
    output_list.append(topic)
    output_list.append(chn_name)
    output_list.append(chn_join_date)
    output_list.append(chn_days_final)
    output_list.append(chn_sub)
    output_list.append(chn_views)
    
    
    #Create a list of 3 videos for each channel
    for elements in video_title_elements:
        if total_c >=3:
            break
        get_video = elements.get_attribute('href')
        video_list.append(get_video)
        total_c += 1  
    
    #Works for each video in channel
    
    for vids in video_list:
        output_list.append(vids)
        print vids
        #Load video page
        driver.get(vids)
        
        #Code to scroll to load comments
        elem = driver.find_element_by_tag_name("body")
        no_of_pagedowns = 2
        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(5)
            no_of_pagedowns -= 1
            
        time.sleep(5)
        
        #Capture Views
        video_views_element = driver.find_element_by_xpath("""//*[@id="count"]/yt-view-count-renderer/span[1]""")
        video_views = int(video_views_element.text.split(' ')[0].replace(',',''))
        print ("Views: " + str(video_views))
        output_list.append(video_views)
        
        #Caputure Likes       
        #video_likes_element = driver.find_element_by_xpath("""//*[@id="text"])[position()=3]""")
        video_likes_element = driver.find_element_by_xpath("""//*[@id="text" and contains(@aria-label,'like')]""")
        video_likes = int(video_likes_element.get_attribute('aria-label').split(' ')[0].replace(',',''))
        #video_likes = int(video_likes_element.text)
        output_list.append(video_likes)
        print ("Video Likes: " + str(video_likes_element.text))
        
        #Caputure Dislikes
        #video_dislikes_element = driver.find_element_by_xpath("""(//*[@id="text"])[position()=4]""")
        video_dislikes_element = driver.find_element_by_xpath("""//*[@id="text" and contains(@aria-label,'dislike')]""")
        video_dislikes = int(video_dislikes_element.get_attribute('aria-label').split(' ')[0].replace(',',''))
        #video_dislikes = int(video_dislikes_element.text)
        output_list.append(video_dislikes)
        print ("Video Dislikes: " + str(video_dislikes_element.text))
        
        #Capture Comments
        
        video_comment_elements = driver.find_element_by_xpath("""/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch/div[2]/div[2]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string""")
        video_comments = int(video_comment_elements.text.split(' ')[0].replace(',',''))
        output_list.append(video_comments)
        print ("Comments :" + str(video_comments))
                
        # Calculate Additional metrics
        
        #Comment to View Ratio - Engagement
        if video_views > 0: 
            engagement = round((float(video_comments)/video_views) * 100,2)
        else:
            engagement = 0
        print ("Engagement Ratio :" + str(engagement))
        output_list.append(engagement)
        
        #Likes to View Ratio - Popularity
        if video_views > 0:
            popularity = round((float(video_likes)/video_views)* 100,2)
        else:
            popularity = 0
        print ("Popularity :" + str(popularity))
        output_list.append(popularity)
        
        #Dislikes to Likes - Ratio - Sentiment
        if video_likes > 0 or video_dislikes > 0:
            sentiment = round((float(video_likes)/ (video_likes+video_dislikes))*100,2)
        else:
            sentiment = 0
        print("Sentiment :" + str(sentiment))
        output_list.append(sentiment)
        
        #Views to Subscriber Ratio - Growth
        if chn_sub > 0:
            growth = round((float(video_views)/chn_sub) * 100,2)
        else:
            growth = 0
        print("Growth :" + str(growth))
        output_list.append(growth)
        
        time.sleep(3)
    average_engagement = round(float(output_list[csv_header.index("Engagement_1")]+output_list[csv_header.index("Engagement_2")]+output_list[csv_header.index("Engagement_3")] )/ len(video_list),2)
    output_list.append(average_engagement)
    average_popularity = round(float(output_list[csv_header.index("Popularity_1")]+output_list[csv_header.index("Popularity_2")]+output_list[csv_header.index("Popularity_3")] )/ len(video_list),2)
    output_list.append(average_popularity)
    average_sentiment = round(float(output_list[csv_header.index("Sentiment_1")]+output_list[csv_header.index("Sentiment_2")]+output_list[csv_header.index("Sentiment_3")] )/ len(video_list),2)
    output_list.append(average_sentiment)
    average_growth = round(float(output_list[csv_header.index("Growth_1")]+output_list[csv_header.index("Growth_2")]+output_list[csv_header.index("Growth_3")] )/ len(video_list),2)
    output_list.append(average_growth)
    writer.writerow(output_list)

f.close()
driver.quit()
