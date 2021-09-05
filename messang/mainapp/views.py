from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from django.views import generic


def home(request):
    return render(request, 'home.html')

# def my_decator(f):
#     def wrapper(request, **kwargs):

#         f()
#         user = request.user.username
#         return render(request, 'room.html', {
#             'room_name': room_name,
#             'user': user
#     })
#     return wrapper


@login_required
def room(request, room_name):
    user = request.user.username
    return render(request, 'room.html', {
        'room_name': room_name,
        'user': user
    })


@login_required
def chat(request):
    user = request.user.username
    return render(request, 'room.html', {
        # 'room_name': room_name,
        'user': user
    })
    return render(request, 'chat.html')



