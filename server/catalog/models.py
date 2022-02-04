from django.db import models
from users.models import ChildModel, UserModel
import datetime
import os



class StoreModel(models.Model):
    class Meta:
        verbose_name = 'Хранилище'
        verbose_name_plural = 'Хранилище'

    
    title = models.CharField(max_length=300, verbose_name='Название', default='')
    description = models.TextField(verbose_name="Описание",   default="",blank=True)
    type = models.CharField(max_length=300, verbose_name='Название', default='')
    user =models.ForeignKey(UserModel,blank=True, null=True,  on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title


    def getJson(self):
        return  {
            'id':self.id,
            'title':self.title,
            'type':self.type,
            'typeText':self.type,
            'description':self.description,
        }




class FolderModel(models.Model):
    class Meta:
        verbose_name = 'Директория'
        verbose_name_plural = 'Директории'

    title = models.CharField(max_length=300, verbose_name='Название', default='')
    parent = models.CharField(max_length=300, verbose_name='Раздел', default='-1')
    store =models.ForeignKey(StoreModel,blank=True, null=True,  on_delete=models.CASCADE)

    def __str__(self):
        return self.title


    def getJson(self):
        return  {
            'id':self.id,
            'title':self.title,
            'parent':self.parent,
            'store':self.store.id
        }


class FileModel(models.Model):
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    
    title = models.CharField(max_length=300, verbose_name='Название', default='')
    store =models.ForeignKey(StoreModel,blank=True, null=True,  on_delete=models.CASCADE)
    folder =models.ForeignKey(FolderModel,blank=True, null=True,  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user =models.ForeignKey(UserModel,blank=True, null=True,  on_delete=models.CASCADE)
    check = models.BooleanField( verbose_name='Поврежден  ли', default=True)

    def __str__(self):
        return self.title


    def getJson(self):
        return  {
            'id':self.id,
            'title':self.title,
            'check':self.check,
            'date':self.created_at.strftime("%d.%m.%Y %H:%M") if self.created_at else "",
            'folder':self.folder.id
        }

class FileEntityModel(models.Model):
    class Meta:
        verbose_name = 'Версии файлов'
        verbose_name_plural = 'Версии файлов'

    title = models.CharField(max_length=300, verbose_name='Название', default='')
    user =models.ForeignKey(UserModel,blank=True, null=True,  on_delete=models.CASCADE)
    file =models.ForeignKey(FileModel,blank=True, null=True,  on_delete=models.CASCADE)
    entity = models.FileField(upload_to='store/', null=True, verbose_name='Фото', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField(auto_now_add=True)


    # def __str__(self):
    #     return self.file.title


    def getJson(self):

        fullfilepath=  os.path.join(os.path.dirname(os.path.dirname(__file__)),"media/store/" + str(self.file.title))
        filesize= os.path.getsize(fullfilepath)

        return  {
            'id':self.id,
            'title':self.title,
            'title_parent':self.file.title,
            'size':filesize,
            'user':self.user.getJson(),
            'date':self.created_at.strftime("%d.%m.%Y %H:%M:%S") if self.created_at else "",
            'date_update':self.pub_date.strftime("%d.%m.%Y %H:%M:%S") if self.pub_date else ""
        }



class AccessModel(models.Model):
    class Meta:
        verbose_name = 'Права'
        verbose_name_plural = 'Права'

    file =models.ForeignKey(FileModel,blank=True, null=True,  on_delete=models.CASCADE)
    user =models.ForeignKey(UserModel,blank=True, null=True,  on_delete=models.CASCADE)

    read = models.BooleanField( verbose_name='Чтение', default=False)
    write = models.BooleanField(verbose_name="Запись",   default=False)

    
    def __str__(self):
        return self.user.name


    def getJson(self, addUser = False):
        result = {
            'id':self.id,
            'read':self.read,
            'write':self.write,
            'access':False
        }

        if addUser:
            result['user'] = self.user.getJson()

        return result


class StoreUserModel(models.Model):
    class Meta:
        verbose_name = 'Пользовтель хранилища'
        verbose_name_plural = 'Пользовтели хранилища'

    
    store =models.ForeignKey(StoreModel,blank=True, null=True,  on_delete=models.CASCADE)
    user =models.ForeignKey(UserModel, blank=True, null=True,  on_delete=models.CASCADE)


    def __str__(self):
        return self.store.title

