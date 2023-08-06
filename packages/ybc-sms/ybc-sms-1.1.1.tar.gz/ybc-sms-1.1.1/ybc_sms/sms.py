from ybc_commons.ArgumentChecker import Checker
from ybc_commons.ArgumentChecker import Argument
from ybc_commons import httpclient
from ybc_commons.context import check_arguments
from ybc_commons.util.predicates import non_blank
from ybc_exception import exception_handler
_SMS_URL = 'send-sms'


@exception_handler('ybc_sms')
@check_arguments({'content': non_blank})
def send(phone: (int, str), content: str = '我正在为我的Python程序debug，抱歉打扰到你啦。'):
    """
    发送短信到指定的手机号码

    :param phone: 手机号码，11位数字(int或str类型,必填) 例如:12345678900,'12345678900'
    :param content: 短信内容(文本类型,非必填) 例如:'我正在为我的Python程序debug，抱歉打扰到你啦。'
    :return: 无
    """
    Checker.check_arguments([
        Argument('ybc_sms', 'send', 'phone', phone, (int, str), None),
        Argument('ybc_sms', 'send', 'content', content, str, non_blank)
    ])

    try:
        phone = int(phone)
    except ValueError:
        phone = 0

    data = {'phone': phone, 'content': content}
    res = httpclient.post(_SMS_URL, data)
    print(res['data'])
    return
