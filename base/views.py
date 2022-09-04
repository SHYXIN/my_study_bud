from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# 构造数据
rooms = [
    {'id': 1, 'name': 'Lets learn python!'},
    {'id': 2, 'name': 'Design with me'},
    {'id': 3, 'name': 'Fronted develpers'},
]


def home(request):
    # 将数据传给模板
    context = {'rooms': rooms}
    return render(request, 'home.html', context)


def room(request):
    return render(request, 'room.html')
