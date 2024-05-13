from django.db import models
from django.conf import settings
from django.utils.timezone import now


class CRMContact(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_contacts',
                                      on_delete=models.CASCADE, null=True, blank=True)
    modify_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='modified_contacts',
                                     on_delete=models.CASCADE, null=True, blank=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='assigned_contacts')
    opened = models.BooleanField(null=True, blank=True)
    company_id = models.BigIntegerField(null=True, blank=True)
    source_id = models.BooleanField(null=True, blank=True)
    source_description = models.TextField(null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    second_name = models.CharField(max_length=255, null=True, blank=True)
    post = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    lead_id = models.BigIntegerField(null=True, blank=True)
    export = models.BooleanField(null=True, blank=True)
    type_id = models.BigIntegerField(null=True, blank=True)
    originator_id = models.BigIntegerField(null=True, blank=True)
    origin_id = models.BigIntegerField(null=True, blank=True)
    origin_version = models.BigIntegerField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    search_content = models.TextField(null=True, blank=True)
    category_id = models.BigIntegerField(null=True, blank=True)
    last_activity_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='last_activity_contacts')
    last_activity_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'crm_contacts'
        verbose_name = "Contact (Driver)"
        verbose_name_plural = "Contacts (Drivers)"

    def __str__(self):
        return self.full_name or ""

    def save(self, *args, **kwargs):
        if not self.pk:  # This checks if this is a new instance being created
            self.created_at = now()
            if hasattr(self, '_created_by'):
                self.created_by_id = self._created_by
        else:
            self.updated_at = now()
            if hasattr(self, '_modified_by'):
                self.modify_by_id = self._modified_by

        parts = [self.first_name, self.second_name, self.last_name]
        self.full_name = ' '.join(filter(None, parts))
        super(CRMContact, self).save(*args, **kwargs)


class CRMContactFields(models.Model):
    VALUE_TYPE_CHOICES = (
        ('Phone', 'Phone'),
        ('Email', 'Email'),
    )
    contact_id = models.ForeignKey(CRMContact, on_delete=models.CASCADE, related_name='contact_fields')
    type_id = models.CharField(max_length=255, choices=VALUE_TYPE_CHOICES, null=True, blank=True)
    value_type = models.CharField(max_length=255, default='WORK', null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'crm_contact_fields'


class CRMCompanies(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='companies_created',
        null=True, blank=True
    )
    modify_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='companies_modified',
        null=True, blank=True
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='companies_assigned',
        null=True, blank=True
    )
    opened = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    # logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    address_legals = models.TextField(null=True, blank=True)
    banking_details = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    company_type = models.IntegerField(null=True, blank=True)
    industry = models.IntegerField(null=True, blank=True)
    revenue = models.BigIntegerField(null=True, blank=True)
    currency_id = models.IntegerField(null=True, blank=True)
    employees = models.IntegerField(null=True, blank=True)
    lead_id = models.IntegerField(null=True, blank=True)
    webform_id = models.IntegerField(null=True, blank=True)
    originator_id = models.IntegerField(null=True, blank=True)
    origin_id = models.IntegerField(null=True, blank=True)
    origin_version = models.IntegerField(null=True, blank=True)
    has_phone = models.BooleanField(default=False)
    has_email = models.BooleanField(default=False)
    has_imol = models.BooleanField(default=False)
    search_content = models.TextField(null=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    last_activity_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='companies_last_activity_by',
        null=True, blank=True
    )
    last_activity_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'crm_companies'
        verbose_name = "Company (Owner)"
        verbose_name_plural = "Companies (Owners)"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = now()
            if hasattr(self, '_created_by'):
                self.created_by_id = self._created_by
        else:
            self.updated_at = now()
            if hasattr(self, '_modified_by'):
                self.modify_by_id = self._modified_by

        super(CRMCompanies, self).save(*args, **kwargs)


class CRMContactCompany(models.Model):
    contact = models.ForeignKey(
        CRMContact,
        on_delete=models.CASCADE,
        related_name='company_relations'
    )
    company = models.ForeignKey(
        CRMCompanies,
        on_delete=models.CASCADE,
        related_name='contact_relations'
    )
    sort_by = models.SmallIntegerField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'crm_contact_company_relations'
        unique_together = ('contact', 'company')

    def save(self, *args, **kwargs):
        if self.is_primary:
            CRMContactCompany.objects.filter(company=self.company).update(is_primary=False)
            self.is_primary = True
        super().save(*args, **kwargs)

    def __str__(self):
        primary_status = "Primary" if self.is_primary else "Secondary"
        return f"{self.contact} - {self.company} ({primary_status})"


class CRMContactDrivers(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('Approve', 'Approve'),
        ('Decline', 'Decline'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_contact_drivers',
                                      on_delete=models.CASCADE, null=True, blank=True)
    modify_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='modified_contact_drivers',
                                     on_delete=models.CASCADE, null=True, blank=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='assigned_drivers')
    contact = models.OneToOneField(CRMContact, on_delete=models.CASCADE, related_name='contact_drivers')
    search_content = models.TextField(null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, null=True, blank=True)
    licence_type = models.CharField(max_length=255, null=True, blank=True)
    licence_number = models.CharField(max_length=255, null=True, blank=True)
    licence_state = models.CharField(max_length=15, null=True, blank=True)
    expiration = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'crm_contact_drivers'
        verbose_name = "Driver Information"
        verbose_name_plural = "Drivers Information"

    def __str__(self):
        return f"CRM Contact Driver {self.pk}"

    def save(self, *args, **kwargs):
        if not self.pk:  # This checks if this is a new instance being created
            self.created_at = now()
            if hasattr(self, '_created_by'):
                self.created_by_id = self._created_by
        else:
            self.updated_at = now()
            if hasattr(self, '_modified_by'):
                self.modify_by_id = self._modified_by

        super(CRMContactDrivers, self).save(*args, **kwargs)


class CRMContactDriverEC(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='crmcontactdriverec_created'
    )
    modify_by_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='crmcontactdriverec_modified'
    )
    assigned_by_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='crmcontactdriverec_assigned'
    )
    opened = models.BooleanField(default=False)
    contact_id = models.ForeignKey(
        CRMContact,
        on_delete=models.CASCADE,
        related_name='driver_ec_contacts'
    )
    ec_name = models.CharField(max_length=255)
    ec_phone = models.CharField(max_length=50)
    ec_email = models.EmailField()
    relationship = models.CharField(max_length=100)

    class Meta:
        db_table = 'crm_contact_driver_ec'
        verbose_name = "Driver Emergency Contact"
        verbose_name_plural = "Drivers Emergency Contact"

    def __str__(self):
        return f"Emergency Contact {self.ec_name} for Contact ID {self.contact_id}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = now()
            if hasattr(self, '_created_by'):
                self.created_by_id = self._created_by
        else:
            self.updated_at = now()
            if hasattr(self, '_modified_by'):
                self.modify_by_id = self._modified_by

        super(CRMContactDriverEC, self).save(*args, **kwargs)