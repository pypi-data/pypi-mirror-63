from django.contrib import admin
from django.contrib.admin.options import csrf_protect_m


class DjangoTabbedChangeformAdmin(admin.ModelAdmin):

    tabs = []

    class Media:
        css = {
            "all": [
                "jquery-ui/jquery-ui.min.css",
                "django-tabbed-changeform-admin/css/django-tabbed-changeform-admin.css",
            ]
        }
        js = [
            "jquery3/jquery.js",
            "jquery-ui/jquery-ui.min.js",
            "django-tabbed-changeform-admin/js/django-tabbed-changeform-admin.js",
        ]

    @csrf_protect_m
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context["django_tabbed_changeform_admin_tabs"] = self.get_tabs(request, object_id, form_url, extra_context)
        return super().changeform_view(request, object_id, form_url, extra_context)

    def get_tabs(self, request, object_id, form_url, extra_context):
        return self.tabs
