from django.apps import apps as django_apps
from django.core.exceptions import ValidationError

from edc_base.utils import age, get_utcnow
from edc_constants.choices import NO, YES
from edc_form_validators import FormValidator


class ChildSocioDemographicFormValidator(FormValidator):
    child_caregiver_consent_model = 'flourish_caregiver.caregiverchildconsent'

    maternal_delivery_model = 'flourish_caregiver.maternaldelivery'

    caregiver_socio_demographic_model = 'flourish_caregiver.sociodemographicdata'

    child_assent_model = 'flourish_child.childassent'

    @property
    def caregiver_socio_demographic_cls(self):
        return django_apps.get_model(self.caregiver_socio_demographic_model)

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'facet_visit').appointment.subject_identifier
        super().clean()

        self.validate_other_specify(field='ethnicity')
        self.validate_other_specify(field='toilet_facility')

        self.validate_child_not_schooling()

        self.validate_other_specify(field='education_level')
        self.validate_number_of_people_living_in_the_household()

    @property
    def caregiver_subject_identifier(self):
        subject_identifier = self.subject_identifier.split('-')
        subject_identifier.pop()
        caregiver_subject_identifier = '-'.join(subject_identifier)
        return caregiver_subject_identifier

    def validate_number_of_people_living_in_the_household(self):
        """Validate the number of people living in the household"""
        msg = None
        older_than18 = self.cleaned_data.get('older_than18')
        house_people_number = self.cleaned_data.get('house_people_number')
        if older_than18 and house_people_number:
            if older_than18 > house_people_number:
                msg = {'older_than18':
                       f'Number of people ({older_than18}) who are older than 18 '
                       f'and live in the household cannot be more than the total '
                       f'number ({house_people_number}) of people living in the '
                       f'household'}
            elif older_than18 == house_people_number:
                msg = {'older_than18':
                       f'Number of people ({older_than18}) who are older than 18 '
                       f'and live in the household cannot be equal to the total '
                       f'number ({house_people_number}) of people living in the '
                       f'household'}
        if msg:
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_child_not_schooling(self):
        attend_school = self.cleaned_data.get('attend_school')

        if (attend_school == YES and
                self.cleaned_data.get('education_level') == 'no_schooling'):
            msg = {'education_level':
                   'This child is said to be attending school, Please specify '
                   'education level.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        if (attend_school == NO and
                self.cleaned_data.get('education_level') != 'no_schooling'):
            msg = {'education_level':
                   'This child is not attending school, Please specify '
                   'education level as `No schooling` to indicate this.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        self.applicable_if(
            YES,
            field='attend_school',
            field_applicable='school_type')

        self.applicable_if_true(
            self.child_age > 16 and attend_school == NO,
            field='attend_school',
            field_applicable='working')

    @property
    def child_assent_obj(self):
        child_assent_model_cls = django_apps.get_model(self.child_assent_model)

        child_assent_objs = child_assent_model_cls.objects.filter(
            subject_identifier=self.subject_identifier)

        if child_assent_objs:
            return child_assent_objs.latest('consent_datetime')

    @property
    def child_caregiver_consent_obj(self):
        child_caregiver_consent_model_cls = django_apps.get_model(
            self.child_caregiver_consent_model)

        child_caregiver_consen_objs = child_caregiver_consent_model_cls.objects.filter(
            subject_identifier=self.subject_identifier)

        if child_caregiver_consen_objs:
            return child_caregiver_consen_objs.latest('consent_datetime')

    @property
    def maternal_delivery_obj(self):
        maternal_delivery_model_cls = django_apps.get_model(
            self.maternal_delivery_model)
        try:
            model_obj = maternal_delivery_model_cls.objects.get(
                subject_identifier__istartswith=self.subject_identifier)
        except maternal_delivery_model_cls.DoesNotExist:
            return None
        else:
            return model_obj

    @property
    def child_age(self):
        if self.child_assent_obj:
            birth_date = self.child_assent_obj.dob
            years = age(birth_date, get_utcnow()).years
            return years
        elif self.child_caregiver_consent_obj:
            birth_date = self.child_caregiver_consent_obj.child_dob
            years = age(birth_date, get_utcnow()).years
            return years
        elif self.maternal_delivery_obj:
            birth_date = self.maternal_delivery_obj.delivery_datetime.date()
            years = age(birth_date, get_utcnow()).months
            return years
        return 0
