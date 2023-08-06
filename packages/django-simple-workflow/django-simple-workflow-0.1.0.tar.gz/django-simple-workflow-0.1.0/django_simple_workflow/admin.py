from django.contrib import admin
from .models import Node
from .models import Transition
from .models import Role
from .models import ProcessDefinition
from .models import Data
from pprint import pprint

class DataAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, change=False, **kwargs):
        
        form = super().get_form(request, obj, change, **kwargs)
        pprint(form)
        pprint(dir(form))
        pprint(form.base_fields)
        f = form.base_fields["f1"]
        pprint(f)
        pprint(dir(f))
        pprint(f.label)
        pprint(f.label_suffix)
        f.label = "测试"
        f.help_text = "测试字段噢^_^"
        return form

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return [(None, {"fields": ["type"]})]
        else:
            if obj.type == "t1":
                return [(None, {"fields": ["f1"]})]
            elif obj.type == "t2":
                return [(None, {"fields": ["f2"]})]
            else:
                return []

class RoleInline(admin.TabularInline):
    model = Role
    extra = 0

class NodeInline(admin.TabularInline):
    model = Node
    extra = 0

class TransitionInline(admin.TabularInline):
    model = Transition
    extra = 0

class ProcessDefinitionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [
        RoleInline,
        NodeInline,
        TransitionInline,
    ]

admin.site.register(ProcessDefinition, ProcessDefinitionAdmin)
admin.site.register(Data, DataAdmin)
