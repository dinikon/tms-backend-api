from django import forms
from django_select2.forms import Select2Widget
from .models import CRMContact, CRMCompanies
from truck.models import PostalCodeInfo


class CRMContactForm(forms.ModelForm):
    address = forms.ChoiceField(
        widget=Select2Widget(),
        required=False,  # Указываем, что поле необязательное
        label="Address",
        initial='',  # Устанавливаем начальное значение на пустое
    )

    class Meta:
        model = CRMContact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CRMContactForm, self).__init__(*args, **kwargs)
        # Сначала добавляем пустой выбор
        empty_choice = [('', '--- Select ---')]
        postal_choices = [
            (postal.id, f"{postal.place_name}, {postal.postal_code}, {postal.country_code}")
            for postal in PostalCodeInfo.objects.all()
        ]
        self.fields['address'].choices = empty_choice + postal_choices


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
