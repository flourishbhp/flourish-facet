from django import forms
from edc_form_validators import FormValidatorMixin
from ...form_validators import FacetCaregiverContactFormValidator

from ...models import FacetCaregiverContact


class FacetCaregiverContactForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = FacetCaregiverContactFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = FacetCaregiverContact
        fields = '__all__'
