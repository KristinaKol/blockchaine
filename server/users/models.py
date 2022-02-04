from django.db import models

# Create your models here.

class UserModel(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'

    #авторизационные данные
    login = models.CharField(max_length=100, verbose_name='Логин', blank=True)
    password = models.CharField(max_length=100, verbose_name='Пароль', default="")
    token  = models.CharField(max_length=100, verbose_name='Токен', blank=True)
 
    email = models.CharField(max_length=100, verbose_name='Почта', blank=True)
    phone = models.CharField(max_length=100, verbose_name='Номер телефона', blank=True)
  
    name = models.CharField(max_length=300, verbose_name='Имя', default='')
    text = models.TextField(verbose_name="Описание",default="",blank=True)
    image = models.FileField(upload_to='images/users/', null=True, verbose_name='Фото', blank=True)

    def __str__(self):
        return self.name


    def getJson(self):
        return  {
            'id':self.id,
            'name':self.name,
            'login':self.login,
            'image': "http://veronika.tasty-catalog.ru"+self.image.url if self.image else "http://veronika.tasty-catalog.ru/media/images/users/image_4.jpg",
            'text':self.text
        }
