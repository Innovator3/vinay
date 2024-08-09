from django.contrib import admin
from .models import User, DocumentTypes

# Register your models here.


class Userfileds(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.get_fields()]


class DocumentTypesfileds(admin.ModelAdmin):
    list_display = [field.name for field in DocumentTypes._meta.get_fields()]


admin.site.register(User, Userfileds)
admin.site.register(DocumentTypes, DocumentTypesfileds)
