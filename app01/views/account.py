from io import BytesIO

from django.shortcuts import render, redirect, HttpResponse
from django import forms

from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.code import check_code
from app01.utils.encrypt import md5


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,

    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login(request):
    '''登陆'''
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():

        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', '')
        if code.upper() != user_input_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})



        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        #用户名和密码错误，返回的是None
        if not admin_object:
            form.add_error('password', "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        #用户名和密码错误
        #网站生成随机字符串；写到用户浏览器的cookie中，在写入到session中
        request.session['info'] = {'id':admin_object.id, 'name': admin_object.username}
        return redirect('/admin/list')
    return render(request, 'login.html', {'form': form})


def image_code(request):
    '''生成图片验证码'''

    #调用pillow函数，生成图片
    img, code_string = check_code()

    #x写入到自己的session中，（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    #给session设置7天免登陆
    request.session.set_expiry(60 * 60 * 24 * 7)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    '''注销'''
    request.session.clear()
    return redirect('/logout/')