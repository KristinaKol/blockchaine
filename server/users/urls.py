from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^get/$', views.get, name='get'), #получаем информацию о вопросе по id
    url(r'^add/$', views.addChild, name='addChild'), #получаем информацию о вопросе по id
        url(r'^deleteChild/$', views.deleteChild, name='deleteChild'), #получаем информацию о вопросе по id
    #url(r'^get/$', views.get, name='get'),
    url(r'^login/$', views.login, name='login'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^load/$', views.load, name='load'),
    url(r'^get_detail/$', views.getDetail, name='get_detail'),
    url(r'^getUsers/$', views.getUsers, name='getUsers'),
    url(r'^checkLogin/$', views.checkLogin, name='checkLogin'),
    url(r'^getCurrentUser/$', views.getCurrentUser, name='getCurrentUser'),
]