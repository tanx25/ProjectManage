from django.contrib import admin
from .models import Project, CustomUser, Step

admin.site.register(Project)
admin.site.register(CustomUser)
admin.site.register(Step)

