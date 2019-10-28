from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Project)
admin.site.register(Developer)
admin.site.register(Manager)
admin.site.register(ProductBacklog)
admin.site.register(SprintBacklog)
admin.site.register(Task)
admin.site.register(Sprint)
