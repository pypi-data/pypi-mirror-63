import json
from pprint import pprint
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django import forms
from django.forms.models import ModelChoiceField
from django.template.loader import render_to_string
from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter
from django_dynamic_resource_admin.admin import DjangoDynamicResourceAdmin
from django_cascading_dropdown_widget.widgets import DjangoCascadingDropdownWidget
from django_cascading_dropdown_widget.widgets import CascadingModelchoices
from .models import ModelDefinition
from .models import ModelField
from .models import ModelDefinitionCategory
from .models import FieldWidget
from .models import Data
from .models import get_field_type_choices
from .models import ModelFieldset
from .models import ModelInline

class FieldWidgetForm(forms.ModelForm):
    field_type = forms.ChoiceField(choices=[("", "----------")] + get_field_type_choices())

    class Meta:
        model = FieldWidget
        exclude =[]

class FieldWidgetAdmin(admin.ModelAdmin):
    form = FieldWidgetForm
    list_display = ["name"]

class ModelDefinitionInline(admin.TabularInline):
    model = ModelDefinition
    extra = 0

class ModelDefinitionCategoryAdmin(DraggableMPTTAdmin):
    list_display = ["tree_actions", "indented_title"]
    list_display_links = ["indented_title"]
    inlines = [
        ModelDefinitionInline,
    ]

class ModelFieldsetInline(admin.TabularInline):
    model = ModelFieldset
    extra = 0

class ModelInlineForm(forms.ModelForm):
    class Meta:
        model = ModelInline
        exclude = []
        widgets = {
            "model": DjangoCascadingDropdownWidget(choices=CascadingModelchoices({
                "model": ModelDefinitionCategory,
                "related_name": "definitions",
                "str": "indented_title",
            },{
                "model": ModelDefinition,
                "fk_name": "parent",
            }))
        }

class ModelInlineInline(admin.TabularInline):
    form = ModelInlineForm
    model = ModelInline
    fk_name = "definition"
    extra = 0

class ModelFieldInline(admin.TabularInline):
    model = ModelField
    extra = 0

class ModelDefinitionAdmin(admin.ModelAdmin):

    class Media:
        css = {
            "all": [
                "django-dynamic-model-admin/css/modeldefinition-admin.css",
            ]
        }

    list_display = ["verbose_name", "name", "parent"]
    list_display_links = ["verbose_name"]
    search_fields = ["verbose_name", "name"]
    list_filter = [
        ("parent", TreeRelatedFieldListFilter),
    ]
    inlines = [
        ModelFieldsetInline,
        ModelInlineInline,
        ModelFieldInline,
    ]
    
    def get_form(self, *args, **kwargs):
        return super().get_form(*args, **kwargs)

class DataInline(InlineModelAdmin):
    model = Data

    def __init__(self, parent_model, admin_site, fk_name, md, extra=0):
        self.fk_name = fk_name
        self.md = md
        self.extra = extra
        super().__init__(parent_model, admin_site)
        self.verbose_name = self.md.verbose_name
        self.verbose_name_plural = self.md.get_verbose_name_plural()

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields["md"] = ModelChoiceField(ModelDefinition.objects, initial=self.md, widget=forms.HiddenInput())
        fields_map = self.md.get_fields_map()
        for field_name, field in formset.form.base_fields.items():
            if field_name in fields_map:
                field.label = fields_map[field_name].verbose_name
                field.help_text = fields_map[field_name].help_text
                field.required = fields_map[field_name].required
        return formset

    def get_fieldsets(self, request, obj=None):
        return self.md.get_fieldsets(["md"])

class DataTabularInline(admin.TabularInline, DataInline):
    pass

class DataStackedInline(admin.StackedInline, DataInline):
    pass


class DataAdmin(
        DjangoDynamicResourceAdmin,
        admin.ModelAdmin):

    class Media:
        css = {
            "all": [
                "django-dynamic-model-admin/css/data-admin.css",
            ]
        }
    list_display = ["pk", "title", "md", "create_time", "update_time"]
    list_filter = ["md"]

    def get_css(self, request, **kwargs):
        extra_css = super().get_css(request, **kwargs)
        if "object_id" in kwargs and kwargs["object_id"]:
            object_id = int(kwargs["object_id"])
            obj = self.model.objects.get(pk=object_id)
            if obj.md and obj.md.label_width:
                extra_css.append(render_to_string("django-dynamic-model-admin/data/data-css.css", {
                    "lable_width": obj.md.label_width,
                }))
        return extra_css

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if obj:
            fields_map = obj.md.get_fields_map()
            for field_name, field in form.base_fields.items():
                if field_name in ["md"]:
                    field.widget = forms.HiddenInput()
                if field_name in fields_map:
                    field.label = fields_map[field_name].verbose_name
                    field.help_text = fields_map[field_name].help_text
                    field.required = fields_map[field_name].required
        else:
            if "md" in form.base_fields:
                form.base_fields["md"].widget = DjangoCascadingDropdownWidget(choices=CascadingModelchoices({
                    "model": ModelDefinitionCategory,
                    "related_name": "definitions",
                    "str": "indented_title",
                },{
                    "model": ModelDefinition,
                    "fk_name": "parent",
                }))
        return form
    
    def get_fieldsets(self, request, obj=None):
        if obj:
            return obj.md.get_fieldsets(["md"])
        else:
            return [(None, {"fields": ["md"]})]

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if obj:
            for inline in obj.md.inlines.all():
                if inline.type == inline.TabularInline:
                    instance = DataTabularInline(Data, self.admin_site, inline.fk_name, inline.model, inline.extra)
                else:
                    instance = DataStackedInline(Data, self.admin_site, inline.fk_name, inline.model, inline.extra)
                inline_instances.append(instance)
        return inline_instances

admin.site.register(ModelDefinitionCategory, ModelDefinitionCategoryAdmin)
admin.site.register(ModelDefinition, ModelDefinitionAdmin)
admin.site.register(FieldWidget, FieldWidgetAdmin)
admin.site.register(Data, DataAdmin)
