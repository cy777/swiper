import datetime

from django.db import models
from django.core.cache import cache

from common import keys
from lib.mixins import ModelMixin


class User(models.Model):
    SEX = (
        ('female', 'female'),
        ('male', 'male')
    )
    phonenum = models.CharField(max_length=32, verbose_name='手机号', unique=True)
    nickname = models.CharField(max_length=128, verbose_name='昵称', unique=True)
    sex = models.CharField(max_length=8, choices=SEX, verbose_name='性别')
    birth_year = models.IntegerField(default=2000, verbose_name='出生年')
    birth_month = models.IntegerField(default=1, verbose_name='出生月')
    birth_day = models.IntegerField(default=1, verbose_name='出生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象')
    location = models.CharField(max_length=128, verbose_name='常居地')

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f'<user {self.nickname}>'

    @property
    def age(self):
        birthday = datetime.datetime(year=self.birth_year, month=self.birth_month,
                                     day=self.birth_day)
        now = datetime.datetime.now()
        return (now - birthday).days // 365

    @property
    def profile(self):
        key = keys.PROFILE_KEY % self.id
        profile = cache.get(key)
        if not profile:
            profile, _ = Profile.objects.get_or_create(id=self.id)
            cache.set(key, profile, timeout=86400 * 14)
        return profile

    def to_dict(self):
        return {
            'id': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'sex': self.sex,
            'avatar': self.avatar,
            'location': self.location,
            'age': self.age
        }


class Profile(models.Model, ModelMixin):
    SEX = (
        ('female', 'female'),
        ('male', 'male')
    )
    location = models.CharField(max_length=128, verbose_name='目标城市')
    min_distance = models.IntegerField(default=0, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=100, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    dating_sex = models.CharField(max_length=8, choices=SEX, default='female', verbose_name='匹配的性别')
    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matche = models.BooleanField(default=True, verbose_name='不让为匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    class Meta:
        db_table = 'profile'
