from django.contrib import admin


class GenericAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + ('created_at',)
