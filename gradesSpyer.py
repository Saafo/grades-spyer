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
        self.password = '请在这里填写服务端邮箱密码' #邮箱密码
        self.to_addr = '请在这里填写接收通知的邮箱' #收信息邮箱
        self.smtp_server = '请在这里填写服务端邮箱stmp服务器地址'#示例：'smtp.163.com'
        self.pop3_server = '请在这里填写服务端邮箱pop3服务器地址'#示例：'pop3.163.com'
        self.server = smtplib.SMTP(self.smtp_server, 25)
        # self.server.set_debuglevel(1)    # 打印出和SMTP服务器交互的所有信息
        # self.server.login(from_addr, password)   # 登录SMTP服务器
        # self.server.sendmail(from_addr, [to_addr], msg.as_string())    # 发邮件

    def mailMeInfo(self,state,content):
        if(state == 0):
            subject = '你有新的总评成绩发布'
        elif(state == 1):
            subject = '程序运行产生错误，已重启程序'
        elif(state == 2):
            subject = '你有新的平时成绩发布'
        msg = MIMEText(content,'plain','utf-8')
        msg['subject'] = Header(subject,'utf-8')
        msg['from'] = 'GradesSpyer<'+self.from_addr+'>'
        msg['to'] = self.to_addr
        self.server.set_debuglevel(1)    # 打印出和SMTP服务器交互的所有信息
        self.server.login(self.from_addr, self.password)   # 登录SMTP服务器
        self.server.sendmail(self.from_addr, [self.to_addr], msg.as_string())    # 发邮件


    def mailMeCaptcha(self,state):
        #上传图片 #TODO删掉
        # image_filename = os.path.basename('./screenshot.png')
        # Headers = {"Authorization":"dhlfCDRwzzuy5vc6dhz6riZ9nMVSEAKJ"}
        # files = {'smfile': (image_filename,open('./captchaImg.png','rb'))}
        # url = "https://sm.ms/api/v2/upload/"
        # Response = requests.post(url,headers=Headers,files=files)
        # Data = Response.json()
        # Success = Data['success']
        # capatchaUrl = ""
        # if(Success == "true"):
        #     capatchaUrl = Data['data']['url']
        #构造邮件
        if(state == 0):
            subject = '登录失效，请回复验证码以重新登录'
        elif(state == 1):
            subject = '验证码或密码错误，请尝试回复验证码以重新登录'
        elif(state == 2):
            subject = '启动程序，请回复验证码以登录'

        msg = MIMEMultipart('alternative')
        msg['subject'] = Header(subject,'utf-8')
        msg['from'] = 'GradesSpyer<'+self.from_addr+'>'
        msg['to'] = self.to_addr

        img = open('./captchaImg.png','rb')
        msgImage = MIMEImage(img.read())
        img.close()
        # msgImage.add_header('Content-ID','<captchaImg>')
        msg.attach(msgImage)
        html = '''
        <html>
          <head></head>
          <body>
            <p>请将附件验证码作为`邮件主题`回复到本邮箱<br>
            </p>
          </body>
        <html>
        '''
            # <br>验证码上传成功状态：'''+str(Success)+'''</br>
            # <br><img src='cid:captchaImg'></br> 加了这排网易就会报554,b'DT:SPM垃圾邮件报错，迫不得已注释掉
        htm = MIMEText(html,'html','utf-8')
        msg.attach(htm)
        #发邮件
        self.server.set_debuglevel(1)    # 打印出和SMTP服务器交互的所有信息
        self.server.login(self.from_addr, self.password)   # 登录SMTP服务器
        self.server.sendmail(self.from_addr, [self.to_addr], msg.as_string())    # 发邮件
        with open("./time.txt",'w') as f: #记录最近发送验证码的时间
            f.write(str(time.time()))

    def recvCaptcha(self):
        def guess_charset(msg):
            charset = msg.get_charset()
            if charset is None:
                content_type = msg.get('Content-Type', '').lower()
                pos = content_type.find('charset=')
                if pos >= 0:
                    charset = content_type[pos + 8:].strip()
            return charset
        def decode_str(s):
            value, charset = decode_header(s)[0]
            if charset:
                value = value.decode(charset)
            return value
        with open("./time.txt",'r') as f: #读取最近发送验证码的时间
            sent_pic_captcha_time = float(f.read())

        # 开始循环
        # counter = 0 # 计数菌#TODO删除
        while (True):
            time.sleep(120)
            # 连接到POP3服务器:
            server = poplib.POP3(self.pop3_server)
            # 可以打开或关闭调试信息:
            server.set_debuglevel(1)
            # 可选:打印POP3服务器的欢迎文字:
            # print(server.getwelcome().decode('utf-8'))
            # 身份认证:
            server.user(self.from_addr)
            server.pass_(self.password)
            # stat()返回邮件数量和占用空间:
            # print('Messages: %s. Size: %s' % server.stat())
            # list()返回所有邮件的编号:
            resp, mails, octets = server.list()
            # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
            # print(mails)
            for index in range(len(mails),len(mails)-5,-1):
                resp, lines, octets = server.retr(index)
                # lines存储了邮件的原始文本的每一行,
                # 可以获得整个邮件的原始文本:
                msg_content = b'\r\n'.join(lines).decode('utf-8')
                # 准备解析邮件:
                msg = Parser().parsestr(msg_content)
                raw_info_from = msg.get("From")
                hdr, from_addr = parseaddr(raw_info_from)
                if(from_addr == mymail.to_addr): #如果是指定邮箱发回来的邮件
                    sent_string_captcha_time = time.mktime(time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S'))
                    #如果最近一条指定邮箱发来的邮件比最近发送的验证码时间晚 +100:修正163服务器与本地时间差
                    if(sent_string_captcha_time + 100 > sent_pic_captcha_time): 
                        captcha = decode_str(msg.get("Subject"))
                        server.quit()
                        return captcha
                    break
                continue
            server.quit()
            # if(counter < 2):
            # time.sleep(120)
            #     counter += 1
            # elif(counter < 5):
            #     time.sleep(300)
            #     counter += 1
            # else:
            #     time.sleep(1800)
            #     counter = 0


def captchaShot():
    #获取截图
    driver.get_screenshot_as_file('./screenshot.png')
    #获取指定元素位置
    element = driver.find_element_by_id('captchaImg')
    left = int(element.location['x'])
    top = int(element.location['y'])
    right = int(element.location['x'] + element.size['width'])
    bottom = int(element.location['y'] + element.size['height'])
    #通过Image处理图像
    im = Image.open('./screenshot.png')
    im = im.crop((2*left, 2*top, 2*right, 2*bottom)) #TODO不知道是不是和代码机是2k屏有关系
    im.save('./captchaImg.png')

def login(state,manual):
    driver.get("http://portal.uestc.edu.cn")
    try:
        driver.find_element_by_id("username").send_keys("请在这里填写信息门户账号")
        driver.find_element_by_id("password").send_keys("请在这里填写信息门户密码")
        driver.find_element_by_id("captchaResponse").click()
        if(manual == 0): #通过邮件自动填写验证码
            captchaShot()
            mymail.mailMeCaptcha(state)
            capResult = mymail.recvCaptcha()
            driver.find_element_by_id("captchaResponse").send_keys(capResult)
        else: #通过手动填写验证码
            while(True): #死循环到找不到验证码输入框，产生错误跳转到finally
                driver.find_element_by_id("captchaResponse")
                time.sleep(3)
        time.sleep(5)
        driver.find_elements_by_class_name("auth_login_btn")[0].click() #如果还停留在登录页，点击登录
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
                with open("./finalscore.txt",'w') as f:
                    for i in range(num):
                        td = tr[i].find_elements_by_tag_name("td")
                        f.write(td[3].text+','+td[6].text+'\n')
            else: #如果已经有存在记录，则遍历查找不同
                with open("./finalscore.txt",'r') as f:
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
                    with open("./finalscore.txt",'a+') as f:
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
                with open("./usualscore.txt",'w') as f:
                    for i in range(num):
                        td = tr[i].find_elements_by_tag_name("td")
                        f.write(td[3].text+','+td[6].text+'\n')
            else: #如果已经有存在记录，则遍历查找不同
                with open("./usualscore.txt",'r') as f:
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
                    mail_string = "科目名称,分数：\n"
                    with open("./usualscore.txt",'a+') as f:
                        for item in unrecord_subject_indexs:
                            td = tr[item].find_elements_by_tag_name("td")
                            f.write(td[3].text+','+td[6].text+'\n')
                            mail_string += td[3].text+','+td[6].text+'\n'
                    mymail.mailMeInfo(2,mail_string)

            time.sleep(300)
        except NoSuchElementException:
            if(login(0,0)):
                pass
            else:
                restart()
        # except Exception as e:
        #     mymail.mailMeInfo(1,'错误信息：\n' + str(e))
        #     restart()


def restart():
    driver.quit()
    python = sys.executable
    os.execl(python,python,sys.argv[0])


def main(manual):
    # ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
    # options = webdriver.ChromeOptions()
    # options.add_argument("user-agent="+ua)
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # driver = webdriver.Chrome(chrome_options=options,executable_path='./chromedriver')#chrome_options=browser)
    if(login(2,manual)): #登录
        # driver.get(final_score_table_url)
        compare()
    else: #重启程序
        restart()

if __name__ == '__main__':
    # 参数解析模块
    args = sys.argv[1:]
    manual = 0
    try:
        opts, arg = getopt.getopt(args, "m", ["manual"])
    except getopt.GetoptError:
        print('参数错误！')
        exit(-1)
    for opt, arg in opts:
        if opt in ('-m','-manual'):
            manual = 1
        else:
            manual = 0
    # main module
    mymail = Mymail()
    driver = webdriver.Firefox(executable_path='./geckodriver')
    final_score_table_url = "http://eams.uestc.edu.cn/eams/teach/grade/course/person!search.action?semesterId=243&projectType="
    try: 
        main(manual)
    except BaseException:
        with open('./log.txt','a+') as f:
            f.write(time.asctime(time.localtime(time.time())) + '\n' + traceback.format_exc())
        mymail.mailMeInfo(1,time.asctime(time.localtime(time.time())) + '\n' +'错误信息：\n' + traceback.format_exc())
    finally: #不行就重启 重启能解决99%的问题
        restart()