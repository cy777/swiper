import os

from django.conf import settings

from common import keys
from lib.qiniu import upload_qiniu
from swiper import config
from worker import celery_app


@celery_app.task
def handle_upload(user, avatar):
    file_name = keys.AVATAR_KEY % user.id
    file_path = os.path.join(settings.BASE_DIR, settings.MEIDAS, file_name)
    with open(file_path, mode='wb') as fp:
        for chunk in avatar.chunks():
            fp.write(chunk)

    upload_qiniu(user, file_path)
    user.avatar = config.QN_URL + file_name
    user.save()
