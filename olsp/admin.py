from django.contrib import admin
from olsp import models
admin.site.register(models.User)
admin.site.register(models.Taken)
admin.site.register(models.Course)
admin.site.register(models.Categories)
admin.site.register(models.Material)
admin.site.register(models.Chapter)
admin.site.register(models.Chat)
admin.site.register(models.TakenCourse)
admin.site.register(models.Superuser)