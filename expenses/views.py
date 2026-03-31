from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'expenses/index.html')

@login_required
def add(request):
    return HttpResponse('add')

@login_required
def edit(request, id: int):
    return HttpResponse('edit')

@login_required
def delete(request, id: int):
    return HttpResponse('delete')
