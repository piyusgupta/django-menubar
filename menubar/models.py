from django.db import models
from django.contrib.auth.models import Group


class CLS_MENU_TYPE:
    Menu = 1
    SubMenu = 2
    ChildSubMenu = 3

MENU_TYPE = (
    (CLS_MENU_TYPE.Menu, 'Menu'),
    (CLS_MENU_TYPE.SubMenu, 'SubMenu'),
    (CLS_MENU_TYPE.ChildSubMenu, 'ChildSubMenu'),
)


class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100, default='#')
    permissions = models.ManyToManyField(Group)
    type = models.PositiveSmallIntegerField(choices=MENU_TYPE)
    priority = models.PositiveSmallIntegerField(default=0)
    parent = models.ForeignKey('self', blank=True, null=True,
                               related_name='children')

    class Meta:
        unique_together = (('title', 'type'),)
        ordering = ('type', 'title')

    def __unicode__(self):
        return "%s : %s" % (self.get_type_display(), self.title)

    def get_children(self):
        return self.children.all().order_by('priority', 'title')
