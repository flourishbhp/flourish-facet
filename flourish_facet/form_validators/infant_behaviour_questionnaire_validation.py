from edc_form_validators import FormValidator
from django.apps import apps as django_apps
import pytz
from django.core.exceptions import ValidationError
from flourish_child_validations.utils import caregiver_subject_identifier
from edc_constants.constants import YES


class InfantBehaviourQuestionnaireFormValidator(FormValidator):

    maternal_del_model = 'flourish_caregiver.maternaldelivery'

    @property
    def maternal_del_cls(self):
        return django_apps.get_model(self.maternal_del_model)

    def clean(self):
        self.validate_dob()
        self.applicable_if(YES, field='take_outside',
                           field_applicable='talking_sound')
        super().clean()

    def validate_dob(self):
        cleaned_data = self.cleaned_data
        self.subject_identifier = self.cleaned_data.get(
            'facet_visit').appointment.subject_identifier

        try:
            maternal_lab_del = self.maternal_del_cls.objects.get(
                child_subject_identifier=self.subject_identifier)
        except self.maternal_del_cls.DoesNotExist:
            raise ValidationError(
                'Cannot find maternal labour and delivery '
                'form for this infant! This is not expected.')
        else:
            dob = cleaned_data.get('dob')  # already a date
            delivery_datetime = maternal_lab_del.delivery_datetime  # date + utc time
            local_tz = pytz.timezone('Africa/Gaborone')  # get our zone
            local_delivery_datetime = delivery_datetime.astimezone(
                local_tz)  # convert to CAT

            if dob != local_delivery_datetime.date():
                # Get date only and remove the time fraction

                msg = {'dob':
                       'Infant dob must match maternal delivery date. Expected'
                       f' {maternal_lab_del.delivery_datetime.date()}, '
                       f'got {dob}'}
                self._errors.update(msg)
                raise ValidationError(msg)
