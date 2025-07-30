from django.contrib import admin
from .models import Menu, MenuItem

class MenuItemInline(admin.StackedInline):
    model = MenuItem
    extra = 1
    fields = ['title', 'url', 'named_url', 'parent']
    autocomplete_fields = ['parent']

class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]
    list_display = ('name',)
    search_fields = ('name',)

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent')
    list_filter = ('menu',)
    search_fields = ('title',)
    autocomplete_fields = ['parent']
    ordering = ('menu', 'parent_id', 'title')

admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
