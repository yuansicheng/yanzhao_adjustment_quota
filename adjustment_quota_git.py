# -*- coding: utf-8 -*-
#Author: YuanSicheng
#Email: yuansc23@outlook.com

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import sys
#sys.path.append("/opt/google/chrome")
import smtplib
from email.mime.text import MIMEText
import datetime

from selenium.webdriver.chrome.service import Service
import os
import argparse
#import lxml

def get_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--run_os', type=str, default='linux')
    parser.add_argument('--phone', type=str)
    parser.add_argument('--passwd', type=str)
    parser.add_argument('--driver_path', type=str)
    parser.add_argument('--majors', nargs='+', type=str)
    parser.add_argument('--mail163_user', type=str)
    parser.add_argument('--mail163_pass', type=str)
    parser.add_argument('--receivers', nargs='+', type=str)
    
    return parser.parse_args()

#initialize
def initializeDriver(browser_name='google', driver='/opt/google/chrome/chromedriver'):
    print('initializeDriver: create a '+browser_name+' driver')
    google_driver = driver
    if browser_name =='google':
        c_service = Service(google_driver)
        c_service.command_line_args()
        c_service.start()
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(executable_path=google_driver,chrome_options=options)
    return browser, c_service

def login(browser, adjustment_url='https://yz.chsi.com.cn/sytj/tj/qecx.html', \
          phone='', passwd=''):
    print('login...')
    browser.get(adjustment_url)
    
    phone_form_selector = '#username'
    phone_form = browser.find_element_by_css_selector(phone_form_selector)
    phone_form.send_keys(phone)
    
    passwd_form_selector = '#password'
    passwd_form = browser.find_element_by_css_selector(passwd_form_selector)
    passwd_form.send_keys(passwd)
    
    login_button_selector = '#fm1 > div.yz-pc-loginbtn > input.yz_btn_login'
    login_button = browser.find_element_by_css_selector(login_button_selector)
    login_button.click()
    
    sleep(2)
    print('login successful')
    return

def isRecent1h(t):
    if '天' not in t and '小时' not in t:
        return True
    return False

def selectQuota(browser, majors=['金融', '国际商务']):
    data = []
    major_form_selector = '#zyxx'
    search_button_selector = '#tj_seach_form > table > tbody > tr > td:nth-child(11) > a'
    nextpage_button_xpath = "//*[text()='下一页']"
    
    try:
        major_form = browser.find_element_by_css_selector(major_form_selector)
    except:
        login()
    
    major_form = browser.find_element_by_css_selector(major_form_selector)
    search_button = browser.find_element_by_css_selector(search_button_selector)
      
    
    for major in majors:
        print(major)
        sleep(2)
        major_form.clear()
        major_form.send_keys(major)
        search_button.click()
        
        #get
        
        while 1:
            sleep(2)
            
            html = browser.page_source
            soup = BeautifulSoup(html, "html.parser")
            
            '''
            with open('C:\\Users\\Dell\\Desktop\\1.txt', 'w', encoding='utf8') as f:
                f.write(soup.prettify())
            '''
            
            table = soup.find_all('table', attrs={'class':'tj-table'})[-1]
            
            
            for tr in table.find_all('tr')[1:]:
                data_this = []
                for td in tr.find_all('td')[:7]:
                    if td.find_all('a'):
                        data_this.append(td.find_all('a')[0].contents[0])
                    else:
                        data_this.append(td.contents[0])
                #print(data_this)
                    
                if len(data_this) == 7:
                    if isRecent1h(data_this[-1]):
                        data.append(data_this)
            

            try:
                nextpage_button = browser.find_element_by_xpath(nextpage_button_xpath)
            except:
                break
                
            if int(nextpage_button.value_of_css_property('color').split(',')[1]) < 150:
                nextpage_button = browser.find_element_by_class_name('next')
                #print(nextpage_button)
                nextpage_button.click()
                print('nextpage_button.click()')
                #print(len(data))
            else:
                break
                
                

    if data:
        data_full = [d for d in data if '非' not in d[-3]]
        data_notfull = [d for d in data if '非' in d[-3]]
        data = []
        if data_full:
            data += ['全日制:']
            data += data_full
            data += ['']
        if data_notfull:
            data += ['非全日制:']
            data += data_notfull
        data = '\r\n'.join([str(d) for d in data])
        print(data)
        return data
    else:
        return '没有新增院校...'

    
    
def setupSmtp(mail_user, mail_pass):
    
    mail_host = 'smtp.163.com'   
    port = 465
    
    try:
        smtpObj = smtplib.SMTP_SSL(host=mail_host) 
        smtpObj.connect(host=mail_host,port=port)
        #smtpObj.starttls()
        smtpObj.login(mail_user,mail_pass) 
        print('Email login successful...')
        return smtpObj
    except Exception as e:
        print('Email login failed...')
        print(e)
        return False

def sendMail(title, content, mail_user, mail_pass, receivers=[]):
    smtpObj = None
    n = 0
    while not smtpObj and n<10:
        smtpObj = setupSmtp(mail_user, mail_pass)
        n += 1
        sleep(5)
    sender = mail_user
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = title
    message['from'] = sender
    for receiver in receivers:
        message['to'] = receiver
        flag = False
        n = 0
        while not flag and n < 10:
            try:
                smtpObj.sendmail(sender,receiver,message.as_string())
                flag = True
            except Exception as e:
                print('Send Failed...')
                print(e)
                n += 1
                sleep(5)
    return True
        
    


def getTimeStamp():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    

        
        
        
        
    
    
    
if __name__ == '__main__':
    
    #get args
    parser = get_parser()
    run_os = parser.run_os
    phone = parser.phone
    passwd = parser.passwd
    driver_path = parser.driver_path
    majors = parser.majors
    mail163_user = parser.mail163_user
    mail163_pass = parser.mail163_pass
    receivers = parser.receivers
    
    if not receivers:
        print('No receivers appointed')
        sys.exit(0)
    
    #clean threads if running on linux
    if run_os.lower() =='linux':   
        os.system('kill -9 | pgrep chrome')
    print(getTimeStamp())
    print ("Python Version {}".format(str(sys.version).replace('\n', '')))
    #sys.exit(0)
    
    adjustment_url = 'https://yz.chsi.com.cn/sytj/tj/qecx.html'
    browser, c_service = initializeDriver(driver=driver_path)
    login(browser, phone=phone, passwd=passwd)
    
    data = selectQuota(browser, majors=majors)
    
    browser.quit()
    c_service.stop()
        
    
    print('Send mail')
    if not data:
        print('No message!')
        sys.exit(0)
    if sendMail('新增调剂院校 {}'.format(getTimeStamp()), data, \
                mail163_user, mail163_pass, receivers=receivers):
        print('Send successful!')


    
