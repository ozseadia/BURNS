# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 08:01:37 2022

@author: OzSea
"""

from bs4 import BeautifulSoup
import httplib2
import requests, lxml, os, json
import re
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as OptionChrome
from selenium.webdriver.edge.options import Options as OptionEdge
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import wget
import sys
import time
import urllib.request
import win32com.client
import pyautogui
import math
import random
import shutil
#import Proxy as Py
Path=os.path.dirname(__file__)
head_tail=os.path.split (Path) 
driversPath=head_tail[0]
#print(driversPath)
#print(1)
sys.path.append(driversPath)
#sys.path.append(Path)
import recaptcha 
import Proxy as Py

sys.path.append(os.path.join(driversPath,'chromedriver.exe'))
#Proxy=sys.path.append(os.path.join(driversPath,'proxy.txt'))
class Scraping_Google_Scholar():
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
        self.BGU_query='title'
        self.BGU_type='begins_with' #'exact'
        self.BGU_end='&tab=Everything&search_scope=MyInst_and_CI&vid=972BGU_INST:972BGU&lang=en&mode=advanced&offset=0&pcAvailability=false'
        self.http=httplib2.Http()
        
        
        driversPath=head_tail[0]
        #print(driversPath)
        sys.path.append(driversPath)
        self.Root=head_tail[0]
        self.ChromPath=os.path.join(head_tail[0],'chromedriver.exe')
        self.EdgePath=os.path.join(head_tail[0],'msedgedriver.exe')
        
        #wd=webdriver.Edge(self.EdgePath)
        #wd.get('edge://version')
        #self.Edge_userdata_path=wd.find_element_by_id('profile_path').text #('id','profile_path').text
        #self.Edge_userdata_path=wd.find_element_by_xpath('/html/body/div/table/tbody/tr[8]/td[2]').text
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
        
    '''        
    headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    params = {
      "q": 'Impetigo +burns',
      "hl": "en",
      "start" : 0,
      "num" : 10
    }
    '''
    def GS(self,params):
        #html = requests.get('https://scholar.google.com/scholar', headers=self._headers, params=params).text
        
        #***************************************************************************
        #Google Sholar log in
        #***************************************************************************
        '''
        html = requests.get('https://scholar.google.com/scholar', headers=self._headers, params=params)
        url=html.url
        wd=webdriver.Chrome(self.ChromPath,options=self.Chrome_options)
        wd.get(url)
        
        self.delay()
        self.delay()
        #time.sleep(10)
        
        try:
            #self.LoginInBGU(wd)
            self.LoginProxy(wd)
            self.delay()
            self.delay()
        except:
                ""
        self.delay()
        time.sleep(10)
        soup = BeautifulSoup(wd.page_source, 'lxml')
        print(soup)
        if (soup.find("div", {"class":"g-recaptcha-response"})):
           print("Page recaptcha find")
           recaptcha(wd,self.Root)
        else:
           print('Page recaptch not found')
        base_window = wd.current_window_handle
        ELs=wd.find_elements_by_class_name("gs_or_ggsm")
        print(ELs)
        for el in ELs:
            #print(1)
            lnks=(el.find_elements_by_tag_name('a'))
            i=0
            for lnk in lnks:
                print(i)
                print(lnk.get_attribute('href'))
                Numer_of_files=len(os.listdir(self.Pdfs_Download_path))
                #***********************************************************************
                #Artical Link
                #***********************************************************************
                lnk.send_keys(Keys.CONTROL + Keys.ENTER)
                self.delay()
                if len(wd.window_handles)==2:
                #if len(os.listdir(self.Pdfs_Download_path))==Numer_of_files:
                    wd.switch_to.window(wd.window_handles[1])
                    self.delay()
                    #try:
                    #     #self.LoginProxy(wd)
                    self.LoginBGU(wd)
                    self.delay()
                    #     time.sleep(5)
                    #except:
                        #print('E Step1')
                #if len(os.listdir(self.Pdfs_Download_path))>Numer_of_files:
                #    break       
                    #*********************************************************
                    # first attemp to push libkey
                    #*********************************************************
                    try:
                        #lnk2=wd.find_element_by_id('BigButton')
                        #textDemo = driver.findElement(By.xpath("//*[text()='Write and Earn']"));
                        #lnk2=wd.find_element_by_xpath("//*[contains(text(),'libkey.io')]")
                        lnk2=wd.find_elements_by_tag_name('a')
                        for lnk in lnk2:
                            print(i)
                            print(lnk.get_attribute('href'))
                            if 'libkey.io' in lnk.get_attribute('href'):
                                lnk.send_keys(Keys.CONTROL + Keys.ENTER)
                                print('found')
                                # try:
                                #     #self.LoginProxy(wd)
                                #     self.LoginBGU(wd)
                                #     self.delay()
                                #     time.sleep(2)
                                # except:
                                #     print('E step 1')
                                time.sleep(5)
                                break
                        if len(wd.window_handles)==3:
                            wd.switch_to.window(wd.window_handles[2])
                            #if len(os.listdir(self.Pdfs_Download_path))==Numer_of_files:
                            #try:
                            self.LoginBGU(wd)
                            self.delay()
                            #except:
                            #        ''
                        #lnk3=(lnk2.find_elements_by_tag_name('a'))
                        #print(lnk2.get_attribute('href'))
                        #lnk2.send_keys(Keys.CONTROL + Keys.ENTER)
                        self.delay()
                        #print(lnk3)
                        #lnk2.send_keys(Keys.CONTROL + Keys.ENTER)
                        #wd.get(temp)
                    except:
                         print("BigButton error1")    
                    
                #if len(os.listdir(self.Pdfs_Download_path))>Numer_of_files:
                #    break
                    #********************************************************
                    #Atemp for BGU serch
                    try:
                        lnk1=wd.find_element_by_id('ember615')
                        lnk1.send_keys(Keys.CONTROL + Keys.ENTER)
                        #lnk1.send_keys(Keys.ENTER)
                        #self.LoginProxy(wd)
                        #self.LoginBGU(wd)
                        self.delay()
                    except:
                            ''
                    
                #if len(os.listdir(self.Pdfs_Download_path))>Numer_of_files:
                #    break
                
                    if len(wd.window_handles)==3:
                        wd.switch_to.window(wd.window_handles[2])
                    #if len(os.listdir(self.Pdfs_Download_path))==Numer_of_files:
                        #try:
                        self.LoginBGU(wd)
                        self.delay()
                        #except:
                        #        ''
                        #******************************************************
                        #second attempt to push LibKey button
                        #******************************************************
                        try:
                            lnk2=wd.find_element_by_id('BigButton')
                            lnk3=(lnk2.find_elements_by_tag_name('a'))
                            #print(lnk2.get_attribute('href'))
                            lnk2.click()
                            self.delay()
                            time.sleep(5)
                            #print(lnk3)
                            #lnk2.send_keys(Keys.CONTROL + Keys.ENTER)
                            #wd.get(temp)
                        except:
                            print("BigButton error2")
                        #try:
                        #    self.delay()
                        #    self.LoginInBGU(wd)
                        #    self.delay()
                        #except:
                        #       ""
                        try:
                            
                            #lnk.click()
                            wd.close()  #close new tab
                            wd.switch_to.window(wd.window_handles[1])
                            wd.close()  #close new tab
                        except:
                            ""
                while len(wd.window_handles)>1:
                    wd.switch_to.window(wd.window_handles[len(wd.window_handles)-1])
                    wd.close()
                wd.switch_to.window(base_window)  #back to initial tab
                self.delay()
                i=i+1
                if len(os.listdir(self.Pdfs_Download_path))>Numer_of_files:
                    break
        
        wd.close()
        try:
            for f in os.listdir(self.Pdfs_Download_path):
                if ('(' in f and ')' in f):
                    os.remove(os.path.join(self.Pdfs_Download_path,f))
        except:
            ""            
        '''        
                
        '''            
        lnks=wd.find_elements_by_tag_name('a')
        for lnk in lnks:
            # get_attribute() to get all href
            print(lnk.get_attribute('href'))
            temp=(lnk.get_attribute('href'))
            if temp[-3:]=='lle':
                #wd.execute_script("window.open();")   #open new tab
                lnk.send_keys(Keys.CONTROL + Keys.ENTER)
                wd.switch_to.window(wd.window_handles[1])
                time.sleep(10)
                lnk1=wd.find_element_by_id('ember615')
                lnk1.send_keys(Keys.CONTROL + Keys.ENTER)
                wd.switch_to.window(wd.window_handles[2])
                #wd.get(temp)
                time.sleep(10)
                self.LoginInBGU(wd)
                self.delay()
                #lnk.click()
                wd.close()  #close new tab
                wd.switch_to.window(wd.window_handles[1])
                wd.close()  #close new tab
                wd.switch_to.window(base_window)  #back to initial tab
                time.sleep(10)
        
        soup = BeautifulSoup(wd.page_source, 'lxml')
        #soup = BeautifulSoup(html,"html.parser")
        # Scrape just PDF links
        #for pdf_link in soup.select('.gs_or_ggsm a'):
        #for pdf_link in soup.findAll("span","gs_ctg2"):
        if(soup.find("div", {"class":"g-recaptcha"})):
            print("Page recaptcha find")
            #recaptcha(wd)
        else:
            print(f"you in url {url}")

        soup = BeautifulSoup(wd.page_source, 'lxml')
        # html = requests.get('https://scholar.google.com/scholar', headers=self._headers, params=params).text
        # lines = html.split('\\n')
        # soup = BeautifulSoup(html,'lxml')
        # lines2 = soup.text.split('\\n')
        links=[]
        for pdf_link in soup.findAll("div","gs_or_ggsm"):
            for link in pdf_link.findAll('a'):
            #print(pdf_link.select('a')[0]['href'])
                print(link['href'])
                links.append(link['href'])
        #wd.close()        
        # if (link['href'].split('.')[-1] == "pdf"):
        #     urllib.request.urlretrieve(link['href'], f"{link['href'].split('/')[-1]}")
        # else:

        for link in links:
            if (link.split('.')[-1] == "pdf"):
                urllib.request.urlretrieve(link, f"{link.split('/')[-1]}")
                ##############
                # wd.get(link)
                # delay()
                # delay()
                # delay()
                # # keyboard.press(['ctrl', 's'])
                # time.sleep(1)
                # keyboard.press('enter')
                # ActionChains(wd).send_keys(Keys.CONTROL, 'S')
                # saveas = ActionChains(wd).key_down(Keys.CONTROL).send_keys('S').key_up(Keys.CONTROL).send_keys(
                #     'MyDocumentName').key_down(Keys.ALT).send_keys('S').key_up(Keys.ALT)
                # ActionChains(wd).key_down(Keys.CONTROL).send_keys('S').key_up(Keys.CONTROL).perform()
                # # Y=wd.find_elements(By.CSS_SELECTOR,"#icon > iron-icon")
                #############
                
            else:
                print('************************************')
                print(link)
                link.click()
                #wd.get("https://scholar.google.com"+link)
                #wd.get(link)
                self.LoginInBGU(wd)
                self.delay()
                self.delay()
                self.delay()
                self.delay()
                self.delay()
                self.delay()
                soup = BeautifulSoup(wd.page_source, 'lxml')
                if (soup.find("div", {"class":"g-recaptcha"})):
                    print("Page recaptcha find")
                #    recaptcha(wd)
                    self.delay()
                    soup = BeautifulSoup(wd.page_source, 'lxml')
                else:
                    print(f"you in url {url}")
                e=soup.find("a",{"class":"article-pdf-option ember-view"})
                if(e):
                        wd.get("https://libkey.io" + e.attrs['href'])
                        self.delay()
                        self.delay()
                        if("bgu.ac.il/login" in wd.current_url):
                            self.LoginInBGU(wd)
                            self.delay()
                            self.delay()
                        try:
                            urllib.request.urlretrieve(wd.current_url, f"{wd.current_url.split('/')[-1]}")
                        except:
                            response = requests.get(wd.current_url)
                            time.sleep(2)
                            #with open("C:\\Users\\לינוי\\PycharmProjects\\BGU\\venv\\text.pdf", 'wb') as f:
                            #    f.write(response.content)
                            #f.close()
                        #wd.close()    
                else:
                    e = soup.find("a", {"class": "article-web-link-option ember-view"})
                    if (e):
                            wd.get("https://libkey.io"+e.attrs['href'])
                            self.delay()
                            self.delay()
                            self.delay()
                            self.delay()
                            self.delay()
                            self.delay()
                            self.LoginInBGU(wd)
                            self.delay()
                            self.delay()
                            soup = BeautifulSoup(wd.page_source, 'lxml')
                            self.delay()
                            self.delay()
                            self.delay()
                            # x = wd.current_url.split('.com')[0]
                            # s=wd.find_element_by_class_name("pdf-link")
                            # s.click()
                            #x=wd.current_url
                            self.delay()
                            e = soup.find("meta",{"name":"citation_pdf_url"}).attrs['content']
                            #e = "https://bmj.com" + soup.find("a",{"class":"pdf-link"}).attrs['href']
                            try:
                                self.delay()
                                urllib.request.urlretrieve(e, f"{e.split('/')[-1]}")
                            except:
                                response = requests.get(wd.current_url)
                                time.sleep(2)
                                #with open("C:\\Users\\לינוי\\PycharmProjects\\BGU\\venv\\text.pdf", 'wb') as f:
                                #    f.write(response.content)
                                #f.close()
                            #wd.close()     
        # i=0
        # for pdf_link in soup.findAll("div","gs_or_ggsm"):
        #     i=i+1
        # #for pdf_link in soup.findAll('id','gs_res_ccl_mid'):
        #     #print(pdf_link)
        #     #print(i)
        #     #print(pdf_link.select("a[href$=lle]")) #$=lle 
        #     #print(pdf_link.select("a[href$=pdf]"))
            
        #     for pdf_file_link in pdf_link.contents[0]:
        #         pass
        #         #print('childe') 
        #         #print(pdf_file_link['href']) 
        #         #for pdf_file_link1 in pdf_file_link:
        #         #    print(2)
        #             #print(pdf_file_link1)
        #     #print(pdf_link['href'])
        #  { 
        # for link in soup.find_all('a', 
        #                   attrs={'href': re.compile("^https://")}):
        #     # display the actual urls
        #     #print(link.get('href'))
        #     try:
        #         response, content = self.http.request(link.get('href'))
    
        #         #html1 = requests.get(link)
        #         #subsoup=BeautifulSoup(html1,"html.parser")
        #         print ('--------------------------------------')
        #         for link2 in BeautifulSoup(content).find_all('a', href=True):
        #                 #links.append(link2['href'])
        #                 print(link2['href'])
        #     except :
        #         pass
        # ''' 
        
        html = requests.get('https://scholar.google.com/scholar', headers=self._headers, params=params)
        url=html.url
        wd=webdriver.Chrome(self.ChromPath,options=self.Chrome_options)
        wd.get(url)
        self.delay()
        time.sleep(10)
        base_window = wd.current_window_handle
        soup = BeautifulSoup(wd.page_source, 'lxml')
        #wd.close()
        data1=[]
        for results in soup.select('.gs_r.gs_or.gs_scl'):
            try:
                #print(results)
                a=results.select_one('.gs_ggs.gs_fl')
                #print(a)
                b=a.select_one('.gs_ggsd')
                #print(b)
                #Pdf=b.select_one('.gs_or_ggsm a')['href']
                c=b.select_one('.gs_or_ggsm')
                Pdf=c.select_one('a')['href']
                print(Pdf)
                data1.append({
                    'pdflink':Pdf})
            except :
                pass
        
        
        # # JSON data will be collected here
        data = []
        # # Container where all needed data is located
        html = requests.get('https://scholar.google.com/scholar', headers=self._headers, params=params).text
        soup = BeautifulSoup(html,"html.parser")
        for result in soup.select('.gs_ri'):
          title = result.select_one('.gs_rt').text
          title_link = result.select_one('.gs_rt a')['href']
          name = result.select_one('.gs_a').text
          publication_info = result.select_one('.gs_a').text
          snippet = result.select_one('.gs_rs').text
          cited_by = result.select_one('#gs_res_ccl_mid .gs_nph+ a')['href']
          related_articles = result.select_one('a:nth-child(4)')['href']
          try:
              all_article_versions = result.select_one('a~ a+ .gs_nph')['href']
          except:
              all_article_versions = None
          data.append({
        'title': title,
        'title_link': title_link,
        'name':name,
        'publication_info': publication_info,
        'snippet': snippet,
        'cited_by': f'https://scholar.google.com{cited_by}',
        'related_articles': f'https://scholar.google.com{related_articles}',
        'all_article_versions': f'https://scholar.google.com{all_article_versions}',
          })
        #wd=webdriver.Chrome(self.ChromPath,options=self.Chrome_options)
       
        for i in range(len(data)):
            wd.execute_script('''window.open("about:blank");''')  
            time.sleep(2)
            wd.switch_to.window(wd.window_handles[len(wd.window_handles)-1])
            #Numer_of_files=len(os.listdir(self.Pdfs_Download_path))
            try:
                wd.get(data[i]['title_link'])
                #base_window = wd.current_window_handle
                self.delay()
                time.sleep(5)
                #if len(os.listdir(self.Pdfs_Download_path))==Numer_of_files:
                try:
                    lnk2=wd.find_elements_by_tag_name('a')
                    for lnk in lnk2:
                        #print(i)
                        print(lnk.get_attribute('href'))
                        if 'libkey.io' in lnk.get_attribute('href'):
                            lnk.send_keys(Keys.CONTROL + Keys.ENTER)
                            print('found')
                            # try:
                            #     #self.LoginProxy(wd)
                            #     self.LoginBGU(wd)
                            #     self.delay()
                            #     time.sleep(2)
                            # except:
                            #     print('E step 1')
                            time.sleep(20)
                            #wd.close()
                            break
                except:
                    print('Big butons fail')
               
                while len(wd.window_handles)>1:
                    wd.switch_to.window(wd.window_handles[len(wd.window_handles)-1])
                    wd.close()
                wd.switch_to.window(wd.window_handles[0])  #back to initial tab
            except:
                print('fail Data %d'%i)
                
            # self.delay()    
                
        for i in range(len(data1)):
            wd.execute_script('''window.open("about:blank");''')  
            time.sleep(2)
            wd.switch_to.window(wd.window_handles[len(wd.window_handles)-1])
            #Numer_of_files=len(os.listdir(self.Pdfs_Download_path))
            print('Data1')
            print(i)
            try:
                wd.get(data1[i]['pdflink'])
                #base_window = wd.current_window_handle
                self.delay()
                time.sleep(5)
                #if len(os.listdir(self.Pdfs_Download_path))==Numer_of_files:
                try:
                    lnk2=wd.find_elements_by_tag_name('a')
                    for lnk in lnk2:
                        #print(i)
                        print(lnk.get_attribute('href'))
                        if 'libkey.io' in lnk.get_attribute('href'):
                            lnk.send_keys(Keys.CONTROL + Keys.ENTER)
                            print('found')
                            # try:
                            #     #self.LoginProxy(wd)
                            #     self.LoginBGU(wd)
                            #     self.delay()
                            #     time.sleep(2)
                            # except:
                            #     print('E step 1')
                            time.sleep(20)
                            break
                except:
                    print('Big butons fail')
                
                while len(wd.window_handles)>1:
                    wd.switch_to.window(wd.window_handles[len(wd.window_handles)-1])
                    wd.close()
                wd.switch_to.window(wd.window_handles[0])  #back to initial tab
                self.delay()  
                
            except:
                print('fail Data_1 %d'%i)
        curr=wd.current_window_handle
        try:
            for handle in wd.window_handles:
                wd.switch_to.window(handle)
                if handle!=curr:
                    wd.close()
        except:
            ""
                
        wd.quit()

            
                
                      
        try:
            for f in os.listdir(self.Pdfs_Download_path):
                if ('(' in f and ')' in f):
                    os.remove(os.path.join(self.Pdfs_Download_path,f))
        except:
            ""          
            
            
            
          
        #return (data , data1)
    
    def BGU(self,Title):
        
        
        
        pattern = r'\[[^\]]*\]'
        Title = re.sub(pattern, '', Title)
        print (Title)
        username='ozseadia'
        password='n2sebyJi'
        url=('https://'+ username +':' + password + '@' + 'primo.bgu.ac.il/discovery/search?query=%s,%s,%s%s'%(self.BGU_query,
                                                                          self.BGU_type,
                                                                          Title,
                                                                          self.BGU_end))    
        
        
        #wd=webdriver.Edge(self.EdgePath)
        #chrome_options = Options() 
        #chrome_options.add_experimental_option("detach", True)
        #Edge_options = OptionEdge() 
        #Edge_options.add_experimental_option("detach", True)
        wd=webdriver.Chrome(self.ChromPath,options=self.Chrome_options)
        #wd=webdriver.Edge(self.EdgePath,options=self.Edge_options)
        time.sleep(0.1)
        #wd.Chrome(options=chrome_options) 
        
        #wd=webdriver.Edge(self.EdgePath,options=self.Edge_options).get(url)
        wd.get(url)
        
        time.sleep(10)
        #Link=(wd.find_element_by_xpath('//*[@id="SEARCH_RESULT_RECORDID_cdi_proquest_miscellaneous_70289116"]/div[3]/div[2]/prm-search-result-availability-line/div[1]/div[1]/div/a'))
        Link=wd.find_element_by_class_name('browzine-direct-to-pdf-link')
        Link=(Link.get_attribute('href'))
        url=(Link[0:Link.find('://')+3]+ username +':' + password + '@' 
             +Link[Link.find('://')+3:])
        print(url)
        #wd.get(Link.get_attribute("href"))
        wd.get(url)
        
        time.sleep(10)
        print(wd.current_url)
        
        try:
            LoginFlag=0
            # head to proxy login page
            wd.get(wd.current_url)
            # find username/email field and send the username itself to the input field
            
            wd.find_element_by_name('user').send_keys(username)
            
            #wd.find_eleme ("login_field").send_keys(username)
            # 
            wd.find_element_by_name('pass').send_keys(password)
            #driver.find_element_by_id("password").send_keys(password)
            # click login button
            time.sleep(1)
            wd.find_element_by_xpath("/html/body/form/input[4]").click()
            time.sleep(5)
            LoginFlag=1
            print(LoginFlag)
        except:
            print(LoginFlag)
                
        #driver.quit()
        print(not LoginFlag)
        if not LoginFlag : 
            
            shell = win32com.client.Dispatch("WScript.Shell")   
            shell.Sendkeys(username)  
            shell.Sendkeys("{TAB}")
            shell.Sendkeys(password) 
            shell.Sendkeys("{ENTER}")
            time.sleep(0.1)
            time.sleep(1)
        #wd.get(wd.current_url)
        print(wd.current_url)
        time.sleep(5)
        #wget.download(wd.current_url,r'G:\Oz\fiveer\Dani_Velinchick\Burns\PDFs\aaa.pdf')
        try:
            wd.switchTo().alert();
            shell = win32com.client.Dispatch("WScript.Shell")   
            shell.Sendkeys(username)
            time.sleep(1)
            shell.Sendkeys("{TAB}")
            time.sleep(1)
            shell.Sendkeys(password)
            time.sleep(1)
            shell.Sendkeys("{ENTER}")
            time.sleep(0.1)
            time.sleep(5)
        except:
                pass
        url=(wd.current_url)    
        #wd.get(url)
        time.sleep(2)
        wd.close()
        time.sleep(5)
        
        
        
        
        #pyautogui.hotkey('ctrl','s')
        #time.sleep(5)
        #pyautogui.press('enter')
        #wd.find_element_by_id('download').click()
        #wd.close()
        '''
        filename=r'G:\Oz\fiveer\Dani_Velinchick\Burns\PDFs\test.pdf'
        #response = urllib.request.urlopen(wd.current_url)    
        #file = open(filename + ".pdf", 'wb')
        #file.write(response.read())
        #file.close()
        #print(L)
        #L=wd.find_element_by_id("profile_path").get_attribute('text')
        #L=wd.find_element('id','profile_path').text
        
        response = requests.get(wd.current_url)
        time.sleep(2)
        with open(filename, 'wb') as f:
            f.write(response.content)
        f.close()
        '''    
        
        '''
        html = requests.get(url).text
        #soup = BeautifulSoup(html,"html.parser")
        soup = BeautifulSoup(html,"html.parser")
        # Scrape just PDF links
        #print(1)
        for pdf_link in soup.findAll('div'):
            #print(1)
            #pdf_file_link = pdf_link['href']
            print(1)
            print(pdf_link)
        '''
        return (Link)  
    
    
    
    
    def LoginBGU(self,driver):
        try:
            username = self.username
            password = self.password
            # head to proxy login page
            LoginFlag=0
            driver.get(driver.current_url)
            # find username/email field and send the username itself to the input field
    
            driver.find_element_by_name('user').send_keys(username)
    
            # wd.find_eleme ("login_field").send_keys(username)
            #
            driver.find_element_by_name('pass').send_keys(password)
            # driver.find_element_by_id("password").send_keys(password)
            # click login button
            driver.find_element_by_xpath("/html/body/form/input[4]").click()
            time.sleep(1)
            print(LoginFlag=1)
        except:
            print('BGU fail')
    def LoginProxy(self,driver):
        try:
            username = self.username
            password = self.password
            #if not LoginFlag :     
            shell = win32com.client.Dispatch("WScript.Shell")   
            shell.Sendkeys(username)  
            shell.Sendkeys("{TAB}")
            shell.Sendkeys(password) 
            shell.Sendkeys("{ENTER}")
            time.sleep(0.1)
            time.sleep(1)
                
            #wd.get(wd.current_url)
        except:
             print ('Proxy fail')
                
                
        
        
    def delay(self):
        time.sleep(random.randint(4,7))
        
    def main (self,query,n,hl='en'):
        J=math.floor(n/10)
        if J>0:
            for i in range(0,J):
                params = {
                  "q": query,
                  "hl": hl,
                  "start" : i,
                  "num" : 10
                }
                data=self.GS(params)
                time.sleep(2)
                # print(len(data))
                # for l in range (len(data)):
                #     #try:
                #         self.BGU(data[l]['title'])
                #     #except:
                #         print ('article was not saved')
         
        if (n%10)>0:
            params = {
              "q": query,
              "hl": hl,
              "start" : J,
              "num" : n%10
            }
            data=self.GS(params)
            time.sleep(2)
            #print(len(data))
            # for l in range (len(data)):
            #     try:
            #         self.BGU(data[l]['title'])
            #     except:
            #         print ('article was not saved')
        
        #creat Folder with the Key words name
        folder_path =os.path.join(self.Pdfs_Download_path,query)
        if not(os.path.exists(folder_path)):
            os.mkdir(folder_path)
        
    #try:
        for f in os.listdir(self.Pdfs_Download_path):
            if f.endswith(".pdf"):
                shutil.move(os.path.join(self.Pdfs_Download_path,f),folder_path)    
    #except:
    #    ""
        
            
                
                        
                        