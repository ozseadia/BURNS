import selenium
from selenium import webdriver
import time
import requests
import os
from PIL import Image
import io
import hashlib
import streamlit as st
import random
#import path
import sys
Path=os.path.join((os.path.split(os.path.dirname(os.path.abspath(__file__))))[0])
sys.path.append(Path)
sys.path.append(r"G:\Oz\fiveer\Dani_Velinchick\Burns\Avoid_duplicates")
import Avoid_duplicates as AD
 


# All in same directory
#DRIVER_PATH = '\Scraping_Google_Images\chromedriver.exe'


def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=int(30*random.random())):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions+5)        
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    error_clicks = 0
    while (image_count < max_links_to_fetch) & (error_clicks <50): # error clicks to stop when there are no more results to show by Google Images. You can tune the number
        scroll_to_end(wd)

        print('Starting search for Images')

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        for img in thumbnail_results[results_start:max_links_to_fetch]:
            # try to click every thumbnail such that we can get the real image behind it
            print("Total Errors till now:", error_clicks)
            try:
            #if 1:
                print(1)
                print('Trying to Click the Image')
                img.click()
               
                time.sleep(sleep_between_interactions)
                print('Image Click Successful!')
            except Exception:
                error_clicks = error_clicks + 1
                print('ERROR: Unable to Click the Image')
                if(results_start +1 < number_results):
                    continue
                else:
                    break
                	
            results_start = results_start + 1

            # extract image urls    
            print('Extracting of Image URLs')
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            print('Current Total Image Count:', image_count)
            print(len(image_urls))
            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
            else:
                load_more_button = wd.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click();")
                else:
                    break
            	        
        results_start = len(thumbnail_results)
        if results_start == number_results:
            break

    return image_urls

def persist_image(folder_path:str,file_name:str,url:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        folder_path = os.path.join(folder_path,file_name)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:15] + '.jpg')
            print(1)
        else:
            print(2)
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:15] + '.jpg')
        #with open(file_path, 'wb') as f:
            #time.sleep(3)  
        FlagSave=AD.FeatureExtractor().main(image)
        print('Flage save %d',FlagSave)
        if FlagSave :
            f=open(file_path,'w')
            time.sleep(15)
                #print(f)
            image.save(f, "JPEG", quality=85)
            image.close()
            f.close()
            print('done')
            time.sleep(1)
            print(f"SUCCESS - saved {url} - as {file_path}")
        else:
            print('image was not saved')
        
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")
        try:
            f.close()
            time.sleep(1)
        except:
            return
    try:
        f.close()
        time.sleep(1)
    except:
        return
#if __name__ == '__main__':
def main(queries,number_of_images,chromePath,MainPath):    
    wd = webdriver.Chrome(executable_path=chromePath)
    #wd =chromePath
    #queries = ['child burn','burn','child abuse']  #change your set of queries here
    for query in queries:
        wd.get('https://google.com')
        search_box = wd.find_element_by_css_selector('input.gLFyf')
        search_box.send_keys(query)
        links = fetch_image_urls(query,number_of_images,wd) # 200 denotes no. of images you want to download
        print(links)
        images_path =os.path.join(MainPath,'dataset')
        for i in links:
            print(images_path)
            persist_image(images_path,query,i)
    st.write('FINISHED')
    wd.quit()
    
    st.stop()
    
    try:
        st.stop()
        wd.quit()
        
    except:
        return
    