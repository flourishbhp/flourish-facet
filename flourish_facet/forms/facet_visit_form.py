from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from ..models import FacetVisit
from ..form_validators import FacetVisitFormValidator


class FacetVisitForm(SiteModelFormMixin,
                     FormValidatorMixin,
                     forms.ModelForm):

    form_validator_cls = FacetVisitFormValidator

    class Meta:
        model = FacetVisit
        fields = '__all__'
