from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import json, random,time

def get_plugin_properties(plugin_name):
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

def get_plugin_reviews(plugin_name,page_num):
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

def get_plugin_reviews_pages(plugin_name):
    browser.get("https://wodpress.org/support/plugin/"+plugin_name+"/reviews/page/1")
    return(int(browser.find_elements_by_class_name('page-numbers')[-2].text))


def get_plugins_per_cat(cat,page_num):

    browser.get("https://wordpress.org/plugins/browse/"+cat+"/page/" + str(page_num))
    plugins = browser.find_elements_by_tag_name('article')
    plugins_names=[]
    for plugin in plugins:
        entry = plugin.find_element_by_class_name('entry-header')
        a_entry = entry.find_element_by_tag_name('a')
        plugins_names.append(a_entry.get_attribute('href').replace("https://wordpress.org/plugins/","").replace("/",""))
    return plugins_names

def get_plugins_per_cat_pages(cat):
    browser.get("https://wordpress.org/plugins/browse/"+cat+"/page/1" )
    return(int(browser.find_elements_by_class_name('page-numbers')[-2].text))

#--------------------------------------------------------------
#--------------------------------------------------------------
def get_all_popular_plugins():
    maxpags=get_plugins_per_cat_pages('popular')
    allplugins=[]
    for i in range(1):
        time.sleep(random.randint(1,20))
        allplugins.extend(get_plugins_per_cat('popular',i))
    
    result=dict()
    for plugin in allplugins:
        time.sleep(random.randint(1,20))
        plugin_data=get_plugin_properties(plugin)
        max_rev_pages=get_plugin_reviews_pages(plugin)
        review_data=[]
        for j in range(1):
            time.sleep(random.randint(1,20))
            review_data.extend(get_plugin_reviews(plugin,j))
        plugin_data['reviews']=review_data
        result[plugin]=plugin_data
    return plugin
#--------------------------------------------------------------
# Starting the actual program
#--------------------------------------------------------------
#--------------------------------------------------------------
#--------------------------------------------------------------
browser_categories=["popular","blocks","featured","beta"]

chrome_options = Options()  
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
browser = webdriver.Chrome(options=chrome_options)

#print(json.dumps(processPlugin("leadin")))
#processPluginsListPage(1)
#print(getPluginsMaxPages())
#processReviewPage('leadin',1)
#print(get_plugin_reviews_pages('leadin'))
with open('pluggins.json', 'w') as f:
    json.dumps(get_all_popular_plugins(),f,sort_keys=True, indent=4)