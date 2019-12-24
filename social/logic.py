import datetime

from django.core.cache import cache
from django.db.models import Q

from common import keys, errors
from social.models import Swiped, Friend
from swiper import config
from user.models import User


def get_recd_list(user):
    now = datetime.datetime.now()
    max_brith_year = now.year - user.profile.min_dating_age
    min_birth_year = now.year - user.profile.max_dating_age
    swiped_list = Swiped.objects.filter(uid=user.id).only('sid')
    sid_list = [s.sid for s in swiped_list]
    sid_list.append(user.id)
    users = User.objects.filter(location=user.profile.location,
                                birth_year__range=[max_brith_year, min_birth_year],
                                sex=user.profile.dating_sex).exclude(id__in=sid_list)[:20]
    data = [user.to_dict() for user in users]
    return data


def like(uid, sid):
    Swiped.like(uid=uid, sid=sid)
    if Swiped.has_like(uid=uid, sid=sid).exists():
        Friend.make_friends(uid1=uid, uid2=sid)
        return True
    return False


def dislike(uid, sid):
    Swiped.dislike(uid=uid, sid=sid)
    Friend.delete_friend(uid, sid)
    return True


def superlike(uid, sid):
    Swiped.like(uid=uid, sid=sid)
    if Swiped.has_like(uid=uid, sid=sid).exists():
        Friend.make_friends(uid1=uid, uid2=sid)
        return True
    return False


def rewind(user):
    key = keys.REWIND_KEY % user.id
    cached_rewinded_times = cache.get()
    if cached_rewinded_times < config.MAX_REWIND:
        cached_rewinded_times += 1
        now = datetime.datetime.now()
        left_seconds = 86400 - now.hour * 3600 - now.minute * 60 - now.second
        cache.set(cached_rewinded_times, timeout=left_seconds)

        try:
            record = Swiped.objects.filter(uid=user.id).latest('time')
            Friend.delete_friend(uid1=user.id, uid2=record.sid)
            record.delete()
            return 0, None
        except Swiped.DoesNotExist:
            return errors.NO_RECORD, '无操作记录,无法反悔'

    else:
        return errors.EXCEED_MAXIMUN_REWIND, '超过最大反悔次数'


def show_friends(user):
    friends = Friend.objects.filter(Q(uid1=user.id) | Q(uid2=user.id))
    friends_id = []
    for friend in friends:
        if friend.uid1 == user.id:
            friends_id.append(friend.uid2)
        else:
            friends_id.append(friend.uid1)
    users = User.objects.filter(id__in=friends_id)
    data = [user.to_dict() for user in users]
    return data