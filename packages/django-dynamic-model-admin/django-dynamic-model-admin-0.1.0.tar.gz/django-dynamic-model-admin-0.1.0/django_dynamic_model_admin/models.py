import functools
import json
from fastutils import strutils
from django.db import models
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


class FieldWidget(models.Model):
    field_type = models.CharField(max_length=64, verbose_name=_("Field Type"))
    name = models.CharField(max_length=64, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Field Widget")
        verbose_name_plural = _("Field Widgets")

    def __str__(self):
        return self.name

class ModelDefinitionCategory(MPTTModel):
    parent = TreeForeignKey("self", on_delete=models.CASCADE, related_name="children", null=True, blank=True, verbose_name=_("Model Definition Category Parent"))
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = _("Model Definition Category")
        verbose_name_plural = _("Model Definition Categories")

    def __str__(self):
        return self.name

    def indented_title(self):
        return ("-"*4) * self.get_level() + self.name


class ModelDefinition(models.Model):
    parent = TreeForeignKey(ModelDefinitionCategory, on_delete=models.CASCADE, related_name="definitions", null=True, blank=True, verbose_name=_("Model Definition Category"))
    name = models.CharField(max_length=64, verbose_name=_("Name"), unique=True)
    verbose_name = models.CharField(max_length=64, verbose_name=_("Verbose Name"))
    verbose_name_plural = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Verbose Name Plural"))
    title_template = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Title Template"))
    label_width = models.CharField(max_length=32, null=True, blank=True, verbose_name=_("Label Width"), help_text=_("Add unit, e.g. 120px"))

    class Meta:
        verbose_name = _("Model Definition")
        verbose_name_plural = _("Model Definitions")

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

class ModelFieldset(models.Model):
    definition = models.ForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="fieldsets", verbose_name=_("Definition"))
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Name"))
    fields = models.TextField(null=True, blank=True, verbose_name=_("Fields"))
    classes = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Classes"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Model Fieldset")
        verbose_name_plural = _("Model Fieldsets")
        ordering = ["order"]

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

class ModelInline(models.Model):
    TabularInline = 1
    StackedInline = 2
    TYPES = [
        (TabularInline, _("TabularInline")),
        (StackedInline, _("StackedInline")),
    ]
    definition = models.ForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="inlines", verbose_name=_("Model Definition"))
    model = models.ForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="+", verbose_name=_("Target Model Definition"))
    fk_name = models.CharField(max_length=64, verbose_name=_("FK Name"))
    extra = models.IntegerField(default=0, verbose_name=_("Extra Data Number"))
    type = models.IntegerField(default=TabularInline, choices=TYPES, verbose_name=_("Inline Type"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Model Inline")
        verbose_name_plural = _("Model Inlines")
        ordering = ["order"]

    def __str__(self):
        return self.fk_name

class ModelField(models.Model):
    definition = models.ForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="fields", verbose_name=_("Definition"))
    real_field_name = models.CharField(max_length=64, verbose_name=_("Real Field Name"))
    field_type = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Field Type"))
    field_widget = models.ForeignKey(FieldWidget, on_delete=models.SET_NULL, null=True, blank=True, related_name="+", verbose_name=_("Field Widget"))
    verbose_name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Verbose Name"))
    prefered_field_name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Prefered Field Name"))
    help_text = models.CharField(max_length=512, null=True, blank=True, verbose_name=_("Help Text"))
    required = models.BooleanField(default=False, verbose_name=_("Requried"))

    class Meta:
        verbose_name = _("Model Field")
        verbose_name_plural = _("Model Fields")
        unique_together = [
            ("definition", "real_field_name"),
            ("definition", "prefered_field_name"),
        ]


class Data(models.Model):
    md = models.ForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="data", null=True, blank=True, verbose_name=_("Model Definition"))
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Title"))
    f01 = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    f02 = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    f03 = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    f04 = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    f05 = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    f06 = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    f07 = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    f08 = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    f09 = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    f10 = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    c01 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c02 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c03 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c04 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c05 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c06 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c07 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c08 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c09 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c10 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c11 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c12 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c13 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c14 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c15 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c16 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c17 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c18 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c19 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    c20 = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    i01 = models.IntegerField(null=True, blank=True, db_index=True)
    i02 = models.IntegerField(null=True, blank=True, db_index=True)
    i03 = models.IntegerField(null=True, blank=True, db_index=True)
    i04 = models.IntegerField(null=True, blank=True, db_index=True)
    i05 = models.IntegerField(null=True, blank=True, db_index=True)
    i06 = models.IntegerField(null=True, blank=True, db_index=True)
    i07 = models.IntegerField(null=True, blank=True, db_index=True)
    i08 = models.IntegerField(null=True, blank=True, db_index=True)
    i09 = models.IntegerField(null=True, blank=True, db_index=True)
    i10 = models.IntegerField(null=True, blank=True, db_index=True)
    i11 = models.IntegerField(null=True, blank=True, db_index=True)
    i12 = models.IntegerField(null=True, blank=True, db_index=True)
    i13 = models.IntegerField(null=True, blank=True, db_index=True)
    i14 = models.IntegerField(null=True, blank=True, db_index=True)
    i15 = models.IntegerField(null=True, blank=True, db_index=True)
    i16 = models.IntegerField(null=True, blank=True, db_index=True)
    i17 = models.IntegerField(null=True, blank=True, db_index=True)
    i18 = models.IntegerField(null=True, blank=True, db_index=True)
    i19 = models.IntegerField(null=True, blank=True, db_index=True)
    i20 = models.IntegerField(null=True, blank=True, db_index=True)
    d01 = models.DateTimeField(null=True, blank=True, db_index=True)
    d02 = models.DateTimeField(null=True, blank=True, db_index=True)
    d03 = models.DateTimeField(null=True, blank=True, db_index=True)
    d04 = models.DateTimeField(null=True, blank=True, db_index=True)
    d05 = models.DateTimeField(null=True, blank=True, db_index=True)
    d06 = models.DateTimeField(null=True, blank=True, db_index=True)
    d07 = models.DateTimeField(null=True, blank=True, db_index=True)
    d08 = models.DateTimeField(null=True, blank=True, db_index=True)
    d09 = models.DateTimeField(null=True, blank=True, db_index=True)
    d10 = models.DateTimeField(null=True, blank=True, db_index=True)
    t01 = models.TextField(null=True, blank=True, db_index=True)
    t02 = models.TextField(null=True, blank=True, db_index=True)
    t03 = models.TextField(null=True, blank=True, db_index=True)
    t04 = models.TextField(null=True, blank=True, db_index=True)
    t05 = models.TextField(null=True, blank=True, db_index=True)
    t06 = models.TextField(null=True, blank=True, db_index=True)
    t07 = models.TextField(null=True, blank=True, db_index=True)
    t08 = models.TextField(null=True, blank=True, db_index=True)
    t09 = models.TextField(null=True, blank=True, db_index=True)
    t10 = models.TextField(null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = _("Data")
        verbose_name_plural = _("Datas")

    def __str__(self):
        return self.title or self.get_title()

    def save(self, *args, **kwargs):
        new_title = self.get_title()
        if self.title != new_title:
            self.title = new_title
        return super().save(*args, **kwargs)

    def get_title(self):
        if self.md and self.md.title_template:
            title = self.md.title_template.format(model_name=self.md.verbose_name, **self.get_prefer_named_data())
        else:
            if self.md:
                model_name = self.md.verbose_name
            else:
                model_name = _("Unkown Type")
            if self.pk:
                title = _("{0} (ID={1})").format(model_name, self.pk)
            else:
                title = _("{0} (Draft)").format(model_name)
        return title

    def get_prefer_named_data(self):
        map = self.md.get_prefer_name_map()
        data = {}
        for prefer_name, real_name in map.items():
            data[prefer_name] = getattr(self, real_name, None)
        return data


FIELD_TYPES = {
    "CharField": lambda : models.CharField(max_length=4096, null=True, blank=True, db_index=True),
    "IntegerField": lambda : models.IntegerField(null=True, blank=True, db_index=True),
    "TextField": lambda: models.TextField(null=True, blank=True, db_index=True),
    "DateField": lambda: models.DateField(null=True, blank=True, db_index=True),
    "DateTimeField": lambda: models.DateTimeField(null=True, blank=True, db_index=True),
    "ForeignKey": lambda: models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"),
    "DecimalField": lambda: models.DecimalField(max_digits=19, decimal_places=6, db_index=True),
}

def get_field_type_choices():
    return sorted([
        (x, x) for x in FIELD_TYPES.keys()
    ])
