# 今天出成绩了吗 | UESTC成绩监控脚本
> 花了三天时间写了个脚本，可以挂在服务器/自己电脑上随时监控成绩变化,变化时会有邮件提醒  
> 暂时还有很多不足，欢迎提issue/PR

[TOC]
## 脚本环境：
* `Python 3` 以上版本，[点击下载](https://www.python.org/)
* pip
* `Selenium 2.0` 以上版本
* `firefox 浏览器` [点击下载](http://www.firefox.com.cn/) | [为什么不用Chrome](#关于没有采用Chrome的问题：)
* `geckodriver`用于selenium控制firefox的程序，[点击下载](https://github.com/mozilla/geckodriver/releases)
## 准备工作：
* 你的一个**很少接收邮件的邮箱**作为发送信息的`服务端邮箱`
* 你的一个`常用邮箱`
* 一台服务器/不关机的电脑
## 使用步骤：
* 安装Python
* 安装Selenium:
    ```bash
    pip install selenium
    ```
* 配置个人信息：
  * 打开 gradesSpyer.py
  * line 24-28 添加邮箱信息  
    服务端邮箱请**一定**要添加**很少**收到邮件的邮箱
  * line 149-150 添加信息门户账号密码
* 运行程序：
  * 参数说明：  
    可以直接运行程序：
    ```bash
    python gradesSpyder.py
    ```
    也可以添加`-m`或`--manual`参数：
    ```bash
    python gradesSpyder.py -m
    python gradesSpyder.py --manual
    ```
    说明：-m参数可以在第一次登录信息门户时不通过邮箱获得验证码，手动输入验证码并点击确定
* 邮箱登录：  
  程序通过你的`服务端邮箱`发送验证码到你的`常用邮箱`,用户手动将附件中的验证码以**邮件主题**发送给服务端邮箱（不是回复！不是回复！）来远程输入验证码。如果你无法看清本次验证码，可以随意回复邮件，等待下一次验证码邮件。也可以在第一次通过输入`-m`参数来使第一次登录时手动输入验证码。
* 成绩通知：  
  平时成绩/总评成绩会通过你的`服务端邮箱`发到你的`常用邮箱`。
* Error处理：  
  报错信息会存在本目录的log.txt文件中，也会将错误信息推送到邮件到你的`常用邮箱`。推送后，程序将自动重启继续工作，但需要再次通过邮件回复验证码登录。
## 文件结构：
* gradesSpyer.py 主程序
* geckodriver.log geckodriver产生的日志文件
* log.txt 日志文件
* finalscore.txt 记录总评成绩的本地文件
* usualscore.txt 记录平时成绩的本地文件
* time.txt 记录最近一次发送邮件的时间（勿删）
* screenshot.png 截图文件
* captchaImg.png 验证码截图文件
## 刷新频率：
* 默认5分钟刷新一次，可以在line 255 行更改，但不建议更频繁，因为学校的银杏服务器还是蛮不容易的。
* 服务端邮箱收验证码邮件的频率是2分钟一次，登录时请耐心等待。
## 其他说明：
### 关于没有采用Chrome的问题：
Chrome的驱动程序chromedriver似乎是由第三方开发的，所以在用selenium控制Chrome时页面会与人工操作有些许不同，具体到本项目则是信息门户登录时，无法显示验证码，无奈只能用Firefox
### 关于人工打码的问题：
信息门户的验证码似乎是自动生成的，但某些参数可能调得比较夸张，实测用pytesseract识别的效果很不好，所以还是采取人工打码的方式完成验证。比如，下面的验证码不是itzl，因为信息门户的验证码是5位字母。别问我是什么，我也不知道。  
![image.png](https://i.loli.net/2020/01/14/epoqmbX3EiHhuIA.png)