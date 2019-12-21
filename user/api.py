from django.core.cache import cache
from django.shortcuts import render
from django.http import JsonResponse

from common import errors, keys
from lib.http import render_json
from lib.sms import send_sms
from user.forms import ProfileModelForm
from user.logic import handle_upload
from user.models import User


def submit_phone(request):
    """提交手机号码, 发送验证码"""
    phone = request.POST.get('phone')
    # 发送验证码
    send_sms.delay(phone)
    return render_json()


def submit_vcode(request):
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')

    # 从缓存中取出数据
    cached_vcode = cache.get(keys.VCODE_KEY % phone)
    if vcode == cached_vcode:
        user, _ = User.objects.get_or_create(phonenum=phone, defaults={'nickname': phone})
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        return render_json(code=errors.VCODE_ERROR, data='验证码错误')


def get_profile(request):
    return render_json(data=request.user.profile.to_dict())


def edit_profile(request):
    form = ProfileModelForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False)
        uid = request.user.id
        profile.id = uid
        profile.save()
        return render_json(data=profile.to_dict())
    return render_json(code=errors.PROFILE_ERROR, data=form.errors)


def upload_aavatar(request):
    avatar = request.FIles.get('avatar')
    user = request.user
    handle_upload.delay(user, avatar)
    return render_json()
