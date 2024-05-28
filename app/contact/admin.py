from django.contrib import admin

from .models import CRMContact, CRMContactFields, CRMContactCompany, CRMCompanies, CRMContactDrivers, CRMContactDriverEC
from django.contrib.auth import get_user_model


User = get_user_model()


class CRMContactDriversEcInline(admin.TabularInline):
    model = CRMContactDriverEC
    fields = ('ec_name', 'ec_phone', 'ec_email', 'relationship')

    def get_formset(self, request, obj=None, **kwargs):
        if obj:
            count = obj.contact_fields.count()
            if count == 0:
                self.extra = 1
            else:
                self.extra = 0
        return super().get_formset(request, obj, **kwargs)
    # readonly_fields = ('value_type',)  # Optional: make some fields read-only


class CRMContactDriversInline(admin.TabularInline):
    model = CRMContactDrivers
    fields = ('hire_date', 'status', 'licence_type', 'licence_number', 'licence_state', 'expiration')

    def get_formset(self, request, obj=None, **kwargs):
        if obj:
            count = obj.contact_fields.count()
            if count == 0:
                self.extra = 1
            else:
                self.extra = 0
        return super().get_formset(request, obj, **kwargs)
    # readonly_fields = ('value_type',)  # Optional: make some fields read-only


class CRMContactInline(admin.TabularInline):
    model = CRMContactFields
    fields = ('type_id', 'value')

    def get_formset(self, request, obj=None, **kwargs):
        if obj:
            count = obj.contact_fields.count()
            if count == 0:
                self.extra = 1
            else:
                self.extra = 0
        return super().get_formset(request, obj, **kwargs)
    # readonly_fields = ('value_type',)  # Optional: make some fields read-only


class CRMContactInline(admin.TabularInline):
    model = CRMContactFields
    fields = ('type_id', 'value')

    def get_formset(self, request, obj=None, **kwargs):
        if obj:
            count = obj.contact_fields.count()
            if count == 0:
                self.extra = 1
            else:
                self.extra = 0
        return super().get_formset(request, obj, **kwargs)
    # readonly_fields = ('value_type',)  # Optional: make some fields read-only


class CRMContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company_id', 'assigned_to', 'created_by_user', 'last_activity_time', 'opened_status')
    list_filter = ('opened', 'created_at', 'updated_at', 'assigned_by', 'created_by')
    search_fields = ('full_name', 'first_name', 'last_name', 'address', 'comments')
    readonly_fields = ('created_at', 'updated_at', 'created_by_user', 'modify_by_user', 'last_activity_by')
    inlines = [CRMContactInline, CRMContactDriversInline, CRMContactDriversEcInline]

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'second_name')}),
        ('Contact Details', {'fields': ('address', 'birthdate', 'comments')}),
        ('Company and Assignment', {'fields': ('assigned_by', 'type_id', 'category_id')}),
        ('System Information', {'fields': (
        'created_at', 'updated_at', 'created_by_user', 'modify_by_user', 'last_activity_by')}),
    )

    def opened_status(self, obj):
        return "Opened" if obj.opened else "Not Opened"
    opened_status.short_description = 'Opened Status'

    def assigned_to(self, obj):
        return obj.assigned_by.username if obj.assigned_by_id else None
    assigned_to.short_description = 'Assigned To'

    def created_by_user(self, obj):
        return obj.created_by.username if obj.created_by_id else None
    created_by_user.short_description = 'Created By'

    def modify_by_user(self, obj):
        return obj.modify_by.username if obj.modify_by_id else None
    modify_by_user.short_description = 'Last Modified By'

    def get_queryset(self, request):
        """Изменение queryset для отображения только контактов с type_id равным 2."""
        qs = super().get_queryset(request)
        # Фильтрация queryset по type_id
        return qs.filter(category_id=1)

    def save_model(self, request, obj, form, change):
        obj.last_activity_by = request.user
        # obj.last_activity_time = timezone.now()
        if not obj.id:
            obj.created_by = request.user
            obj.category_id = 1
        else:
            obj.modify_by = request.user
            obj.category_id = 1
        super().save_model(request, obj, form, change)


class CRMContactCompanyInline(admin.TabularInline):
    model = CRMContactCompany
    extra = 1  # Количество форм для новых записей
    autocomplete_fields = ['contact']  # Добавление автозаполнения для поля контакта, если у вас много контактов

    def get_formset(self, request, obj=None, **kwargs):
        if obj:
            # Подсчитываем количество связанных объектов
            count = obj.contact_relations.count()
            if count == 0:
                self.extra = 1
            else:
                self.extra = 0
        return super().get_formset(request, obj, **kwargs)


class CRMCompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'created_by')
    # list_filter = ('opened', 'created_at', 'updated_at', 'assigned_by', 'created_by')
    # search_fields = ('full_name', 'first_name', 'last_name', 'address', 'comments')
    # readonly_fields = (
    # 'created_at', 'updated_at', 'created_by_user', 'modify_by_user', 'last_activity_by', 'last_activity_time')

    fieldsets = (
        (None, {'fields': ('title', 'address', 'address_legals', 'assigned_by')}),
        # ('Contact Details', {'fields': ('address', 'birthdate', 'comments')}),
        # ('Company and Assignment', {'fields': ('assigned_by_id', 'type_id', 'category_id')}),
        # ('System Information', {'fields': (
        # 'created_at', 'updated_at', 'created_by_user', 'modify_by_user', 'last_activity_by', 'last_activity_time')}),
    )
    inlines = [CRMContactCompanyInline]

    def get_queryset(self, request):
        """Изменение queryset для отображения только контактов с type_id равным 2."""
        qs = super().get_queryset(request)
        # Фильтрация queryset по type_id
        return qs.filter(category_id=1)

    def save_model(self, request, obj, form, change):
        obj.last_activity_by = request.user
        # obj.last_activity_time = timezone.now()
        if not obj.id:
            obj.created_by = request.user
            obj.category_id = 1
        else:
            obj.modify_by = request.user
            obj.category_id = 1
        super().save_model(request, obj, form, change)


admin.site.register(CRMContact, CRMContactAdmin)
admin.site.register(CRMCompanies, CRMCompanyAdmin)


