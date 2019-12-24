from django.utils.deprecation import MiddlewareMixin

from common import errors
from lib.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    def precess_request(self, request):
        uid = request.session.get('uid')
        if not uid:
            return render_json(code=errors.LOGIIN_REQUIRED, data='请登录')
        user = User.objects.get(id=uid)
        request.user = user