from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Message, Room, Topic, User
from .form import RoomForm, UserForm , MyUserCreationFrom 
# Create your views here.
# # 构造数据
# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Fronted develpers'},
# ]


def loginPage(request):
    page = 'login'
    # 已经登录的就不让再登录了
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # username = request.POST.get('username').lower()
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            # 验证有没有这个用户
            user = User.objects.get(email=email)
        except:
            # 添加消息，用户不存在,会自动返回给前端
            messages.error(request, 'Username dose not exists.')

        # 通过了存在用户的验证，该校对密码了
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # 成功校对上
            login(request, user)  # 给request增加登录信息
            return redirect('home')
        else:
            messages.error(request, 'Username OR password dose not exists.')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)  # 退出登录
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = MyUserCreationFrom()
    if request.method == 'POST':
        form = MyUserCreationFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # 保存並返回給user
            user.username = user.username.lower()  # 对大小写不敏感了
            user.save()
            login(request, user)  # 登录
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # rooms = Room.objects.filter(topic__name=q)  # 获取数据库的数据
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )  # 获取数据库的数据

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    # room_messages = Message.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    # 将数据传给模板
    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)  # 根据pk获取正确的room
    room_messages = room.message_set.all()
    participants = room.participants.all()
    # print(participants)
    if request.method == 'POST':
        messages = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants,
               }
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        # print(request.POST)
        topic_name = request.POST.get('topic')
        # 获取或者创建 话题
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     # form.save()
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    # 不是room的拥有者，不允许修改
    if request.user != room.host:
        return HttpResponse('You are not allowed here !!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)

        topic_name = request.POST.get('topic')
        # 获取或者创建 话题
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        # if form.is_valid():
        #     form.save()
        #     return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    context = {'obj': room}

    # 不是room的拥有者，不允许修改
    if request.user != room.host:
        return HttpResponse('You are not allowed here !!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    # 不是room的拥有者，不允许修改
    if request.user != message.user:
        return HttpResponse('You are not allowed here !!')

    if request.method == 'POST':
        message.delete()
        # return redirect('room',message.room.id)
        return redirect('home')

    context = {'obj': message}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/update-user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    rooms = Room.objects.all()
    context = {'topics': topics, 'rooms': rooms}
    return render(request, 'base/topics.html', context)

def activityPage(request):
    room_messages = Message.objects.all()[:3]
    context = {'room_messages' :room_messages}
    return render(request, 'base/activity.html', context)


from django.utils.translation import ugettext_lazy as _

def trans_test(request):
    
    context = {'msg': _("Welcome to China")}
    return render(request, 'base/trans_test.html', context)