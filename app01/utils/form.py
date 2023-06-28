from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5


class User(BootStrapModelForm):
    name = forms.CharField(
        min_length=3,
        label="姓名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']


class NumberAddForm(BootStrapModelForm):
    number = forms.CharField(
        label='卡号',
        validators=[RegexValidator(r'^0\d{5}$', '卡号格式错误,必须是0开头的6位数字')]
    )

    class Meta:
        model = models.Number
        fields = ['number', 'price', 'level', 'status']

    def clean_number(self):
        txt_number = self.cleaned_data['number']
        exists = models.Number.objects.filter(number=txt_number).exists()
        if exists:
            raise ValidationError('卡号已存在')
        return txt_number


class NumberEditForm(BootStrapModelForm):
    number = forms.CharField(
        label='卡号',
        validators=[RegexValidator(r'^0\d{5}$', '卡号格式错误,必须是0开头的6位数字')]
    )

    class Meta:
        model = models.Number
        fields = ['number', 'price', 'level', 'status']

    def clean_number(self):
        txt_number = self.cleaned_data['number']
        exists = models.Number.objects.exclude(id=self.instance.pk).filter(number=txt_number).exists()
        if exists:
            raise ValidationError('卡号已存在')
        return txt_number


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd =self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd =self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        #去数据库校验当前密码和新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError('密码不能与之前的一致')
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm

