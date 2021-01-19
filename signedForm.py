from email.header import Header
from email.mime.text import MIMEText
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib
import json

# #添加账户信息
# def addAccount():
#     accounts = [{"userId": "xxx", "password": "xxx","province":"广东省","city":"东莞市","street":"请选择","email":"xxx@hotmail.com"}]
#     with open("accounts.json", mode='w') as load_f:
#         json.dump(accounts, load_f, sort_keys=True, indent=2)
# addAccount()

#加载配置文件
with open("accounts.json") as load_f:
    accounts = json.load(load_f)

#发送邮件通知
sender = "xxx@qq.com"
def sendEmailInfo(receiver):
    qqCode = 'opabkobjzcaobfje'  # 授权码（这个要填自己获取到的）
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
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")

#定时任务
scheduler = BlockingScheduler()

#签到
@scheduler.scheduled_job('cron',day_of_week='*', hour=9, minute='00')
def checkIn():
    print("开始登记")
    for account in accounts:
        # 打开登录窗口
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://stuhealth.jnu.edu.cn/#/login")
        # 打开健康问卷
        driver.find_element_by_id("zh").clear()
        driver.find_element_by_id("passw").clear()
        driver.find_element_by_id("zh").send_keys(str(account['userId']))
        driver.find_element_by_id("passw").send_keys(account['password'])
        driver.find_element_by_xpath("//button[text()='登录']").click()
        sleep(1)
        if driver.current_url == "https://stuhealth.jnu.edu.cn/#/index/complete":
            print("登记完成")
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
            driver.quit()
            #防止签到不成功,重新检查签到
            checkIn()

if __name__ == "__main__":
    scheduler.start()
