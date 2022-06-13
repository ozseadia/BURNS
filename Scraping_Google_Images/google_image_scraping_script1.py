import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as OptionChrome
from selenium.webdriver.edge.options import Options as OptionEdge
from selenium.webdriver.common.action_chains import ActionChains
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
Path=os.path.join((os.path.split(os.path.dirname(os.path.abspath(__file__))))[0],'Avoid_duplicates')
print(Path)
print (type(Path))
sys.path.append(Path)
#sys.path.append(r"G:\Oz\fiveer\Dani_Velinchick\Burns\Avoid_duplicates")
import Avoid_duplicates as AD
import MetaData as MD
from openpyxl.workbook import Workbook

Path=os.path.dirname(__file__)
head_tail=os.path.split (Path) 
driversPath=head_tail[0]
#print(driversPath)
#print(1)
sys.path.append(driversPath)

import Proxy as Py 


# All in same directory
#DRIVER_PATH = '\Scraping_Google_Images\chromedriver.exe'
class google_image():
    def __init__ (self):
        Path=os.path.dirname(__file__)
        head_tail=os.path.split (Path) 
        Proxy_file=os.path.join(head_tail[0],'proxy.txt')
        with open(Proxy_file) as f:
            lines = f.readlines()
        self.username=lines[1][:-1]
        self.password=lines[3][:-1]
        self.PROXY_HOST=lines[5][:-1]
        self.PROXY_PORT=lines[7]
        self.oz='oz'
        self._headers={'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }
        driversPath=head_tail[0]
        #print(driversPath)
        sys.path.append(driversPath)
        self.Root=head_tail[0]
        self.ChromPath=os.path.join(head_tail[0],'chromedriver.exe')
        self.EdgePath=os.path.join(head_tail[0],'msedgedriver.exe') 
        
        self.Edge_userdata_path=(r'C:\Users\OzSea\AppData\Local\Microsoft\Edge\User Data')
        #self.Edge_userdata_path=''
        self.Edge_options = OptionEdge() 
        self.Edge_options.add_experimental_option("detach", True)
        self.Edge_options.add_argument("user-data-dir=%s"%self.Edge_userdata_path); 
        print(self.Edge_userdata_path)
        self.Edge_options.add_argument("profile-directory=Default");
        #/html/body/div/table/tbody/tr[8]/td[2]
        
        
        self.Chrome_userdata_path=(r'C:\Users\OzSea\AppData\Local\Google\Chrome\User Data')
        #self.Chrome_userdata_path=''
        self.Chrome_options = OptionChrome() 
        self.Chrome_options.add_experimental_option("detach", True)
        self.Chrome_options.add_argument("user-data-dir=%s"%self.Chrome_userdata_path); 
        print(self.Chrome_userdata_path)
        self.Edge_options.add_argument("profile-directory=Default");
        self.Chrome_options.add_experimental_option('prefs', {
            "download.default_directory": os.path.join(self.Root,'PDFs'), #Change default directory for downloads
            "download.prompt_for_download": False, #To auto download the file
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
            })
        self.Pdfs_Download_path=os.path.join(self.Root,'PDFs')
        self.Chrome_options.add_extension(Py.SetProxy(self.PROXY_HOST,self.PROXY_PORT,
                                                      self.username,self.password))
        self.proxies = {
            'http': 'http://%s:%s@%s:%s/'%(self.username,self.password,self.PROXY_HOST,self.PROXY_PORT)
            }    
    

    def fetch_image_urls(self,query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=int(30*random.random())):
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
        Flag_stop=0
        while (image_count < max_links_to_fetch) & (error_clicks <50): # error clicks to stop when there are no more results to show by Google Images. You can tune the number
            time.sleep((5*random.random()))
            scroll_to_end(wd)
    
            print('Starting search for Images')
    
            # get all image thumbnail results
            thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
            number_results = len(thumbnail_results)
            
            print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
            Flag_stop+=1
            if Flag_stop >5:
                break
            for img in thumbnail_results[results_start:max_links_to_fetch]:
                # try to click every thumbnail such that we can get the real image behind it
                print("Total Errors till now:", error_clicks)
                results_start = results_start + 1
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
                    pass
                else:
                    break
                    	
                
    
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
                	        
            #results_start = len(thumbnail_results)
            #if results_start == number_results:
            #    break
    
        return image_urls
    
    def persist_image(self,folder_path:str,file_name:str,url:str,ad):
        FlagSave=0
        Info=[]
        try:
            #image_content = requests.get(url,proxies=self.proxies,auth=(self.username,self.password)).content
            image_content = requests.get(url,proxies=self.proxies).content
            time.sleep(0.5)
    
        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")
    
        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_name=file_name.replace('"','')
            file_name=file_name.replace('+','_')
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
            FlagSave=ad.main(image)
            print('Flage save %d',FlagSave)
            if FlagSave :
                f=open(file_path,'w')
                time.sleep(0.5)
                    #print(f)
                image.save(f, "JPEG", quality=85)
                image.close()
                f.close()
                print('done')
                time.sleep(0.5)
                print(f"SUCCESS - saved {url} - as {file_path}")
                Info=[(os.path.split(file_path))[1],
                      str((image.size)),
                      "",
                      os.path.basename(folder_path),
                      "",
                      url]
            else:
                print('image was not saved')
            
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")
            FlagSave=0
            try:
                f.close()
                time.sleep(1)
            except:
                pass
        try:
            f.close()
            time.sleep(1)
        except:
            pass
        
        
        return FlagSave , Info
    
    
        
        
    #if __name__ == '__main__':
    def main(self,queries,number_of_images):
        #images_path =os.path.join(MainPath,'dataset')
        images_path =os.path.join(self.Root,'dataset')
        ad=AD.FeatureExtractor()
        md=MD.MetaData(images_path)
        #wd = webdriver.Chrome(executable_path=chromePath)
        wd=webdriver.Chrome(self.ChromPath,options=self.Chrome_options)
        #wd =chromePath
        #queries = ['child burn','burn','child abuse']  #change your set of queries here
        
        
        
        for query in queries:
            wd.get('https://google.com')
            search_box = wd.find_element_by_css_selector('input.gLFyf')
            search_box.send_keys(query)
            links = self.fetch_image_urls(query,number_of_images,wd) # 200 denotes no. of images you want to download
            print(links)
            n=0
            for i in links:
                n=n+1
                print(images_path)
                FlagSave,Info=self.persist_image(images_path,query,i,ad)
                time.sleep((5*random.random()))
                if FlagSave:
                    Info[2]=n
                    Info[4]=query
                    #Info[5] #URL
                    md.MetaDataAppend(Info)    
                
        st.write('FINISHED')
        wd.quit()
        
        st.stop()
        
        try:
            st.stop()
            wd.quit()
            
        except:
            return
    