from django.db import models
from django.conf import settings
from django.utils.timezone import now

from contact.models import CRMCompanies
from contact.models import CRMContact


class PostalCodeInfo(models.Model):
    country_code = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=20)
    place_name = models.CharField(max_length=100)
    admin_name1 = models.CharField(max_length=100)
    admin_code1 = models.CharField(max_length=20)
    admin_name2 = models.CharField(max_length=100, null=True, blank=True)
    admin_code2 = models.CharField(max_length=20, null=True, blank=True)
    admin_name3 = models.CharField(max_length=100, null=True, blank=True)
    admin_code3 = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    accuracy = models.IntegerField(null=True, blank=True)
    coordinates = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.place_name}, {self.postal_code}, {self.country_code}"

    class Meta:
        db_table = 'crm_dic_postal_code_info'
        verbose_name = "Postal Code Information"
        verbose_name_plural = "Postal Codes Information"


# Модель для Cross Border
class CRMCrossBorder(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'crm_cross_border'


# Модель для Certificates
class CRMCertificate(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'crm_certificate'


# Модель для Preferred Loads
class CRMPreferredLoad(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'crm_preferred_load'


# Модель для Trucks
class CRMTrucks(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_trucks',
                                   on_delete=models.CASCADE, null=True, blank=True)
    modify_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='modified_trucks',
                                  on_delete=models.CASCADE, null=True, blank=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_trucks')
    opened = models.BooleanField(null=True, blank=True)
    status = models.CharField(max_length=255, default='New')
    owner = models.ForeignKey(CRMCompanies, on_delete=models.SET_NULL, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    license_plate = models.CharField(max_length=255, null=True, blank=True)
    license_state = models.CharField(max_length=255, null=True, blank=True)
    vincode = models.CharField(max_length=255, null=True, blank=True)
    make = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    truck_type = models.CharField(max_length=255, null=True, blank=True)
    trailer_type = models.CharField(max_length=255, null=True, blank=True)
    door_type = models.CharField(max_length=255, null=True, blank=True)
    is_reefer = models.BooleanField(null=True, blank=True)
    is_deleted = models.BooleanField(null=True, blank=True)
    company_signs = models.BooleanField(null=True, blank=True)
    is_owner_coordinator_responsible = models.BooleanField(null=True, blank=True)
    responsible = models.CharField(max_length=255, null=True, blank=True)
    current_travel_order_number = models.CharField(max_length=255, null=True, blank=True)
    hired_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    crm_id = models.IntegerField(null=True, blank=True)
    cross_borders = models.ManyToManyField(CRMCrossBorder)
    certificates = models.ManyToManyField(CRMCertificate)
    preferred_loads = models.ManyToManyField(CRMPreferredLoad)
    registration_expiration = models.DateField(null=True, blank=True)
    insurance_expiration = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = now()
            if hasattr(self, '_created_by'):
                self.created_by_id = self._created_by
        else:
            self.updated_at = now()
            if hasattr(self, '_modified_by'):
                self.modify_by_id = self._modified_by

        super(CRMTrucks, self).save(*args, **kwargs)

    class Meta:
        db_table = 'crm_trucks'


class CRMDimensions(models.Model):
    dimensions_id = models.AutoField(primary_key=True)
    truck = models.OneToOneField(CRMTrucks, on_delete=models.CASCADE, null=True, blank=True, related_name='dimensions')
    door_dims_height = models.FloatField(null=True, blank=True)
    inside_dims_width = models.FloatField(null=True, blank=True)
    inside_dims_height = models.FloatField(null=True, blank=True)
    inside_dims_length = models.FloatField(null=True, blank=True)
    valid_dims_width = models.FloatField(null=True, blank=True)
    valid_dims_height = models.FloatField(null=True, blank=True)
    valid_dims_length = models.FloatField(null=True, blank=True)
    dims_units = models.CharField(max_length=50, null=True, blank=True)
    payload = models.FloatField(null=True, blank=True)
    payload_units = models.CharField(max_length=50, null=True, blank=True)
    door_dims_width = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'crm_dimensions'


class CRMTruckNotes(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_truck_notes',
                                   on_delete=models.CASCADE, null=True, blank=True)
    modify_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='modified_truck_notes',
                                  on_delete=models.CASCADE, null=True, blank=True)
    truck = models.ForeignKey(CRMTrucks, on_delete=models.CASCADE, related_name='crmtrucknotes_set')
    note = models.TextField()

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_at = now()
            if hasattr(self, '_created_by'):
                self.created_by_id = self._created_by
        else:
            self.updated_at = now()
            if hasattr(self, '_modified_by'):
                self.modify_by_id = self._modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'crm_truck_notes'


class CRMTruckLocations(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_truck_locations',
                                   on_delete=models.CASCADE, null=True, blank=True)
    truck = models.ForeignKey(CRMTrucks, on_delete=models.CASCADE, related_name='crmtrucklocations_set')
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'crm_truck_locations'
