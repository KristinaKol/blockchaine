import json
import datetime
import hashlib
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from users.models import  UserModel


#РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
@csrf_exempt
def registration(request):
    #получаем параметры post запроса
    post = json.loads(request.body)


    login = post['email'].lower()
    name = post['name']
    password = post['password']
    #email = post['email'].lower()


    #создаем пользователя
    userQS = UserModel.objects.create(
        login=login,
        name=name,
        password=password,
        #email=email,
    )


    return JsonResponse(userQS.getJson())



#АВТОРИЗАЦИЯ ПОЛЬЗОВАТЕЛЯ
@csrf_exempt
def login(request):

    #получаем параметры post запроса
    post = json.loads(request.body)

    login = post['login'].lower()
    password = post['password']

    usersQS = UserModel.objects.filter(login=login,password=password)


    if usersQS.count() > 0:
        #меняем токен
        UserModel.objects.filter(login=login, password=password).update(token=token)

        response = JsonResponse({
            'token': token
        })


    else:
        response = JsonResponse({
            'error': 1,
            'code': 401
        })


    return response



@csrf_exempt
#выход пользователя
def logout(request):
    usersQS = UserModel.objects.filter(id=request["id"]).update(token="")
    return JsonResponse({"result":"ok"})










def byToken(request):

    result = -1
    if "token" in request.COOKIES:
        usersQS = UserModel.objects.filter(token=request.COOKIES["token"])
        users = []
        if len(usersQS) > 0:
            return usersQS[0].getJson()

    return result

