from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_appointment.form_validators import AppointmentFormValidator
from ..models import Appointment


class FacetAppointmentForm(SiteModelFormMixin, FormValidatorMixin,
                           AppointmentFormValidator, forms.ModelForm):

    class Meta:
        model = Appointment
        fields = '__all__'
