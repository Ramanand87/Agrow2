from django.contrib import admin
from . import models
from django.utils.html import format_html

class ChatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'formatted_response', 'messages', 'curr_user')

    def formatted_response(self, obj):
        return format_html(obj.response)

    formatted_response.short_description = 'Response'

admin.site.register(models.Profile)
admin.site.register(models.Schemes)
admin.site.register(models.chats, ChatsAdmin)
admin.site.register(models.crophealth)
admin.site.register(models.loan)
admin.site.register(models.posts)
