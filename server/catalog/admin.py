from django.contrib import admin

# Register your models here.
from catalog.models import StoreModel,FolderModel, FileModel, FileEntityModel, StoreUserModel, BlockModel, AccessModel
from datetime import datetime




class CatalogAdmin(admin.ModelAdmin):
    list_display = ('__str__',)



class FileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

    def save_model(self, request, obj, form, change):
            obj.pub_date = datetime.now()
            obj.save()

admin.site.register(AccessModel,CatalogAdmin)
admin.site.register(BlockModel,CatalogAdmin)
admin.site.register(StoreUserModel,CatalogAdmin)
admin.site.register(StoreModel,CatalogAdmin)
admin.site.register(FolderModel,CatalogAdmin)
admin.site.register(FileModel,CatalogAdmin)
admin.site.register(FileEntityModel,FileAdmin)