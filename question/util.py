from django.conf import settings

from mmwxapi.all import *


def get_third():
    return get_or_create_third(settings.THIRD_APPID,
                               settings.THIRD_APPSECRET,
                               settings.THIRD_TOKEN,
                               settings.THIRD_AESKEY)


def get_mp():
    third = get_third()
    return third.get_mp_by_appid(settings.MP_APPID)
