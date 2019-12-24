from django.shortcuts import render

# Create your views here.
from lib.http import render_json
from social import logic
from user.models import User


def get_recd_list(request):
    user = request.user
    data = logic.get_recd_list(user)
    return render_json(data=data)


def like(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.like(user.id, sid)
    return render_json(data={'match': flag})


def dislike(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.dislike(user.id, sid)
    return render_json(data={'unmatch': flag})


def superlike(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.superlike(user.id, sid)
    return render_json(data={'match': flag})


def rewind(request):
    """
    每天可以反悔三次,把反悔的次数记录在redis中
    每次执行操作前,确认是否超过配置的最大反悔次数
    """
    user = request.user
    code, data = logic.rewind(user)
    return render_json(code, data)


def show_friends(request):
    user =request.user
    data = logic.show_friends(user)
    return render_json(data)


def show_friend_msg(request):
    sid = int(request.POST.get('sid'))
    data = User.objects.get(id=sid).profile.to_dict()
    return render_json(data=data)
