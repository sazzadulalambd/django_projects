from django.contrib import admin
from .models import *

# Register your models here.


class TeamViewAdmin(admin.ModelAdmin):
    list_display = ("name", "position")


class TaskViewAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "assign", "pending",
                    "completed", "created_at", "updated_at")


class AccountViewAdmin(admin.ModelAdmin):
    list_display = ("title",)


admin.site.register(Team, TeamViewAdmin)
admin.site.register(Task, TaskViewAdmin)
admin.site.register(Account, AccountViewAdmin)
