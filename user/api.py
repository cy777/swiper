from django.core.cache import cache
from django.shortcuts import render
from django.http import JsonResponse

from common import errors, keys
from lib.http import render_json
from lib.sms import send_sms
from user.models import User


def submit_phone(request):
    '''提交手机号码, 发送验证码'''
    phone = request.POST.get('phone')
    #发送验证码
    status, msg = send_sms(phone)
    if not status:
        return render_json(code=errors.SMS_ERROR, data='短信发送失败')
    return render_json()


def submit_vcode(request):
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')

    #从缓存中取出数据
    cached_vcode = cache.get(keys.VCODE_KEY % phone)
    if vcode == cached_vcode:
        user, _ = User.objects.get_or_create(phonenum=phone, defaults={'nickname': phone})
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        return render_json(code=errors.VCODE_ERROR, data='验证码错误')


def get_profile(request):
    uid = request.session.get('uid')
    if not uid:
        return render_json(code=errors.LOGIIN_REQUIRED, data='请登录')
    user = User.objects.get(id=uid)
    return render_json(data=user.profile.to_dict())