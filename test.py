# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pickle
import time
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
      
def check_exists_by_xpath(xpath, driver):
    try:
        driver.find_element_by_xpath(xpath)
    except:
        return False
    return True

class driver_class():
    
    def __init__(self, url_in):
        options = webdriver.FirefoxOptions()
        #options.add_argument("-headless")
        self.driver = webdriver.Firefox(firefox_options=options)
        self.driver.get(url_in,)
        self.driver.set_page_load_timeout(120)
    
    def __del__(self):
        self.driver.close()
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.close()

def get_product_data(country_in,category_in):
    
    prod_list = []
    
    #options = webdriver.FirefoxOptions()
    #options.add_argument("-headless")
    #driver = webdriver.Firefox(firefox_options=options)
    
    country_switcher = {
        "DE": "https://www.alza.de",
        "UK": "https://www.alza.co.uk",
        "PL": "https://www.alza.pl",
        "CZ": "https://www.alza.cz"
    }
    
    main_url = country_switcher.get(country_in)
    
    drvclass = driver_class(main_url)
    
    #driver.get(main_url,)
    #driver.set_page_load_timeout(120)
    
    category_switcher = {
        "Smart": "//*[@id=\"litp18855733\"]/div[1]/a",
        "Phones": "//*[@id=\"litp18843445\"]/div[1]/a",
        "Laptops": "//*[@id=\"litp18842920\"]/div[1]/a",
        "Household": "//*[@id=\"litp18850352\"]/div[1]/a"
    }
    xpath_str = category_switcher.get(category_in)
    
    # Open mobile phones
    elem = drvclass.driver.find_element_by_xpath(xpath_str)
    elem.click()
    
    next_button_exists = 1
    page_counter = 1
    
    for page_counter in range(0,10):
        
        xpath_str="//*[@id=\"notificationBoxCookiesCloseBtn\"]/span"
        if check_exists_by_xpath(xpath_str, drvclass.driver):
            elem = drvclass.driver.find_element_by_xpath(xpath_str)
            elem.click()
        
        for prod_id in range(0,24):
            
            curr_prod_data={'country':country_in,'category':category_in,'url':'','pic_path':'','title':'','price':'','desc':''}
            
            try:
            
                #close cookies dialog if it appears
                xpath_str="/html/body/div[3]/div/div/div[2]/div/span/span"
                if check_exists_by_xpath(xpath_str, drvclass.driver):
                    elem = drvclass.driver.find_element_by_xpath(xpath_str)
                    elem.click()
                    
                xpath_str="//*[@id=\"boxes\"]/div["+str(prod_id+1)+"]/div[1]/div[2]/a"
                if check_exists_by_xpath(xpath_str, drvclass.driver):
                    elem = drvclass.driver.find_element_by_xpath(xpath_str)
                    elem.click()
                else:
                    xpath_str="//*[@id=\"boxes\"]/div["+str(prod_id+1)+"]/div[1]/div/a"
                    if check_exists_by_xpath(xpath_str, drvclass.driver):
                        elem = drvclass.driver.find_element_by_xpath(xpath_str)
                        elem.click()
                    else:
                        print("Error")
                
                curr_prod_data['url'] = drvclass.driver.current_url
                
                for pic_id in range(0,4):
                    
                    curr_prod_data['pic_path'] = []
                    xpath_str="//*[@id=\"galleryPreview\"]/div/div/a["+str(pic_id+2)+"]/img"
                    
                    if check_exists_by_xpath(xpath_str, drvclass.driver):
                        try:
                            elem = drvclass.driver.find_element_by_xpath(xpath_str)
                            hover = ActionChains(drvclass.driver).move_to_element(elem)
                            hover.perform()
                            time.sleep(2)
                            
                            elem = drvclass.driver.find_element_by_xpath("//*[@id=\"imgMain\"]")
                            src = elem.get_attribute('src')
                            
                            curr_pic_path = "pics/pic_" + country_in + "_cat_" + category_in + "_page_"+str(page_counter)+"_place_"+str(prod_id)+"_pic_"+str(pic_id)+".png"
                            curr_prod_data['pic_path'].append(curr_pic_path)
                            urllib.request.urlretrieve(src, curr_pic_path)
                        
                        except:
                            print("Loading pic id " + str(pic_id) + " FAILED.")
                
                curr_prod_data['title'] = ''
                elem = drvclass.driver.find_element_by_xpath("//*[@id=\"h1c\"]/h1")
                
                print("Product title:")
                print(elem.text)
                curr_prod_data['title'] = elem.text
                
                #xpath_str = "/html/body/div[3]/div/div/div[1]/div[3]/div[2]/div[2]/div[3]/div[6]/div[4]/div[1]/table/tbody/tr[1]/td[2]/span"
                xpath_str = "//*[@id=\"prices\"]/tbody/tr[1]/td[2]/span[2]"
                curr_prod_data['price'] = ''
                if check_exists_by_xpath(xpath_str, drvclass.driver):
                
                    elem = drvclass.driver.find_element_by_xpath(xpath_str)
                    print("Product price:")
                    print(elem.text)
                    curr_prod_data['price'] = elem.text
                else:
                    #xpath_str = "/html/body/div[3]/div/div/div[1]/div[3]/div[2]/div[2]/div[3]/div[6]/div[5]/div[1]/table/tbody/tr[1]/td[2]/span[2]"
                    xpath_str = "//*[@id=\"prices\"]/tbody/tr[1]/td[2]/span"
                    if check_exists_by_xpath(xpath_str, drvclass.driver):
                        elem = drvclass.driver.find_element_by_xpath(xpath_str)
                        print("Product price:")
                        print(elem.text)
                        curr_prod_data['price'] = elem.text
                    else:
                        print("Error")
                
                curr_prod_data['desc'] = ''
                elem = drvclass.driver.find_element_by_xpath("//*[@id=\"detailText\"]/div[2]/span")
                print("Product desc:")
                print(elem.text)
                curr_prod_data['desc'] = elem.text
                
                print(curr_prod_data)
        
            except:
                print("Error while analysing prod id " + str(prod_id))
                
            prod_list.append(curr_prod_data)
            
            drvclass.driver.execute_script("window.history.go(-1)")
            time.sleep(2)
        
        xpath_str="//*[@id=\"notificationBoxCookiesCloseBtn\"]/span"
        
        if check_exists_by_xpath(xpath_str, drvclass.driver):
            elem = drvclass.driver.find_element_by_xpath(xpath_str)
            elem.click()
        
        xpath_str = "//*[@id=\"pgby" + str(page_counter+1) + "\"]"
        
        if check_exists_by_xpath(xpath_str, drvclass.driver):
            next_button_exists=1
            elem = drvclass.driver.find_element_by_xpath(xpath_str)
            elem.click()
        else:
            next_button_exists=0
    
    return prod_list
        
    #/html/body/div[3]/div/div/div[1]/div[3]/div[2]/div[2]/div[3]/div[8]/div[2]/div[4]/div
    #/html/body/div[25]/div/div/div[2]/div/img
    
    #/html/body/div[3]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[4]/div[9]/div[2]/div/div[1]/div[1]/div[2]/a
    #/html/body/div[3]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[4]/div[9]/div[2]/div/div[2]/div[1]/div[2]/a
    #/html/body/div[3]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[4]/div[9]/div[2]/div/div[3]/div[1]/div[2]/a
    #/html/body/div[3]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[4]/div[9]/div[2]/div/div[4]/div[1]/div/a
    #/html/body/div[3]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[4]/div[9]/div[2]/div/div[5]/div[1]/div/a
    
    #//*[@id="pgby2"]
    #//*[@id="pgby3"]
    #//*[@id="pgby4"]
        
def get_pics(my_prod_list):
    
    drvclass = driver_class("https://www.google.com/shopping")
    
    for prod_id in range(0,len(my_prod_list)):
        if (len(my_prod_list[prod_id]['title'])>0):
            try:
                xpath_str="//*[@id=\"lst-ib\"]"
                elem = drvclass.driver.find_element_by_xpath(xpath_str)
                elem.clear()
                elem.send_keys(my_prod_list[prod_id]['title'])
                elem.send_keys(Keys.RETURN)
                time.sleep(3)
                xpath_str="//*[@class=\"TL92Hc\"]"
                
                elem = drvclass.driver.find_element_by_xpath(xpath_str)
                
                elem.click()
                
                xpath_str="//*[@id=\"rso\"]/div[1]/div/div[2]/div/div/div/div[1]/div[1]/a/div/img"
                elem = drvclass.driver.find_element_by_xpath(xpath_str)
                src = elem.get_attribute('src')
                
                pic_path = "goog_pics/goog_pic_"+str(prod_id)+".png"
                my_prod_list[prod_id]['pic_path'].append(pic_path)
                urllib.request.urlretrieve(src, pic_path)
                
            except:
                print("Error")
                
            drvclass.driver.execute_script("window.history.go(-1)")
            time.sleep(3)
    return 0


my_prod_list = get_product_data("UK","Smart")+get_product_data("UK","Phones")+get_product_data("UK","Laptops")+get_product_data("UK","Household")

my_prod_list = get_product_data("UK","Smart")

with open('data/data.dat', 'wb')as f:  # Python 3: open(..., 'wb')
    pickle.dump(my_prod_list, f)
    
with open('data/data.dat', 'rb') as f:  # Python 3: open(..., 'rb')
    my_prod_list = pickle.load(f)

get_pics(my_prod_list)
