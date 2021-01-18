from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from apscheduler.schedulers.blocking import BlockingScheduler
import json

# #添加账户信息
# def addAccount():
#     accounts = [{"userId": "202034261024", "password": "Lovecs456","province":"广东省","city":"东莞市","street":"请选择"}]
#     with open("accounts.json", mode='w') as load_f:
#         json.dump(accounts, load_f, sort_keys=True, indent=2)
# addAccount()

#加载配置文件
with open("accounts.json") as load_f:
    accounts = json.load(load_f)

#发送邮件通知
def sendEmailInfo():
    pass

#签到
def checkIn():
    for account in accounts:
        # 打开登录窗口
        chrome_options = Options()
        # 设置chrome浏览器无界面模式
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
        if driver.current_url =="https://stuhealth.jnu.edu.cn/#/index/complete":
            print("登记完成")
            sendEmailInfo()
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
    scheduler = BlockingScheduler()
    scheduler.add_job(checkIn(), 'cron', day_of_week='1-7', hour=22, minute=18)
    scheduler.start()
