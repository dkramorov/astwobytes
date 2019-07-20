from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request, *args, **kwargs):

    #from .models import create_default_user
    #create_default_user()

    user = authenticate(username='jocker', password='cnfylfhnysq')
    if user is not None:
        login(request, user)
        return HttpResponse(f'Hi, {user}')

    return HttpResponse('Hi')

#@login_required
def logout_view(request, *args, **kwargs):
    logout(request)
    return HttpResponse('Logout successful')
