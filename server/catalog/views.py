import json
import datetime
from django.http import JsonResponse
from django.shortcuts import render
import secure
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from cryptography.fernet import Fernet

from users.views import getUserIdByToken
from catalog.models import StoreModel,FolderModel, FileModel, FileEntityModel, StoreUserModel, BlockModel, AccessModel
from users.views import md5
# from classes.Metrika import MetricaApi





#ОБНОВЛЕНИЕ В МАТРИЦЕ ДОСТУПА
@csrf_exempt
def updateSecure(request):
    post = json.loads(request.body)
    if post['id'] == -1:
        secure = AccessModel.objects.create(
            user_id = post['user']['id'],
            file_id = post['fileId'],
            read = post['read'],
            write = post['write'],
        )
    else:
        AccessModel.objects.filter(id = post['id']).update(
            read = post['read'],
            write = post['write'],
        )
        secure = AccessModel.objects.get(id = post['id'])
    return  JsonResponse(secure.getJson(True), safe=False)


#СОЗДАТЬ ДИРЕКТОРИЮ
@csrf_exempt
def addFolder(request):
    post = json.loads(request.body)
    user = getUserIdByToken(request)
    #В ТАБЛИЦУ С ДИРЕКТОРИЯМИ СОЗДАЕТСЯ ЗАПИСЬ
    folder = FolderModel.objects.create(
            title=post['title'],
            parent = post['parent'],
            store_id =post['store']
    )
    addBlock("ADD_FOLDER",folder.id, folder.store.id,user["id"])
    return  JsonResponse(folder.getJson(), safe=False)


#СОЗДАТЬ ФАЙЛ
@csrf_exempt
def addFile(request):
    data = request.GET
    user = getUserIdByToken(request)
    typeOperation = ""

    if  data['type'] == 'folder':
        typeOperation = "ADD_FILE"

        files = FileModel.objects.filter(
                title=request.FILES["file"].name,
                folder_id=data['value']
        )
        if len(files) > 0:
            typeOperation = "UPDATE_FILE"
            file = files[0]
        else:
            file = FileModel.objects.create(
                    title=request.FILES["file"].name,
                    folder_id=data['value'],
                    user_id = user['id']
            )

    else:
        typeOperation = "UPDATE_FILE"
        file  = FileModel.objects.get(id=data['value'] )

    
    fileEntity = FileEntityModel.objects.create(
               user_id=user["id"],
               file_id=file.id,
               title=request.FILES["file"].name,
               entity=request.FILES["file"]
        )

    addBlock(typeOperation,file.id, file.folder.store.id,user["id"])

    fileJson = file.getJson()
    fileJson['version'] = []
    fileJson['secure'] = getSecure(file, user)
    versionQS = FileEntityModel.objects.filter(
        file_id = file.id
    )

    for v in versionQS:
        fileJson['version'].append(v.getJson())

    return  JsonResponse(fileJson, safe=False)


#СОЗДАТЬ ХРАНИЛИЩЕ
@csrf_exempt
def addStore(request):
    post = json.loads(request.body)
    user = getUserIdByToken(request)
    users = post['users']
    users.append(user["id"])

    #СОЗДАТЬ ЗАПИСЬ В ТАБЛИЦЕ ХРАНИЛИЩ
    store = StoreModel.objects.create(
            title=post['title'],
            user_id = user['id'],
            type = post['type']
    )

    for u in users:
        StoreUserModel.objects.create(
            store_id = store.id,
            user_id = u
        )

    tmp = store.getJson()
    tmp['users'] = []
    userQS = StoreUserModel.objects.filter(store_id = store.id)
    for u in userQS:
        tmp['users'].append(u.user.getJson())


    addBlock("ADD_STORE",store.id, store.id,user["id"])
    return  JsonResponse(tmp, safe=False)





#ВЫВЕСТИ МАТРИЦУ ДОСТУПА
def getSecure(file, user):
    secure = {
        "read" : True,
        "write" : False,
        "access" : False
    }

    #ПРАВА НА ЭТОГО ПОЛЬЗОВАТЕЛЯ И ЭТОТ ФАЙЛ
    store = file.folder.store
    #ВЛАДЕЛЕЦ ЛИ ?
    if user["id"] == file.user.id or user["id"] == store.user.id:
        secure = {
            "read" : True,
            "write" : True,
            "access" : True
        }
    accessQS = AccessModel.objects.filter(file_id=file.id, user_id = user['id'])
    for v in accessQS:
        secure = v.getJson()

    return secure




#СКАЧАТЬ БЛОКИ ИЗ СЕТИ
def getBlocks(file, user):



    secure = {
        "read" : True,
        "write" : False,
        "access" : False
    }

    #ПРАВА НА ЭТОГО ПОЛЬЗОВАТЕЛЯ И ЭТОТ ФАЙЛ
    store = file.folder.store
    #ВЛАДЕЛЕЦ ЛИ ?
    if user["id"] == file.user.id or user["id"] == store.user.id:
        secure = {
            "read" : True,
            "write" : True,
            "access" : True
        }
    accessQS = AccessModel.objects.filter(file_id=file.id, user_id = user['id'])
    for v in accessQS:
        secure = v.getJson()

    return secure

##ОТПРАВИТЬ БЛОК В БЛОКЧЕЙН
def addBlock(type,value, store_id, user_id):
    
    timestamp = datetime.datetime.timestamp(datetime.datetime.now())
    lastBlock = BlockModel.objects.filter(store_id=store_id).order_by('-id')

    if len(lastBlock) == 0:
        prevHash="-"
    else:
        prevHash=lastBlock[0].hash



    typeBlock = type



    hash = md5(str(value))

    return  BlockModel.objects.create(
            hash=hash,
            time= timestamp,
            prevHash=prevHash,
            type=typeBlock ,
            value=value,
            store_id=store_id,
            user_id=user_id
    )


#ВЫВЕСТИ ВСЕ ОСТАЛЬНЕ ДАЛЕЕ ПО ТИПАМ
@csrf_exempt
def get(request):
    data = request.GET
    user = getUserIdByToken(request)
    catalogEntity = {
        'folders':FolderModel,
        'files':FileModel,
        #'fileEntity':FileEntityModel
    }

    result = []
    needResult = True
#ВЫВЕСТИ ХРАНИЛИЩА
    if data["type"] == "store":

        store_ids = []
        storeUsers = StoreUserModel.objects.filter(user_id=user["id"])
        for u in storeUsers:
            store_ids.append(u.store.id)

        needResult = False
        resultQS = StoreModel.objects.filter(id__in=store_ids)
     
        for s in resultQS:
            tmp = s.getJson()
            tmp['users'] = []
            userQS = StoreUserModel.objects.filter(store_id = s.id)
            for u in userQS:
                tmp['users'].append(u.user.getJson())

            result.append(tmp)        

    


    if data["type"] == "entity":
        resultQS = FileEntityModel.objects.filter(file_id=data["id"])
    if data["type"] == "block":
        resultQS = BlockModel.objects.all().order_by('-id')

    if data["type"] == "block_detail":
        needResult = False
        resultQS = BlockModel.objects.get(id=data["id"])
        result = resultQS.getJson()
        if resultQS.type == "UPDATE_FILE":
            file = FileModel.objects.get(id=resultQS.value)
            result["detail"] = file.getJson()
            result["typeText"] = "Добавлена версия"

        if resultQS.type == "ADD_FILE":
            file = FileModel.objects.get(id=resultQS.value)
            result["detail"] = file.getJson()
            result["typeText"] = "Создан файл"

        if resultQS.type == "ADD_FOLDER":
            folder = FolderModel.objects.get(id=resultQS.value)
            
            result["detail"] = folder.getJson()
            result["typeText"] = "Создана директория"

        if resultQS.type == "ADD_STORE":
            store = StoreModel.objects.get(id=resultQS.value)
            
            result["detail"] = store.getJson()
            result["typeText"] = "Создано хранилище"

    if data["type"] == "secure":
        needResult = False
        users = []
        result = []
        file = FileModel.objects.get(id = data['id'])
        accessListQS = AccessModel.objects.filter(file_id=file.id)            
        for t in accessListQS:
            result.append( t.getJson(True))
            users.append(t.user.id)
        #ВЫГРУЖАЕМ ПОЛЬЗОВАТЕЛЕЙ
        #ДЛЯ ФОРМИРОВАНИЯ МАТРИЦЫ ДОСТУПА
        store = file.folder.store
        usersQS = StoreUserModel.objects.filter(store_id = store.id)

        for u in usersQS:
            if u.user.id == file.user.id or u.user.id == store.user.id or u.user.id in users:
                continue              
            result.append( {
                "id" : -1,
                "user":u.user.getJson(),
                "fileId": data['id'],
                "read" : True,
                "write" : False,
                "access" : False 
            })


        #ЧИТАЕМ МАТРИЦУ ДОСТУПА
    if data["type"] == "check":
        needResult = False
        result = []
        files = []
        folders = []
        foldersId = []
        store = StoreModel.objects.get(id = data['id'])

        folderQS = FolderModel.objects.filter(store_id=data['id'])
        for f in folderQS:
            folders.append(f.getJson())
            foldersId.append(f.id)

        fileQS = FileModel.objects.filter(folder_id__in=foldersId)
        for f in fileQS:
            file = f.getJson()
            filesEntityQS = FileEntityModel.objects.filter(file_id=f.id)
            for entity in filesEntityQS:
                obj = entity.getJson()
                obj['check'] = obj['date'] == obj['date_update']
                if not obj['check']:
                    FileModel.objects.filter(id=entity.file.id).update(
                        check = False
                    )
                result.append(obj)



            file["secure"] = getSecure(f, user)
            files.append(file)

        

    if data["type"] == "catalog":
        needResult = False
        result = {
            'folders':[],
            'files':[]
        }
        files = []
        folders = []
        foldersId = []
        store = StoreModel.objects.get(id = data['id'])

        folderQS = FolderModel.objects.filter(store_id=data['id'])
        for f in folderQS:
            folders.append(f.getJson())
            foldersId.append(f.id)

        fileQS = FileModel.objects.filter(folder_id__in=foldersId)
        for f in fileQS:
            file = f.getJson()
            file["count"] = FileEntityModel.objects.filter(file_id=f.id).count()
            file["secure"] = getSecure(f, user)
            files.append(file)


        result = {
            'folders':folders,
            'files':files
        }



    if needResult:
        for item in resultQS:
            result.append(item.getJson())

    return  JsonResponse(result, safe=False)

    