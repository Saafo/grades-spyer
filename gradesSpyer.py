from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from PIL import Image
import requests
import time
import json
import os
import sys
import getopt
import smtplib
import traceback
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import poplib
from email.header import decode_header
from email.utils import parseaddr
from email.parser import Parser


class Mymail:
    def __init__(self):
        self.from_addr = '请在这里填写服务端邮箱' #发送邮箱
        self.password = '请在这里填写服务端邮箱授权码' #邮箱密码
        self.to_addr = '请在这里填写接收通知的邮箱' #收信息邮箱
        self.smtp_server = '请在这里填写服务端邮箱stmp服务器地址'#示例：'smtp.163.com'
        self.pop3_server = '请在这里填写服务端邮箱pop3服务器地址'#示例：'pop3.163.com'
        # self.server = smtplib.SMTP_SSL(self.smtp_server,465) #为兼容服务器和更好的安全性采用SSL 465端口登录

    def mailMeInfo(self,state,content):
        if(state == 0):
            subject = '你有新的总评成绩发布'
        elif(state == 1):
            subject = '程序运行产生错误，已重启程序'
        elif(state == 2):
            subject = '你有新的平时成绩发布'
        log(subject+'\n'+content)
        msg = MIMEText(content,'plain','utf-8')
        msg['subject'] = Header(subject,'utf-8')
        msg['from'] = 'GradesSpyer<'+self.from_addr+'>'
        msg['to'] = self.to_addr
        self.server = smtplib.SMTP_SSL(self.smtp_server,465) #为兼容服务器和更好的安全性采用SSL 465端口登录
        self.server.set_debuglevel(1)    # 打印出和SMTP服务器交互的所有信息
        self.server.login(self.from_addr, self.password)   # 登录SMTP服务器
        self.server.sendmail(self.from_addr, [self.to_addr], msg.as_string())    # 发邮件

    def mailMeLogin(self):
        #构造邮件
        subject = '登录失效，请远程连接桌面以登录'

        msg = MIMEMultipart('alternative')
        msg['subject'] = Header(subject,'utf-8')
        msg['from'] = 'GradesSpyer<'+self.from_addr+'>'
        msg['to'] = self.to_addr

        #发邮件
        self.server = smtplib.SMTP_SSL(self.smtp_server,465)
        self.server.set_debuglevel(1)    # 打印出和SMTP服务器交互的所有信息
        self.server.login(self.from_addr, self.password)   # 登录SMTP服务器
        self.server.sendmail(self.from_addr, [self.to_addr], msg.as_string())    # 发邮件
        with open("./time.txt",'w',encoding='utf-8') as f: #记录最近发送验证码的时间
            f.write(str(time.time()))


def login(state,manual):
    driver.get("http://portal.uestc.edu.cn")
    try:
        driver.find_element_by_id("username").send_keys("请在这里填写信息门户账号")
        driver.find_element_by_id("password").send_keys("请在这里填写信息门户密码")
        if(manual == 0): #通过邮件提醒
            mymail.mailMeLogin()
        while(True): #死循环到找不到验证码输入框，产生错误跳转到finally
            driver.find_element_by_id("captchaResponse")
            time.sleep(3)
        time.sleep(5)
        driver.find_elements_by_class_name("auth_login_btn")[0].click() #如果还停留在登录页，点击登录
    except KeyboardInterrupt:
        safequit()
    finally:
        time.sleep(2)
        try:
            driver.find_element_by_id("msg") #验证码或密码错误
        except NoSuchElementException:
            driver.get(final_score_table_url) #重定向，用来防止各种奇奇怪怪的教务系统错误
            driver.get(final_score_table_url) #跳过确认重复登录页面
            try:
                driver.find_element_by_class_name("gridtable") #如果成功登陆，能获取课表
                return True
            except NoSuchElementException:
                return False
        login(1,manual) #验证码或密码错误,则重新尝试登录


def compare():
    while(True):
        try:
            #总评成绩查询
            driver.get(final_score_table_url)
            table = driver.find_element_by_class_name("gridtable")
            tr = table.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
            num = len(tr)
            if(os.path.exists("./finalscore.txt") == False): #如果还没有已存在的记录
                with open("./finalscore.txt",'w',encoding='utf-8') as f:
                    for i in range(num):
                        td = tr[i].find_elements_by_tag_name("td")
                        f.write(td[3].text+','+td[6].text+'\n')
            else: #如果已经有存在记录，则遍历查找不同
                with open("./finalscore.txt",'r',encoding='utf-8') as f:
                    records = f.readlines()
                record_subject_names = []
                unrecord_subject_indexs = []
                for item in records:
                    record_subject_names.append(item.split(',')[0])
                #开始比对
                for i in range(num):
                    td = tr[i].find_elements_by_tag_name("td")
                    name = td[3].text
                    for rname in record_subject_names:
                        if(name == rname): #已经存在记录
                            break #开始比较下一个
                        elif(rname == record_subject_names[len(record_subject_names) - 1]): #扫描完未找到记录
                            unrecord_subject_indexs.append(i)
                #如果有新增项
                if(unrecord_subject_indexs != []):
                    mail_string = "科目名称 , 分数：\n"
                    with open("./finalscore.txt",'a+',encoding='utf-8') as f:
                        for item in unrecord_subject_indexs:
                            td = tr[item].find_elements_by_tag_name("td")
                            f.write(td[3].text+','+td[6].text+'\n')
                            mail_string += td[3].text+' , '+td[6].text+'\n'
                    mymail.mailMeInfo(0,mail_string)
            #平时成绩查询
            driver.get("http://eams.uestc.edu.cn/eams/home!childmenus.action?menu.id=844")
            time.sleep(1)
            driver.find_element_by_css_selector("a[enname='/Usual-Grade-Std']").click()
            time.sleep(1)
            table = driver.find_element_by_class_name("gridtable")
            tr = table.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
            num = len(tr)
            if(os.path.exists("./usualscore.txt") == False): #如果还没有已存在的记录
                with open("./usualscore.txt",'w',encoding='utf-8') as f:
                    for i in range(num):
                        td = tr[i].find_elements_by_tag_name("td")
                        f.write(td[3].text+','+td[6].text+'\n')
            else: #如果已经有存在记录，则遍历查找不同
                with open("./usualscore.txt",'r',encoding='utf-8') as f:
                    records = f.readlines()
                record_subject_names = []
                unrecord_subject_indexs = []
                for item in records:
                    record_subject_names.append(item.split(',')[0])
                #开始比对
                for i in range(num):
                    td = tr[i].find_elements_by_tag_name("td")
                    name = td[3].text
                    for rname in record_subject_names:
                        if(name == rname): #已经存在记录
                            break #开始比较下一个
                        elif(rname == record_subject_names[len(record_subject_names) - 1]): #扫描完未找到记录
                            unrecord_subject_indexs.append(i)
                #如果有新增项
                if(unrecord_subject_indexs != []):
                    mail_string = "科目名称 , 分数：\n"
                    with open("./usualscore.txt",'a+',encoding='utf-8') as f:
                        for item in unrecord_subject_indexs:
                            td = tr[item].find_elements_by_tag_name("td")
                            f.write(td[3].text+','+td[6].text+'\n')
                            mail_string += td[3].text+' , '+td[6].text+'\n'
                    mymail.mailMeInfo(2,mail_string)
            log('已成功刷新成绩数据\n')
            time.sleep(300) # 默认5分钟（300秒）刷新一次，不建议更频繁
        except KeyboardInterrupt:
            safequit()
        except NoSuchElementException:
            if(login(0,0)):
                pass
            else:
                restart()


def restart():
    driver.quit()
    python = sys.executable
    os.execl(python,python,sys.argv[0])

def safequit():
    driver.quit()
    os._exit(0)

def log(info):
    with open('./log.txt','a+',encoding='utf-8') as f:
        f.write(time.asctime(time.localtime(time.time())) + '\n' + info + '\n')


def main(manual):
    if(login(2,manual)): #登录
        compare()
    else: #重启程序
        restart()

if __name__ == '__main__':
    # 参数解析模块
    args = sys.argv[1:]
    manual = 1
    try:
        opts, arg = getopt.getopt(args, "m", ["manual"])
    except getopt.GetoptError:
        print('参数错误！')
        exit(-1)
    for opt, arg in opts:
        if opt in ('-m','--manual'):
            manual = 1
        else:
            manual = 0
    # main module
    mymail = Mymail()
    driver = webdriver.Firefox(executable_path='./geckodriver')
    final_score_table_url = "http://eams.uestc.edu.cn/eams/teach/grade/course/person!search.action?semesterId=243&projectType="
    try: 
        main(manual)
    except KeyboardInterrupt:
        safequit()
    except BaseException:
        log(traceback.format_exc())
        mymail.mailMeInfo(1,time.asctime(time.localtime(time.time())) + '\n' +'错误信息：\n' + traceback.format_exc())
    finally: #不行就重启 重启能解决99%的问题
        restart()