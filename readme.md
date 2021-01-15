# 今天出成绩了吗 | UESTC成绩监控脚本
> 花了三天时间写了个脚本，可以挂在服务器/自己电脑上随时监控成绩变化,变化时会有邮件提醒  
> 暂时还有很多不足，欢迎提issue/PR

## 脚本环境：
* `Python 3` 以上版本，[点击下载](https://www.python.org/)
* pip
* `Selenium 2.0` 以上版本
* `Pillow`库
* GUI环境
* `firefox 浏览器` [点击下载](http://www.firefox.com.cn/) | [为什么不用Chrome](#关于没有采用Chrome的问题)
* `geckodriver`：用于selenium控制firefox的程序，[点击下载](https://github.com/mozilla/geckodriver/releases)
## 准备工作：
* 你的一个邮箱作为发送信息的`服务端邮箱`
* 你的一个`常用邮箱`
* 一台GUI服务器/不关机的电脑
## 使用步骤：
* 安装Python
* 安装Selenium:
    ```bash
    pip install selenium
    ```
* 安装Pillow:
    ```bash
    pip install Pillow
    ```
* 配置个人信息：
  * 打开 gradesSpyer.py
  * line 24-28 添加邮箱信息  
    * line 25 邮箱授权码是你在第三方客户端使用的密码，不是网页登录使用的密码。如果没有使用过，可能要去邮箱网页端开启授权码功能。
  * line 161-162 添加信息门户账号密码
* 配置 `geckodriver`：
  * 将`geckodriver`或`geckodriver.exe`(Windows)文件放在文件目录下
  * Windows环境需要将line 316`./geckodriver`改为`./geckodriver.exe`
* 运行程序：
  * 参数说明：  
    可以直接运行程序：
    ```bash
    python gradesSpyder.py
    ```
* 邮箱登录：  
  程序通过你的`服务端邮箱`发送登录失效，需要手动登录到你的`常用邮箱`,用户收到邮件后应该手动登录信息门户。因为最近升级为滑块验证码，破解成本较大，故采用手动登录方式。
* 成绩通知：  
  平时成绩/总评成绩会通过你的`服务端邮箱`发到你的`常用邮箱`。
* 退出程序：
  请使用`ctrl`/`⌃` `+ c`退出程序。
* Error处理：  
  报错信息会存在本目录的log.txt文件中，也会将错误信息推送到邮件到你的`常用邮箱`。推送后，程序将自动重启继续工作，但需要再次通过邮件回复验证码登录。
## 已知问题：
* 在非2k屏上运行的时候四个长度应该删除line 155 `* 2`(也有可能是macOS的锅，暂未测试，欢迎反馈)
* 在windows平台使用时可能会有不能重启成功的问题，最近比较忙可能短期不会修复。推荐在GUI的Linux/macOS下运行。也欢迎提PR
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
* 默认5分钟刷新一次，可以在line 270 更改，但不建议更频繁，因为学校的银杏服务器还是蛮不容易的。
* 服务端邮箱收验证码邮件的频率是2分钟一次，登录时请耐心等待。
## Q&A：
### 关于没有采用Chrome的问题：
Chrome的驱动程序chromedriver似乎是由第三方开发的，所以在用selenium控制Chrome时页面会与人工操作有些许不同，具体到本项目则是信息门户登录时，无法显示验证码，无奈只能用Firefox。

Copyright &copy; 2020-2021 Saafo. All Rights Reserved.
