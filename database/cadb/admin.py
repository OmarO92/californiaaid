from django.contrib import admin

# Register your models here.
from .models import EoooStudent, EoooDistributedto
admin.site.register(EoooStudent)
admin.site.register(EoooDistributedto)
