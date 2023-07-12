import random
from kavenegar import *
from Berimkharid.local_settings import kavenegarApiKey, kavenegarTemplates, kavenegarUrl
import requests


def sendKavenegar(data, type):
    url = kavenegarUrl + '?' + 'receptor=' + data['phoneNumber']
    if type == 'customerRegister':
        url = url + '&template=' + kavenegarTemplates['customerRegister'] + '&token=' + str(data['code'])
    if type == 'customerForgotPassword':
        url = url + '&template=' + kavenegarTemplates['customerForgotPassword'] + '&token=' + str(data['code'])
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response


def sendSms(data, type):
    response = sendKavenegar(data, type)
    if response.status_code == 200:
        return True
    else:
        return False

