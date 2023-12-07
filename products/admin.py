from django.contrib import admin
from django.contrib.auth.models import Group
from . import models

admin.site.unregister(Group)
admin.site.register(models.Category)
admin.site.register(models.SubCategory)
admin.site.register(models.Product)
admin.site.register(models.ProductImage)
admin.site.register(models.Discount)

