# 今天出成绩了吗 | UESTC成绩监控脚本
> 花了三天时间写了个脚本，可以挂在服务器/自己电脑上随时监控成绩变化,变化时会有邮件提醒  
> 暂时还有很多不足，欢迎提issue/PR

## 脚本环境：
* `Python 3` 以上版本，[点击下载](https://www.python.org/)
* pip
* `Selenium 2.0` 以上版本
* GUI环境
* `firefox 浏览器` [点击下载](http://www.firefox.com.cn/) | [为什么不用Chrome](#关于没有采用Chrome的问题)
* `geckodriver`：用于selenium控制firefox的程序，[点击下载](https://github.com/mozilla/geckodriver/releases)
## 准备工作：
* 你的一个**很少接收邮件的邮箱**作为发送信息的`服务端邮箱`
* 你的一个`常用邮箱`
* 一台GUI服务器/不关机的电脑
## 使用步骤：
* 安装Python
* 安装Selenium:
    ```bash
    pip install selenium
    ```
* 配置个人信息：
  * 打开 gradesSpyer.py
  * line 24-28 添加邮箱信息  
    * 服务端邮箱请**一定**要添加**很少**收到邮件的邮箱
    * line 25 邮箱授权码是你在第三方客户端使用的密码，不是网页登录使用的密码。如果没有使用过，可能要去邮箱网页端开启授权码功能。
  * line 153-154 添加信息门户账号密码
* 配置 `geckodriver`：
  * 将`geckodriver`或`geckodriver.exe`(Windows)文件放在文件目录下
  * Windows环境需要将line 307`./geckodriver`改为`./geckodriver.exe`
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
* 退出程序：
  请使用`ctrl`/`⌃` `+ c`退出程序。
* Error处理：  
  报错信息会存在本目录的log.txt文件中，也会将错误信息推送到邮件到你的`常用邮箱`。推送后，程序将自动重启继续工作，但需要再次通过邮件回复验证码登录。
## 已知问题：
* 在1920*1080屏上运行的时候四个长度应该删除line 147 `* 2`
* 目前信息门户登录页面出现了一些问题，在windows平台使用时可能会造成截取不到验证码的问题。等待信息门户恢复正常后会想办法修复。
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
* 默认5分钟刷新一次，可以在line 261 更改，但不建议更频繁，因为学校的银杏服务器还是蛮不容易的。
* 服务端邮箱收验证码邮件的频率是2分钟一次，登录时请耐心等待。
## Q&A：
### 关于没有采用Chrome的问题：
Chrome的驱动程序chromedriver似乎是由第三方开发的，所以在用selenium控制Chrome时页面会与人工操作有些许不同，具体到本项目则是信息门户登录时，无法显示验证码，无奈只能用Firefox。
### 关于为什么服务端邮箱需要非常用邮箱：
服务端在收取邮件的时候只会收取最近5条，收取太多程序效率会很低。如果验证码不出现在最近5条邮件，则会无法读取验证码。
### 关于为什么验证码邮件没有把验证码嵌入正文：
尝试过将附件嵌入正文和将验证码上传图床，正文放html标签，但发送时网易服务器会报错`554,b'TD:SPM`将邮件认为是垃圾邮件而不予发送。无奈只有将验证码作为附件发送。
### 关于人工打码的问题：
信息门户的验证码似乎是自动生成的，但某些参数可能调得比较夸张，实测用pytesseract识别的效果很不好，所以还是采取人工打码的方式完成验证。  
比如，下面的验证码不是itzl，因为信息门户的验证码是5位字母。别问我是什么，我也不知道。  
![image.png](https://i.loli.net/2020/01/14/epoqmbX3EiHhuIA.png)

Copyright &copy; 2020 Saafo. All Rights Reserved.
