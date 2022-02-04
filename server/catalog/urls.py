from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^get/$', views.get, name='get'), #получаем информацию о вопросе по id
    url(r'^updateSecure/$', views.updateSecure, name='updateSecure'), #получаем информацию о вопросе по id
    url(r'^addFolder/$', views.addFolder, name='addFolder'), #получаем информацию о вопросе по id
    url(r'^addFile/$', views.addFile, name='addFile'), #получаем информацию о вопросе по id
    url(r'^addStore/$', views.addStore, name='addStore'), #получаем информацию о вопросе по id
    url(r'^listCategory/$', views.listCategory, name='listCategory'), #получаем информацию о вопросе по id
    url(r'^getMetrica/$', views.getMetrica, name='getMetrica'), #получаем информацию о вопросе по id
    #url(r'^updateFile/$', views.updateFile, name='updateFile'), #получаем информацию о вопросе по id

]