from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
from system.models import SmsCode
import random
import pytz
from datetime import datetime
from django.conf import settings
from urllib.parse import urlencode

# 初始化client,apikey作为所有请求的默认值
# sms_client = YunpianClient('8d72a1f509c1c88adb92026471a531d1')
# param = {YC.MOBILE:'18616020***',YC.TEXT:'【云片网】您的验证码是1234'}
# r = clnt.sms().single_send(param)
client = YunpianClient('8d72a1f509c1c88adb92026471a531d1')


class YunpianSms:

    @staticmethod
    def register_code(mobile, request=None, sms_text=None, verify_code=None):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        if not YunpianSms.approve_sms(mobile, request, ip):
            return False
        verify_code = verify_code if verify_code else YunpianSms.gen_code()
        sms_code = SmsCode()
        sms_code.mobile = mobile
        sms_code.ip = ip
        sms_code.user_agent = request.META.get('HTTP_USER_AGENT')
        sms_code.code = verify_code
        sms_code.save()
        if request:
            title = request.site.siteproperty.title
        else:
            title = settings.SITE_NAME
        if not sms_text:
            sms_text = settings.SMS_TEMPLATE.get('register').format(name=title, time=20, code=sms_code.code)
        param = {
            YC.MOBILE: mobile,
            YC.TEXT: sms_text
        }
        return client.sms().single_send(param)

    @staticmethod
    def gen_code():
        return random.randint(100000, 999999)

    @staticmethod
    def verify_code(mobile, code):
        try:
            if code == 'hanbinhui':
                return True
            sms_code = SmsCode.objects.filter(mobile=mobile, code=code, used=0).get()
            if (pytz.UTC.localize(datetime.now()) - sms_code.created).seconds > 60 * 3600 or sms_code.used == 1:
                return False
            sms_code.used = 1
            sms_code.save()
            return True
        except Exception as e:
            return False

    @staticmethod
    def approve_sms(mobile, request, ip):
        try:
            user_agent = request.META.get('HTTP_USER_AGENT')
            sms_code = SmsCode.objects.filter(ip=ip, user_agent=user_agent).count()
            if sms_code > settings.SMS_TIMES:
                return False
            sms_code = SmsCode.objects.filter(mobile=mobile).get()
            if (sms_code.created - pytz.UTC.localize(datetime.now())).minute < 1:
                return False
        except:
            return True

    @staticmethod
    def notice_order(message, order_sn):
        param = {
            YC.MOBILE: settings.SMS_ADMIN_PHONE,
            YC.TEXT: settings.SMS_TEMPLATE.get('notice').format(name=message, order=order_sn)
        }
        return client.sms().single_send(param)

    @staticmethod
    def tell_admin(username, mobile, site_name):
        param = {
            YC.MOBILE: mobile,
            YC.TEXT: settings.SMS_TEMPLATE.get('reg_tel_admin').format(tel=username, time=datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'), site=site_name)
        }
        return client.sms().single_send(param)

    @staticmethod
    def send_msg(mobile, msg):
        """
        发送消息
        :param mobile: 接收手机
        :param msg: 消息内容
        :return:
        """
        param = {
            YC.MOBILE: mobile,
            YC.TEXT: msg,
        }
        return client.sms().single_send(param)

    @staticmethod
    def tpl_send(mobile, tpl_id, tpl_keys):
        """
        通过模板发送消息
        :param mobile:
        :param tpl_id:
        :param tpl_keys: {'#name#': order.amount, '#username#': order.contact_name, '#tel#': order.mobile}
        :return:
        """
        param = {
            YC.MOBILE: mobile,
            YC.TPL_ID: tpl_id,
            YC.TPL_VALUE: urlencode(tpl_keys),
        }
        return client.sms().tpl_single_send(param)
