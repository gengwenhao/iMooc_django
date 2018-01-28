__author__ = 'gengwenhao'
__date__ = '2017/10/7 2:04'
from random import Random

from user.models import EmailVerifyRecord
from django.core.mail import send_mail
from iMooc.settings import EMAIL_FROM


# 生成验证码
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiZzKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]

    return str


# 给传入的邮箱地址发送激活连接
def send_register_email(email, send_type='register'):
    # 在数据库生成邮箱激活码记录
    email_record = EmailVerifyRecord()
    code = random_str(4 if send_type == 'update_email'else 16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    # 定义邮箱发送内容
    email_title = ''
    email_body = ''
    send_url = 'http://127.0.0.1/'

    if send_type == 'register':
        email_title = 'iMooc在线, 注册新用户, 激活链接'
        email_body = '请点击下边的连接激活你的账号: {0}active/{1}'.format(send_url, code)

        # 调用django内置的邮件发送函数
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return '已经发送邮箱, 请查看邮件激活账户'

    elif send_type == 'forget':
        email_title = 'iMooc在线, 个人账户密码, 重置链接'
        email_body = '请点击下边的连接重置你的密码: {0}reset/{1}'.format(send_url, code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'update_email':
        """
        修改邮箱
        """
        email_title = 'iMooc在线, 账户绑定新邮箱, 验证码'
        email_body = '{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
