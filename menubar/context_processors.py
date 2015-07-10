from django.conf import settings
from django.core.cache import cache
from django.utils.datastructures import SortedDict
from django.contrib.auth.models import User, Group

from menubar.models import MenuItem, CLS_MENU_TYPE


def SetMenuItemContext(request):
    variables = {'menuitem': get_menu_item(request.user)}
    return variables


def get_menu_item(user):
    user_groups = user.groups.all()
    # check if it exists in the cached data
    _cache_key = "menubar-cached-key-groups-%s" % ("-".join([str(x) for x in user_groups.values_list('id', flat=True)]))
    menubar_items = cache.get(_cache_key)
    if not menubar_items:
        menubar_items = SortedDict({})
        first_level = MenuItem.objects.filter(type=CLS_MENU_TYPE.Menu, permissions__in=user_groups).order_by('priority', 'title')
        for menu in first_level:
            key = (menu.url, menu.title,)
            values = {}
            for menu1 in menu.get_children().filter(permissions__in=user_groups):
                values[(menu1.url, menu1.title,)] = menu1.get_children().filter(permissions__in=user_groups).values_list('url', 'title')
            menubar_items[key] = values
        cache.set(_cache_key, menubar_items, 10 * 60)  # cache it for 10 mins
    return menubar_items
