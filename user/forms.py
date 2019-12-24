from django.forms import ModelForm
from django.forms import ValidationError

from user.models import Profile


class ProfileModelForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    # django校验按创建的models顺序从上至下校验
    # 上面字段校验完了才会从前端传过来的forms表单取下一个数据
    # 所以这里应该校验后面的字段,不能校验min_distance
    # 如果校验hmin_distance,max_distanc会拿不到
    def clean_max_distance(self):
        data = self.clean()
        min_distance = data['min_distance']
        max_distance = data['max_distance']
        if min_distance >= max_distance:
            raise ValidationError('min_distance is greater then max_distance')
        return max_distance

    def clean_max_dating_age(self):
        data = self.clean()
        min_dating_age = data['min_dating_age']
        max_dating_age = data['max_dating_age']
        if min_dating_age >= max_dating_age:
            raise ValidationError('min_dating_age is greater then max_dating_age')
        return max_dating_age