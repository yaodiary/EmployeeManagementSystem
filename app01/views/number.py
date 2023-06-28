from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import NumberAddForm, NumberEditForm


def number_list(request):
    '''卡号列表'''
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict["number__contains"] = search_data

    queryset = models.Number.objects.filter(**data_dict).order_by('level')
    page_object = Pagination(request, queryset, page_size=15)

    context = {
        'search_data': search_data,
        'queryset': page_object.page_queryset, #分完页数据
        'page_string': page_object.html(), #页码
    }
    return render(request, 'number_list.html', context)


def number_add(request):
    '''添加卡号'''
    if request.method == 'GET':
        form = NumberAddForm()
        return render(request, 'number_add.html', {'form': form})

    # 用户post提交数据，数据校验
    form = NumberAddForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/number/list/')
    return render(request, 'number_add.html', {'form': form})


def number_edit(request, nid):
    '''编辑卡号'''
    row_object = models.Number.objects.filter(id=nid).first()

    if request.method == "GET":
        form = NumberEditForm(instance=row_object)
        return render(request, 'number_edit.html', {'form': form})

    form = NumberEditForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/number/list/')
    return render(request, 'number_edit.html', {"form": form})


def number_delete(request, nid):
    '''删除卡号'''
    models.Number.objects.filter(id=nid).delete()
    return redirect('/number/list/')
