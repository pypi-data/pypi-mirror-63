# django-with-extra-context-admin

Provide a simple way to add extra context for view rendering in Django's admin site.

## Install

```shell
pip install django-with-extra-context-admin
```

## Usage

**Note:**

There is NO need to add app name django_with_extra_context_admin into INSTALLED_APPS. Just install this application and import the admin extention DjangoWithExtraContextAdmin where you need.


**app/admin.py**

```python
from django.contrib import admin
from django_with_extra_context_admin.admin import DjangoWithExtraContextAdmin
from .models import MyModel

class MyModelAdmin(DjangoWithExtraContextAdmin, admin.ModelAdmin):

    django_with_extra_context_admin_view_name = False

    def get_extra_context(self, request, **kwargs):
        extra_context = super().get_extra_context(request, **kwargs) or {}
        extra_context.update({
            ...
            "var1": "value1",
            "var2": "value2",
            ...
        })
        return extra_context

admin.site.register(MyModel, MyModelAdmin)
```

## Where to use?

All admin's default views are inject with the extra context.

- changeform_view
- changelist_view
- delete_view
- history_view
- add_view
- change_view

## Any extra context provided?

By default we always add *django_with_extra_context_admin_view_name* to the extra context. It can be disabled by set add_django_with_extra_context_admin_view_name to False. The value of variable django_with_extra_context_admin_view_name is the the name of current view name, e.g. changeform_view, changelist_view.


## Releases

### v0.1.0 2020/03/13

- First release.