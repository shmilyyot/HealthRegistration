from email.header import Header
from email.mime.text import MIMEText
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib
import json

#添加账户信息
def addAccount():
    accounts = [{"userId": "xxx", "password": "xxx","province":"广东省","city":"东莞市","street":"请选择","email":"xxx@hotmail.com"}
                ,{"userId": "xxx", "password": "xxx","province":"xxx","city":"xxx","street":"xxx","email":"xxx@qq.com"}
                ,{"userId": "xxx", "password": "xxx","province":"xxx","city":"xxx","street":"请选择","email":"xxx@qq.com"}]
    with open("accounts.json", mode='w') as load_f:
        json.dump(accounts, load_f, sort_keys=True, indent=2)

#加载配置文件
with open("accounts.json") as load_f:
    accounts = json.load(load_f)

#发送邮件通知
sender = "xxx@qq.com"
def sendEmailInfo(receiver):
    qqCode = 'xxx'
    smtp_server = 'smtp.qq.com'
    smtp_port = 465
    stmp = smtplib.SMTP_SSL(smtp_server, smtp_port)
    stmp.login(sender, qqCode)
    message = MIMEText('今天疫情打卡已成功', 'plain', 'utf-8')
    message['From'] = Header("Eason", 'utf-8')
    message['To'] = Header("Anyone", 'utf-8')
    message['Subject'] = Header('健康问卷打卡', 'utf-8')
    try:
        stmp.sendmail(sender, receiver, message.as_string())
        print ("通知邮件已发送")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")

#定时任务
scheduler = BlockingScheduler()

#逐个打卡
@scheduler.scheduled_job('cron',day_of_week='*', hour=9, minute='00')
def check():
    print("今日开始打卡")
    for account in accounts:
        checkProcess(account)
    print("今日打卡已完成")

#打卡过程
def checkProcess(account):
    # 打开登录窗口
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    #在linux部署时chromedriver的路径
    #driver = webdriver.Chrome(options=chrome_options, executable_path='/opt/google/chrome/chromedriver')
    driver.get("https://stuhealth.jnu.edu.cn/#/login")
    # 打开健康问卷
    driver.find_element_by_id("zh").clear()
    driver.find_element_by_id("passw").clear()
    driver.find_element_by_id("zh").send_keys(str(account['userId']))
    driver.find_element_by_id("passw").send_keys(account['password'])
    driver.find_element_by_xpath("//button[text()='登录']").click()
    sleep(1)
    if driver.current_url == "https://stuhealth.jnu.edu.cn/#/index/complete":
        print("账户" + account['userId'] + "打卡完成")
        sendEmailInfo(account['email'])
        driver.quit()
        return
    else:
        # 填写问卷
        province = driver.find_element_by_id("selectProvinceJtzz")
        sleep(1)
        Select(province).select_by_visible_text(account["province"])
        city = driver.find_element_by_id("selectCityJtzz")
        sleep(1)
        Select(city).select_by_visible_text(account["city"])
        street = driver.find_element_by_id("selectDistrictJtzz")
        sleep(1)
        Select(street).select_by_visible_text(account["street"])
        driver.find_element_by_id("10000").click()
        driver.find_element_by_id("tj").click()
        sleep(1)
        # 防止签到不成功
        if(driver.current_url == "https://stuhealth.jnu.edu.cn/#/index/complete"):
            print("账户" + account['userId'] + "打卡完成")
            sendEmailInfo(account['email'])
            driver.quit()
        else:
            checkProcess(account)

# def checkExist(account):
#     chrome_options = Options()
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--headless')
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.get("https://stuhealth.jnu.edu.cn/#/login")
#     # 打开健康问卷
#     driver.find_element_by_id("zh").clear()
#     driver.find_element_by_id("passw").clear()
#     driver.find_element_by_id("zh").send_keys(str(account['userId']))
#     driver.find_element_by_id("passw").send_keys(account['password'])
#     driver.find_element_by_xpath("//button[text()='登录']").click()
#     str = driver.current_url
#     driver.quit()
#     sleep(1)
#     if str == "https://stuhealth.jnu.edu.cn/#/index/complete":
#         return True
#     else:
#         return False

if __name__ == "__main__":
    # addAccount()
    scheduler.start()
