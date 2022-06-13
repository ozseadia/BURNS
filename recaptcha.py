# -*- coding: utf-8 -*-
"""
Created on Mon May 16 23:44:34 2022

@author: OzSea
"""
import time
import urllib
from selenium.webdriver.common.keys import Keys

from pydub import AudioSegment
import speech_recognition as sr
#import os
#Path=os.path.dirname(__file__)
#import ffmpy
def delay():
    time.sleep(5)
    
def recaptcha(driver,Patch):
    #Patch="C:\\Users\\לינוי\\Desktop\\Workstaion\\OpenUser\\"
#     frames = driver.find_elements_by_tag_name("iframe")
#     driver.switch_to.frame(frames[0]);
#     delay()
#     a=driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div/div/span").get_attribute("aria-checked")
#     print()
#     while driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div/div/span").get_attribute("aria-checked") == "false" :

    # switch to recaptcha frame
    frames = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[0]);
    delay()
    delay()

    # click on checkbox to activate recaptcha
    driver.find_element_by_class_name("recaptcha-checkbox-border").click()
    # switch to recaptcha audio control frame
    i=0

    driver.switch_to.default_content()
    frames = driver.find_element_by_xpath("/html/body/div/div[4]").find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[0])
    delay()
    # delay()
    # delay()
    # delay()
    # click on audio challenge
    driver.find_element_by_id("recaptcha-audio-button").click()
    delay()
    driver.switch_to.default_content()
    delay()
    frames = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[-1])
    try:
        while i < 6:
            delay()
            #click on the play button
           # driver.find_element_by_id("recaptcha-reload-button").click()
            driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()

            src = driver.find_element_by_id("audio-source").get_attribute("src")
            urllib.request.urlretrieve(src, Patch+"sample.mp3")
            sound = AudioSegment.from_mp3(Patch+"sample.mp3")
            sound.export(Patch+"sample.wav", format="wav")
            sample_audio = sr.AudioFile(Patch+"sample.wav")
            r = sr.Recognizer()
            with sample_audio as source:
                 audio = r.record(source)

            # translate audio to text with google voice recognition
            key = r.recognize_google(audio)
            print("[INFO] Recaptcha Passcode: %s" % key)

            # key in results and submit
            # for letter in key.lower().split():
            #     driver.find_element_by_id("audio-response").send_keys(letter)
            #     delay()
            driver.find_element_by_id("audio-response").send_keys(key)
            delay()
            driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
            delay()
            print("[INFO] Validation Successful")
            # driver.switch_to.default_content()
            # driver.find_element_by_id("recaptcha-verify-button").click()
            delay()
            i=i+1
    except:
        print('Robot Fail')
        ""