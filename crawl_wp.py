from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import json, random,time,datetime
import logging
def get_plugin_properties(plugin_name,browser):
    properties=dict()

    browser.get("https://wordpress.org/plugins/" + plugin_name)
    title = browser.find_element_by_class_name("plugin-title").text
    
    properties["Title"]=title

    data = browser.find_element_by_class_name("plugin-meta")
    elementUL = data.find_element_by_xpath('.//ul')
    informacion = elementUL.find_elements_by_xpath('.//li')
    for w in informacion :
        if 'Tags' in w.text:
            tags = w.find_elements_by_tag_name('a')
            tag_list=[]
            for t in tags :
                tag_list.append(t.text)
            properties["Tags"]=tag_list
        elif 'Advanced View' in w.text:
            pass
        #have to implement Languages
        elif 'Languages' in w.text:
            #print("Languages: ")
            languages_div = w.find_element_by_class_name('popover-inner')
            languages = languages_div.find_elements_by_tag_name('a')
            languages_list=[]
            for l in languages :
                if not 'Translate' in l.get_attribute('innerHTML') :
                    languages_list.append(l.get_attribute('innerHTML'))
            properties["Languages"]=languages_list
        else:    
            pluggin_property=w.text.split(':')
            properties[pluggin_property[0]]=pluggin_property[1].strip()
    
    # Counting stars
    data = browser.find_element_by_class_name("plugin-ratings")

    try:
        full_stars = data.find_elements_by_class_name("dashicons-star-filled")
    except NoSuchElementException:
        full_stars=[]

    try:
        half_stars = data.find_elements_by_class_name("dashicons-star-half")
    except NoSuchElementException:
        half_stars=[]


    total_stars=len(full_stars)+0.5*len(half_stars)
    properties["Score"]=str(total_stars)
    return(properties)

def get_plugin_reviews(plugin_name,page_num,browser):
    browser.get("https://wordpress.org/support/plugin/"+plugin_name+"/reviews/page/" + str(page_num))
    results=[]
    container=browser.find_element_by_class_name("bbp-body")
    uls = container.find_elements_by_xpath('.//ul')
    for ul in uls :
        comment=dict()
        link=ul.find_element_by_class_name("bbp-author-name").text
        comment["autor"]=link
        review=ul.find_element_by_class_name("bbp-topic-permalink").text
        comment["review"]=review
        try :
            stars=ul.find_element_by_class_name("wporg-ratings").get_attribute('title')
            comment["stars"]=stars
        except NoSuchElementException:
            comment["stars"]=""

        date=ul.find_element_by_class_name('bbp-topic-freshness').find_element_by_tag_name('a').get_attribute('title')
        comment["date"]=date
        results.append(comment)
    return results

def get_plugin_reviews_pages(plugin_name,browser):
    browser.get("https://wordpress.org/support/plugin/"+plugin_name+"/reviews/")
    try:
        pages=int(browser.find_elements_by_class_name('page-numbers')[-2].text)
    except NoSuchElementException:
        pages=1
    return(pages)


def get_plugins_per_cat(cat,page_num,browser):

    browser.get("https://wordpress.org/plugins/browse/"+cat+"/page/" + str(page_num)+"/")
    plugins = browser.find_elements_by_tag_name('article')
    plugins_names=[]
    for plugin in plugins:
        entry = plugin.find_element_by_class_name('entry-header')
        a_entry = entry.find_element_by_tag_name('a')
        plugins_names.append(a_entry.get_attribute('href').replace("https://wordpress.org/plugins/","").replace("/",""))
    return plugins_names

def get_plugins_per_cat_pages(cat,browser):
    browser.get("https://wordpress.org/plugins/browse/"+cat+"/page/1" )
    return(int(browser.find_elements_by_class_name('page-numbers')[-2].text))

#--------------------------------------------------------------
#--------------------------------------------------------------
def get_all_popular_plugins():
    browser=getRandomBrowser()
    
    maxpags=get_plugins_per_cat_pages('popular',browser)
    allplugins=[]
    for i in range(1,maxpags):
        allplugins.extend(get_plugins_per_cat('popular',i,browser))
    result=dict()
    for plugin in allplugins:
        print(plugin)
        plugin_data=get_plugin_properties(plugin,browser)
        max_rev_pages=get_plugin_reviews_pages(plugin,browser)
        review_data=[]
        for j in range(1,max_rev_pages):
            #time.sleep(10)
            review_data.extend(get_plugin_reviews(plugin,j,browser))

        plugin_data['reviews']=review_data
        result[plugin]=plugin_data
        
    return result
#--------------------------------------------------------------
# Starting the actual program
#--------------------------------------------------------------
#--------------------------------------------------------------
#--------------------------------------------------------------
def getRandomBrowser():

    chrome_options = Options()  
    #chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless")
    # chrome_options.headless = True # also works
    #chrome_options.add_argument("--log-path=/dev/null")
    PROXY = proxies[random.randint(0,len(proxies))].get_address()
    webdriver.DesiredCapabilities.CHROME['proxy']={
        "httpProxy":PROXY,
        "ftpProxy":PROXY,
        "sslProxy":PROXY,
        "proxyType":"MANUAL",
        'trustAllServers':'true',
        
    }
    browser = webdriver.Chrome(options=chrome_options)
    return browser

logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)

req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
proxies = req_proxy.get_proxy_list() #this will create proxy list
sp = [] #int is list of Indian proxy
for proxy in proxies:
    if proxy.country == 'Spain':
        sp.append(proxy)
proxies=sp


browser_categories=["popular","blocks","featured","beta"]
data=get_all_popular_plugins()
json_data=json.dumps(data)

current_date_and_time = datetime.datetime.now()
current_date_and_time_string = str(current_date_and_time)
extension = ".json"

file_name =  current_date_and_time_string + extension

with open(file_name, 'w') as f:
    json.dump(json_data,f)

f.close()