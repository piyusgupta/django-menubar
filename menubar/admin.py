from django.contrib import admin

from menubar.models import MenuItem


class SubMenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0

    def queryset(self, request, obj=None, **kwargs):
        return super(SubMenuItemInline, self).queryset(request).filter(type=CLS_MENU_TYPE.SubMenu, parent=obj.id)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'type', 'priority', )
    list_filter = ('type', )
    inlines = (SubMenuItemInline, )

admin.site.register(MenuItem, MenuItemAdmin)
