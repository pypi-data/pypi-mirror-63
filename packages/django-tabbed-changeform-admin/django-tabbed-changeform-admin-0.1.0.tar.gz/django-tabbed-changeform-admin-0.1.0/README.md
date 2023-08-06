# django-tabbed-changeform-admin

Group fieldsets or inlinegroups into tabs for django admin's changeform.

## Install

```shell
pip install django-tabbed-changeform-admin
```

## Usgae

**pro/settings.py**

**Note:**

- We used jquery and jquery-ui's static files, so we MUST add django_static_jquery3 and django_static_jquery_ui in INSTALLED_APPS.
- We override admin/change_form.html, so we MUST add django_tabbed_changeform_admin in INSTALLED_APPS.

```python
INSTALLED_APPS = [
    ....
    'django_static_jquery3',
    'django_static_jquery_ui',
    'django_tabbed_changeform_admin',
    ...
]

```

**app/admin.py**

**Note:**

- Create ModelAdmin based on DjangoTabbedChangeformAdmin.
- Add *a sepcial class name* to every fieldset or inline group.
- Add `tabs` property to admin. It's a list of (Tab-Name, Content-Class-Names) pair.
- You can get `tabs` dynamically by overriding method `get_tabs(self, request, object_id, form_url, extra_context)`.

```python
from django.contrib import admin
from django_tabbed_changeform_admin.admin import DjangoTabbedChangeformAdmin
from .models import Book
from .models import Character


class CharacterInline(admin.TabularInline):
    model = Character
    extra = 0
    classes = ["tab-character-inline"]

class BookAdmin(DjangoTabbedChangeformAdmin, admin.ModelAdmin):
    save_on_top = True
    list_display = ["name", "published_time", "publisher"]
    fieldsets = [
        (None, {
            "fields": ["name"],
            "classes": ["tab-basic"],
        }),
        ("Publish Information", {
            "fields": ["published_time", "publisher"],
            "classes": ["tab-publish-info"],
        })
    ]
    inlines = [
        CharacterInline,
    ]

    tabs = [
        ("Basic Information", ["tab-basic", "tab-publish-info"]),
        ("Characters", ["tab-character-inline"]),
    ]

admin.site.register(Book, BookAdmin)

```

## Releases

### v0.1.0 2020/03/17

- First releases.
