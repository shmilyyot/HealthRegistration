from email.header import Header
from email.mime.text import MIMEText
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib
import json
import requests
import json
import base64
from Crypto.Cipher import AES
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives import padding

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

class daka:
    headers = {"accept": "application/json, text/plain, */*",
               "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
               "content-type": "application/json",
               "sec-fetch-dest": "empty",
               "sec-fetch-mode": "cors",
               "sec-fetch-site": "same-origin",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55"}
    sucess = "登录成功，今天已填写"

    def __init__(self, account, password):
        super().__init__()
        self.account = account
        self.password = password
        self.body = {"username": account,
                     "password": self.jiami(password)}
        self.body = json.dumps(self.body)

    def pkcs7_padding(self, data):
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data.encode('utf-8'))+padder.finalize()
        return padded_data

    # 将密码转为加密后的代码
    def jiami(self, data):
        key = 'xAt9Ye&SouxCJziN'.encode('utf-8')
        cryptor = AES.new(key, AES.MODE_CBC, key)
        res = base64.b64encode(cryptor.encrypt(self.pkcs7_padding(
            data))).decode().replace('/', '_').replace('+', '-')
        res = list(res)
        res[-2] = "*"
        res = "".join(res)
        return res

    # 登入
    def login(self):
        url = "https://stuhealth.jnu.edu.cn/api/user/login"#登入的网址
        res_login = requests.post(
            url, data=self.body, headers=self.headers)
        res_login_data = json.loads(res_login.text)
        print(res_login_data)
        self.res_login_data = res_login_data

    # 获取打卡需要的相关信息
    def get_info_data(self):
        res_login_data = self.res_login_data
        get_info_data = {}
        get_info_data['jnuid'] = res_login_data['data']['jnuid']
        get_info_data['idType'] = '2'
        # print(get_info_data)
        get_info_data = json.dumps(get_info_data)
        info_url = "https://stuhealth.jnu.edu.cn/api/user/stuinfo"#获取信息的网址
        res_info_data = requests.post(
            info_url, data=str(get_info_data).encode('utf-8'), headers=self.headers)
        res_info_data = json.loads(res_info_data.text)
        self.res_info_data = res_info_data
        # print(res_info_data)

    def post(self):
        res_info_data = self.res_info_data
        daka_post_url = "https://stuhealth.jnu.edu.cn/api/write/main"#post的网址
        post_data = {}
        post_data['mainTable'] = {}
        post_data['mainTable']['leaveTransportationOther'] = res_info_data['data']['mainTable']['leaveTransportationOther']
        post_data['mainTable']['way2Start'] = res_info_data['data']['mainTable']['way2Start']
        post_data['mainTable']['language'] = res_info_data['data']['mainTable']['language']
        post_data['mainTable']['declareTime'] = res_info_data['data']['declare_time']
        post_data['mainTable']['personNo'] = res_info_data['data']['jnuId']
        post_data['mainTable']['personName'] = res_info_data['data']['xm']
        post_data['mainTable']['sex'] = res_info_data['data']['xbm']
        post_data['mainTable']['professionName'] = res_info_data['data']['zy']
        post_data['mainTable']['collegeName'] = res_info_data['data']['yxsmc']
        post_data['mainTable']['phoneArea'] = res_info_data['data']['mainTable']['phoneArea']
        post_data['mainTable']['phone'] = res_info_data['data']['mainTable']['phone']
        post_data['mainTable']['assistantName'] = res_info_data['data']['mainTable']['assistantName']
        post_data['mainTable']['assistantNo'] = res_info_data['data']['mainTable']['assistantNo']
        post_data['mainTable']['className'] = res_info_data['data']['mainTable']['className']
        post_data['mainTable']['linkman'] = res_info_data['data']['mainTable']['linkman']
        post_data['mainTable']['linkmanPhoneArea'] = res_info_data['data']['mainTable']['linkmanPhoneArea']
        post_data['mainTable']['linkmanPhone'] = res_info_data['data']['mainTable']['linkmanPhone']
        post_data['mainTable']['personHealth'] = res_info_data['data']['mainTable']['personHealth']
        post_data['mainTable']['temperature'] = res_info_data['data']['mainTable']['temperature']
        post_data['mainTable']['personHealth2'] = res_info_data['data']['mainTable']['personHealth2']
        post_data['mainTable']['schoolC1'] = res_info_data['data']['mainTable']['schoolC1']
        post_data['mainTable']['currentArea'] = res_info_data['data']['mainTable']['currentArea']
        post_data['mainTable']['personC4'] = res_info_data['data']['mainTable']['personC4']
        post_data['mainTable']['otherC4'] = res_info_data['data']['mainTable']['otherC4']
        post_data['mainTable']['isPass14C1'] = res_info_data['data']['mainTable']['isPass14C1']
        post_data['mainTable']['isPass14C2'] = res_info_data['data']['mainTable']['isPass14C2']
        post_data['mainTable']['isPass14C3'] = res_info_data['data']['mainTable']['isPass14C3']
        post_data['secondTable'] = {}
        post_data['secondTable']['other1'] = res_info_data['data']['secondTable']['other1']
        post_data['secondTable']['other3'] = res_info_data['data']['secondTable']['other3']
        post_data['secondTable']['other4'] = res_info_data['data']['secondTable']['other4']
        post_data['secondTable']['other5'] = res_info_data['data']['secondTable']['other5']
        post_data['secondTable']['other6'] = res_info_data['data']['secondTable']['other6']
        post_data['secondTable']['other7'] = res_info_data['data']['secondTable']['other7']
        #以下四项表单内容是修改内容，原问卷没有填写疫苗接种信息
        post_data['secondTable']['other10'] = res_info_data['data']['secondTable']['other10']
        post_data['secondTable']['other11'] = res_info_data['data']['secondTable']['other11']
        post_data['secondTable']['other12'] = res_info_data['data']['secondTable']['other12']
        post_data['secondTable']['other13'] = res_info_data['data']['secondTable']['other13']
        post_data['jnuid'] = self.res_login_data['data']['jnuid']
        post_data_res = requests.post(
            daka_post_url, data=json.dumps(post_data), headers=self.headers)
        print(post_data_res.text)
        self.post_data_res = json.loads(post_data_res.text)
        
    #检查是否打卡成功
    def yanzhen(self):
        self.login()
        if(self.res_login_data['meta']['msg'] == self.sucess):
            print(self.res_login_data['data']['name']+'>>>>'+self.sucess)
            return True
        return False

    def run(self):
        self.login()
        self.get_info_data()
        self.post()

#定时任务
scheduler = BlockingScheduler()
#逐个打卡
@scheduler.scheduled_job('cron',day_of_week='*', hour=8, minute='00')
def check():
    print("今日开始打卡")
    for account in accounts:
        obj = daka(account['userId'], account['password'])
        obj.run()
        obj.yanzhen()
        sendEmailInfo(account['email'])
    print("今日打卡已完成")
    
if __name__ == '__main__':
    scheduler.start()
