from django.contrib import admin

from .models import *


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','bank','department','author','date_comm','stars')
    list_display_links = ('id','bank','department','author','date_comm','stars')
    search_fields = ('bank','department','author','date_comm','stars')
    list_filter = ('bank','department','author','date_comm','stars')

# class BankAdmin(admin.ModelAdmin):
#     list_display =('id','name')
#     list_display_links =('id','name')
#     search_fields = ('name',)

admin.site.register(Comment,CommentAdmin)
# admin.site.register(Bank, BankAdmin)
# admin.site.register(Department)
