from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group

def own_this(func):
    def callf(self, queryset=None):
        obj = func(self, queryset)
        if obj.user == self.request.user:
            return obj
        else:
            raise PermissionDenied

    return callf

def in_group(group_name):
    def deco(func):
        def callf(self, request, *args, **kwargs):

            if request.user.groups.filter(name=group_name).exists():
                return func(self, request, *args, **kwargs)
            else:
                raise PermissionDenied
        return callf
    return deco
