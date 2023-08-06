import functools
import json
import yaml
from fastutils import strutils
from django.db import models
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _
from django import forms
from django_yearmonth_widget.widgets import DjangoYearMonthWidget
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


def text_input(**kwargs):
    field_kwargs = {}
    field_kwargs.update(kwargs)
    if "attrs" in field_kwargs:
        attrs = field_kwargs["attrs"]
        del field_kwargs["attrs"]
    else:
        attrs = None    
    field = forms.CharField(**field_kwargs)
    widget = forms.TextInput(attrs)
    return field, widget

def text_area(**kwargs):
    attrs = kwargs.get("attrs", None)
    field = None
    widget = forms.Textarea(attrs)
    return field, widget

def email_input(**kwargs):
    attrs = kwargs.get("attrs", None)
    field = forms.EmailField()
    widget = forms.EmailInput(attrs)
    return field, widget

def django_yearmonth_widget(**kwargs):
    attrs = kwargs.get("attrs", None)
    years = kwargs.get("years", None)
    prev_years = kwargs.get("prev_years", 10)
    next_years = kwargs.get("next_years", 0)
    day_value = kwargs.get("day_value", 1)
    field = None
    widget = DjangoYearMonthWidget(attrs, years, prev_years, next_years, day_value)
    return field, widget

FIELD_TYPES = {
    "CharField": {
        "field": lambda : models.CharField(max_length=4096, null=True, blank=True, db_index=True),
        "prefix": "c",
        "widgets": [
            ("6ade27e6-3b30-4ac4-8a28-21447924b817", "TextInput", text_input),
            ("2a5c1354-2d46-4459-af02-3d36d5188c1c", "TextArea", text_area),
            ("a4b700ac-f8e2-47ee-a628-28ee061fad6f", "EmailInput", email_input),
            ("5c8fd75d-69d0-44c1-8630-734e235a0cf4", "YearMonthSelect", django_yearmonth_widget),
        ],
    },
    "IntegerField": {
        "field": lambda : models.IntegerField(null=True, blank=True, db_index=True),
        "prefix": "i",
        "widgets": [
        ],
    },
    "TextField": {
        "field": lambda: models.TextField(null=True, blank=True, db_index=True),
        "prefix": "t",
        "widgets": [
        ],
    },
    "DateField": {
        "field": lambda: models.DateField(null=True, blank=True, db_index=True),
        "prefix": "d",
        "widgets": [],
        "widgets": [],
    },
    "DateTimeField": {
        "field": lambda: models.DateTimeField(null=True, blank=True, db_index=True),
        "prefix": "dt",
        "widgets": [],
    },
    "DecimalField": {
        "field": lambda: models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, db_index=True),
        "prefix": "dc",
        "widgets": [],
    },
    "ForeignKey": {
        "field": lambda: models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"),
        "prefix": "fk",
        "widgets": [
        ],
    },
}

def get_field_widget_choices():
    choices = []
    for field_name, field_meta in FIELD_TYPES.items():
        typed_choices = []
        for widget_uuid, widget_name, widget_creator in field_meta["widgets"]:
            typed_choices.append((widget_uuid, widget_name))
        choices.append((field_name, typed_choices))
    return choices

def get_field_widget(the_widget_uuid, obj):
    if not the_widget_uuid:
        return None, None
    if obj:
        kwargs = obj.definition.fields.get(field_widget=the_widget_uuid).parameters
    else:
        kwargs = {}
    for field_name, field_meta in FIELD_TYPES.items():
        for widget_uuid, widget_name, widget_creator in field_meta["widgets"]:
            if widget_uuid == the_widget_uuid:
                return widget_creator(**kwargs)
    return None, None

class ModelDefinitionAbstractBase(MPTTModel):
    parent = TreeForeignKey("self", on_delete=models.CASCADE, related_name="children", null=True, blank=True, verbose_name=_("Model Definition Category"))
    verbose_name = models.CharField(max_length=64, verbose_name=_("Verbose Name"))
    verbose_name_plural = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Verbose Name Plural"))
    title_template = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Title Template"))
    label_width = models.CharField(max_length=32, null=True, blank=True, verbose_name=_("Label Width"), help_text=_("Add unit, e.g. 120px"))

    class Meta:
        verbose_name = _("Model Definition")
        verbose_name_plural = _("Model Definitions")
        abstract = True

    def __str__(self):
        return self.verbose_name

    def get_verbose_name_plural(self):
        if self.verbose_name_plural:
            return self.verbose_name_plural
        else:
            return self.verbose_name

    def get_prefer_name_map(self):
        map = {}
        for field in self.fields.all():
            if field.prefered_field_name:
                map[field.prefered_field_name] = field.real_field_name
            if field.verbose_name:
                map[field.verbose_name] = field.real_field_name
        return map

    def get_fieldsets(self, extra_fields=None):
        extra_fields = extra_fields or []
        fieldsets = []
        prefer_name_map = self.get_prefer_name_map()
        first = True
        for fieldset in self.fieldsets.all():
            if first:
                fieldsets.append(fieldset.get_fieldset(prefer_name_map, extra_fields))
            else:
                fieldsets.append(fieldset.get_fieldset(prefer_name_map))
            first = False
        return fieldsets

    def get_fields_map(self):
        map = {}
        for field in self.fields.all():
            map[field.real_field_name] = field
        return map

class ModelFieldsetAbstractBase(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Name"))
    fields = models.TextField(null=True, blank=True, verbose_name=_("Fields"))
    classes = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Classes"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Model Fieldset")
        verbose_name_plural = _("Model Fieldsets")
        ordering = ["order"]
        abstract = True

    def __str__(self):
        return str(self.pk)

    def get_fieldset(self, prefer_name_map, extra_fields=None):
        fields = [] + (extra_fields or [])
        if self.fields:
            for line in self.fields.splitlines():
                line = line.strip()
                if not line:
                    continue
                field_row = []
                for field in strutils.split(line, [",", "，", "、"]):
                    field = field.strip()
                    if not field:
                        continue
                    real_field_name = prefer_name_map.get(field, None)
                    if not real_field_name:
                        continue
                    field_row.append(real_field_name)
                fields.append(field_row)
        classes = []
        if self.classes:
            for klass in self.classes.split():
                klass = klass.strip()
                if not klass:
                    continue
                classes.append(klass)
        return [self.name, {"fields": fields, "classes": classes}]

class ModelInlineAbstractBase(models.Model):
    TabularInline = 1
    StackedInline = 2
    TYPES = [
        (TabularInline, _("TabularInline")),
        (StackedInline, _("StackedInline")),
    ]
    
    fk_name = models.CharField(max_length=64, verbose_name=_("FK Name"))
    extra = models.IntegerField(default=0, verbose_name=_("Extra Data Number"))
    type = models.IntegerField(default=TabularInline, choices=TYPES, verbose_name=_("Inline Type"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Model Inline")
        verbose_name_plural = _("Model Inlines")
        ordering = ["order"]
        abstract = True

    def __str__(self):
        return self.fk_name

class ModelFieldAbstractBase(models.Model):
    real_field_name = models.CharField(max_length=64, verbose_name=_("Real Field Name"))
    field_widget = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Field Widget"))
    verbose_name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Verbose Name"))
    prefered_field_name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Prefered Field Name"))
    help_text = models.CharField(max_length=512, null=True, blank=True, verbose_name=_("Help Text"))
    required = models.BooleanField(default=False, verbose_name=_("Requried"))
    parameters_data = models.TextField(null=True, blank=True, verbose_name=_("Parameters"))

    class Meta:
        abstract = True
        verbose_name = _("Model Field")
        verbose_name_plural = _("Model Fields")
        unique_together = [
            ("definition", "real_field_name"),
            ("definition", "prefered_field_name"),
        ]

    @property
    def parameters(self):
        if not self.parameters_data:
            return {}
        else:
            return yaml.safe_load(self.parameters_data)

    def __str__(self):
        return self.real_field_name

class DataAbstractBase(models.Model):

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Title"))

    class Meta:
        verbose_name = _("Data")
        verbose_name_plural = _("Datas")
        abstract = True

    def __str__(self):
        return self.title or self.get_title()

    def save(self, *args, **kwargs):
        new_title = self.get_title()
        if self.title != new_title:
            self.title = new_title
        return super().save(*args, **kwargs)

    def get_title(self):
        if self.definition and self.definition.title_template:
            title = self.definition.title_template.format(model_name=self.definition.verbose_name, **self.get_prefer_named_data())
        else:
            if self.definition:
                model_name = self.definition.verbose_name
            else:
                model_name = _("Unkown Type")
            if self.pk:
                title = _("{0} (ID={1})").format(model_name, self.pk)
            else:
                title = _("{0} (Draft)").format(model_name)
        return title

    def get_prefer_named_data(self):
        map = self.definition.get_prefer_name_map()
        data = {}
        for prefer_name, real_name in map.items():
            data[prefer_name] = getattr(self, real_name, None)
        return data

    @classmethod
    def get_data_field_choices(cls):
        choices = []
        typed_choices = {}
        for field_type, field_count in cls.field_counts:
            typed_choices[field_type] = []
            choices.append((field_type, typed_choices[field_type]))
        for field_name, field_meta in cls.data_fields.items():
            field_type = field_meta["field_type"]
            typed_choices[field_type].append((field_name, field_name))
        return choices

def create_data_model(app_label, model_name, ModelDefinition, field_counts):
    kwargs = {
        "__module__": app_label + ".models",
        "definition": TreeForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="data", null=True, blank=True, verbose_name=_("Model Definition")),
        "field_counts": field_counts,
        "data_fields": {}
    }
    for field_type, field_count in field_counts:
        field_meta = FIELD_TYPES[field_type]
        for idx in range(1, field_count + 1):
            field_name = "{prefix}{idx:03d}".format(prefix=field_meta["prefix"], idx=idx)
            field = field_meta["field"]()
            kwargs[field_name] = field
            kwargs["data_fields"][field_name] = {
                "field_type": field_type,
                "field": field,
            }
    return type(model_name, (DataAbstractBase,), kwargs)

def create_model_definition(app_label):
    model_definition_kwargs = {
        "__module__": app_label + ".models",
    }
    ModelDefinition = type("ModelDefinition", (ModelDefinitionAbstractBase,), model_definition_kwargs)
    model_fieldset_kwargs = {
        "__module__": app_label + ".models",
        "definition": models.ForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="fieldsets", verbose_name=_("Definition")),
    }
    ModelFieldset = type("ModelFieldset", (ModelFieldsetAbstractBase,), model_fieldset_kwargs)
    model_inline_kwargs = {
        "__module__": app_label + ".models",
        "definition": models.ForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="inlines", verbose_name=_("Model Definition")),
        "model": TreeForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="+", verbose_name=_("Target Model Definition")),
    }
    ModelInline = type("ModelInline", (ModelInlineAbstractBase,), model_inline_kwargs)
    model_field_kwargs = {
        "__module__": app_label + ".models",
        "definition": models.ForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="fields", verbose_name=_("Definition")),
    }
    ModelField = type("ModelField", (ModelFieldAbstractBase,), model_field_kwargs)
    return ModelDefinition, ModelFieldset, ModelInline, ModelField
