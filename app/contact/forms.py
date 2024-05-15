from django import forms
from django_select2.forms import Select2Widget, ModelSelect2Widget
from .models import CRMContact, CRMCompanies
from truck.models import PostalCodeInfo


class PostalCodeSelect2Widget(ModelSelect2Widget):
    search_fields = [
        'place_name__icontains',
        'postal_code__icontains',
        'country_code__icontains'
    ]

    model = PostalCodeInfo
    queryset = PostalCodeInfo.objects.all()

    def label_from_instance(self, obj):
        return f"{obj.place_name}, {obj.postal_code}, {obj.country_code}"


class CRMContactForm(forms.ModelForm):
    address = forms.ModelChoiceField(
        queryset=PostalCodeInfo.objects.none(),
        widget=PostalCodeSelect2Widget,
        required=False,
        label="Address",
        initial='',  # Устанавливаем начальное значение на пустое
    )

    class Meta:
        model = CRMContact
        fields = '__all__'


class CRMCompanyForm(forms.ModelForm):
    address = forms.ChoiceField(
        widget=Select2Widget
    )

    class Meta:
        model = CRMCompanies
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CRMCompanyForm, self).__init__(*args, **kwargs)
        self.fields['address'].choices = [
            (postal.id, f"{postal.place_name}, {postal.postal_code}, {postal.country_code}")
            for postal in PostalCodeInfo.objects.all()
        ]

# class CRMContactForm(forms.ModelForm):
#     class Meta:
#         model = CRMContact
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super(CRMContactForm, self).__init__(*args, **kwargs)
#         self.fields['address'].choices = [
#             (postal.place_name, f"{postal.place_name}, {postal.postal_code}, {postal.country_code}")
#             for postal in PostalCodeInfo.objects.all()
#         ]
