from flask_mail import Message

from logapp.main.fk import mail,app
from logapp.fk_tools import mail_content_tool

msg = Message('test subject',sender='betalun@163.com',recipients=['betalun@qq.com'])
# 这里需要实现文件配置
msg_content = mail_content_tool.build_mail_content('My Title','My Content')
msg.html = msg_content

with app.app_context():
    mail.send(msg)
    print('====邮件发送成功====')