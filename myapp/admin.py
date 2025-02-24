from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(GeneralList)
admin.site.register(CompletedList)
admin.site.register(CancelledList)
admin.site.register(NotComeList)