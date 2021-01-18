from time import sleep
from selenium import webdriver
import json

# accounts = [{"userId":"202034261024","password":"Lovecs456","address":"南城区鸿福西路沙池大厦B504"}]
# with open("accounts.json",mode='a') as load_f:
#     json.dump(accounts,load_f,sort_keys=True, indent=2)
#加载配置文件
with open("accounts.json") as load_f:
    accounts = json.load(load_f)
for account in accounts:
    # 打开登录窗口
    driver = webdriver.Chrome()
    driver.get("https://stuhealth.jnu.edu.cn/#/login")
    sleep(1)
    # 打开健康问卷
    driver.find_element_by_id("zh").clear()
    driver.find_element_by_id("passw").clear()
    driver.find_element_by_id("zh").send_keys(str(account['userId']))
    driver.find_element_by_id("passw").send_keys(account['password'])
    driver.find_element_by_xpath("//button[text()='登录']").click()
    # 填写问卷
    driver.find_element_by_id("jtxxdz").clear()
    driver.find_element_by_id("jtxxdz").send_keys(account['address'])

