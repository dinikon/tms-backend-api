from django.contrib import admin
from django import forms
from django.db import models
from django.forms import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from contact.forms import CRMContactForm
from .models import (
    CRMTrucks, CRMCrossBorder, CRMCertificate, CRMDimensions, CRMTruckNotes, CRMTruckLocations
)


class CrossBorderFilter(admin.SimpleListFilter):
    title = _('cross border')
    parameter_name = 'cross_border'

    def lookups(self, request, model_admin):
        # Список значений, которые могут быть выбраны в фильтре
        cross_borders = CRMCrossBorder.objects.all()
        return [(cb.id, cb.name) for cb in cross_borders]

    def queryset(self, request, queryset):
        # Фильтрация queryset на основе выбранного значения
        if self.value():
            return queryset.filter(cross_borders__id=self.value())
        return queryset


class CertificateFilter(admin.SimpleListFilter):
    title = _('Certificate')
    parameter_name = 'Certificate'

    def lookups(self, request, model_admin):
        # Список значений, которые могут быть выбраны в фильтре
        cross_borders = CRMCertificate.objects.all()
        return [(cb.id, cb.name) for cb in cross_borders]

    def queryset(self, request, queryset):
        # Фильтрация queryset на основе выбранного значения
        if self.value():
            return queryset.filter(cross_borders__id=self.value())
        return queryset


class CrmDimensionsInline(admin.StackedInline):
    model = CRMDimensions
    extra = 1  # Количество пустых форм для новых записей


class CrmTruckLocationsInline(admin.TabularInline):
    model = CRMTruckLocations
    form = CRMContactForm
    fields = ('address', 'created_at', 'created_by')
    readonly_fields = ('created_at', 'created_by')
    extra = 1  # Количество пустых форм для новых записей


class CrmNotesInline(admin.TabularInline):
    model = CRMTruckNotes
    extra = 1  # Количество пустых форм для новых записей
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 80})},
    }

    fields = ('note', 'created_by')  # `created_by` и `modify_by` не указываются здесь, чтобы не отображались в форме
    readonly_fields = ('created_by', )  # Сделаем все поля доступными для редактирования

    def get_formset(self, request, obj=None, **kwargs):
        class CrmNotesInlineFormset(BaseInlineFormSet):
            def save_new(self, form, commit=True):
                instance = form.save(commit=False)
                instance.created_by = request.user
                if commit:
                    instance.save()
                return instance

            def save_existing(self, form, instance, commit=True):
                instance = form.save(commit=False)
                instance.modify_by = request.user
                if commit:
                    instance.save()
                return instance

        kwargs['formset'] = CrmNotesInlineFormset
        return super().get_formset(request, obj, **kwargs)


class CrmTruckAdmin(admin.ModelAdmin):
    list_display = ('number', 'license_plate', 'make', 'model', 'year', 'is_deleted')
    search_fields = ['number', 'license_plate', 'make', 'model']
    fieldsets = (
        (None, {'fields': ('number', 'owner')}),
        ('Truck Details', {'fields': ('truck_type', 'trailer_type', 'make', 'model', 'year')}),
        ('Registration Information', {'fields': ('vincode', 'license_plate', 'license_state', 'registration_expiration', 'insurance_expiration')}),
    )
    list_filter = (CrossBorderFilter, CertificateFilter, 'make', 'model', 'year', 'is_deleted')
    inlines = [CrmDimensionsInline, CrmTruckLocationsInline, CrmNotesInline]


admin.site.register(CRMTrucks, CrmTruckAdmin)
