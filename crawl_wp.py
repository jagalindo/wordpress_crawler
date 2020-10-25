from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import json   

def processPlugin(plugin_name):
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
            print("Languages: ")
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

def processPluginsListPage(page_num):

    browser.get("https://wordpress.org/plugins/browse/popular/page/" + str(page_num))
    plugins = browser.find_elements_by_tag_name('article')
    for plugin in plugins:
        entry = plugin.find_element_by_class_name('entry-header')
        a_entry = entry.find_element_by_tag_name('a')
        print(a_entry.get_attribute('href'))

def getPluginsMaxPages():
    browser.get("https://wordpress.org/plugins/browse/popular/page/1" )
    return(int(browser.find_elements_by_class_name('page-numbers')[-2].text))

#--------------------------------------------------------------
#--------------------------------------------------------------
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

print(json.dumps(processPlugin("leadin")))
#processPluginsListPage(1)
#print(getPluginsMaxPages())