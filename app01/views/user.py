from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import User


def user_list(request):
    '''用户管理'''
    queryset = models.UserInfo.objects.all()
    page_object = Pagination(request, queryset, page_size=2)
    context = {
        'queryset': page_object.page_queryset, #分完页数据
        'page_string': page_object.html(), #生成页码
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    '''添加用户'''
    if request.method == 'GET':
        form = User()
        return render(request, 'user_add.html', {'form': form})

    # 用户post提交数据，数据校验
    form = User(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_add.html', {'form': form})


def user_edit(request, nid):
    '''编辑用户'''
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = User(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = User(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')

