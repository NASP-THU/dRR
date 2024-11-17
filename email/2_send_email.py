import sys
import warnings
from collections import OrderedDict
warnings.filterwarnings('ignore')
from time import sleep
import random
import smtplib
from email.mime.text import MIMEText
from IPython.core.magic import register_cell_magic
import matplotlib.pyplot as plt ;  from matplotlib.ticker import MultipleLocator
import pickle
from datetime import datetime, timedelta
import os.path
import numpy as np
from jinja2 import Template
import time


def send_mail_to_myself(receivers, asn):
    #设置服务器所需信息
    #163邮箱服务器地址
    mail_host = 'XXX'  
    #163用户名
    mail_user = 'XXX'  
    #密码(部分邮箱为授权码) 
    mail_pass = '*******'   
    #邮件发送方邮箱地址
    sender = 'XXX'  

    #设置email信息
    #邮件内容设置
#     message = MIMEText(format_text_html(asn)[1],'plain','utf-8')
    message = MIMEText(format_text_html(asn)[1],'html')
    #邮件主题       
    message['Subject'] = format_text_html(asn)[0]
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = receivers[0]  
    
#     print(format_text_html(asn)[0])
#     print(format_text_html(asn)[1])
    
    #登录并发送邮件
    try:
#         smtpObj = smtplib.SMTP(mail_host,465) 
#         smtpObj.startttls()
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('email sent done.',receivers[0], asn)
    except smtplib.SMTPException as e:
        print('error', receivers[0], asn) #打印错误

def format_text_html(asn):
    subject = "RPKI Deployment Survey"
    text = """
    <html>
    <body>
    <p>Dear administrator:</p>
    <p>We are researchers in the Future Network Laboratory of Tsinghua University, and closely collaborate with CERNET (China Education and Research Network). We are currently responding to the IETF's call and conducting research on the deployment of RPKI (Resource Public Key Infrastructure). We have noticed that your %s has deployed ROA.</p>
    <p>We sincerely invite you to participate in this survey, which only takes a few minutes. Your feedback is important for helping researchers understand the concerns in the deployment of RPKI.</p>
    <p><a href="https://forms.gle/5aAxDH3CbjWRaZgM9">You can click here to fill out the questionnaire</a>. Or you can reply via email (The following is a copy of the questionnaire). Your responses will be kept confidential and only used for research purposes.</p>
    <p>Thank you for taking the time to complete this survey. Your feedback is greatly appreciated.</p>
    <p>Sincerely,<br>Sumuro</p>
    <p><br>Copy of the questionnaire:</p>
    <p>(1) Which RPKI ROA deployment mode does your organization use?</p>
    <ul>
      <li>Delegated RPKI. A more secure mode that allows you to sign the RPKI objects yourself and then publish them in the certificate repository that you operate.</li>
      <li>Hosted RPKI. A more convenient mode that that RIR will help you sign RPKI objects, and all certificates, keys, and signed RPKI objects will be published in RIR's repository.</li>
      <li>I'm not sure.</li>
    </ul>
    <p>(2) If you are currently using the hosted model, will you choose to use a more secure delegated mode in the future?</p>
    <ul>
      <li>Yes.</li>
      <li>No.</li>
      <li>Skip this question (We already use delegated mode).</li>
    </ul>
    <p>(3) Has your AS deployed ROV (Use RPKI certificates to verify all BGP advertisements you receive)?</p>
    <ul>
      <li>Yes.</li>
      <li>No.</li>
      <li>I'm not sure.</li>
    </ul>
    <p>(4) If no for the previous question, what are the reasons for not deploying ROV? (multi-selection)</p>
    <ul>
      <li>Lack of awareness or understanding of RPKI ROV.</li>
      <li>Have doubts about the authenticity and integrity of RPKI certificates.</li>
      <li>Worried that RPKI may not accurately verify the legitimacy of BGP advertisements.</li>
      <li>Other reasons (please specify).</li>
      <li>Skip this question (We have deployed ROV).</li>
    </ul>
    <p>(5) Since RPKI is a PKI-based facility, are you concerned about RPKI authorities maliciously or forcibly compromising your certificates, which could affect the legitimacy of your BGP advertisements?</p>
    <ul>
      <li>Yes.</li>
      <li>No.</li>
      <li>I'm not sure.</li>
    </ul>
    <p>(6) Any additional comments or feedback on RPKI and its deployment?</p>
    </body>
    </html>
    """
    text = text % (asn)
    return subject, text



# send_mail_to_myself(receivers, "6666")
#email_to_all_ASNs_w_ROA-top-10
#email_to_all_ASNs_w_ROA-top-1-10000.csv
with open("C:\\Users\\sumuro\\Desktop\\dRR\\邮件\\email_to_all_ASNs_w_ROA-top-1-10000.csv") as f:
    for line in f:
        email = line.split(",")[0]
        asn = line.split(",")[1]
        receivers = [email]
#         print(receivers)
#         print(asn)
        send_mail_to_myself(receivers, asn)
        time.sleep(3)
        