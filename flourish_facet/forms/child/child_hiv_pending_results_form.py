from django import forms
from ...form_validators.child_hiv_pending_results_validation import ChildHivPendingResultsFormValidator
from ...models import ChildHivPendingResults
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from django.apps import apps as django_apps


class ChildHivPendingResultsForm(FormValidatorMixin, SiteModelFormMixin, forms.ModelForm):
    form_validator_cls = ChildHivPendingResultsFormValidator
    child_hiv_testing_model = 'flourish_facet.childhivtesting'

    @property
    def child_hiv_testing_model_cls(self):
        return django_apps.get_model(self.child_hiv_testing_model)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        subject_identifier = self.initial.get('subject_identifier', None)

        if subject_identifier:
            child_hiv_testing_obj = self.child_hiv_testing_model_cls.objects.filter(
                facet_visit__subject_identifier=subject_identifier).first()
            if child_hiv_testing_obj:
                if child_hiv_testing_obj.preferred_test_venue == 'facet_study':
                    self.initial['test_venue'] = child_hiv_testing_obj.preferred_test_venue
                    self.fields['test_venue'].widget = forms.TextInput(
                        attrs={'readonly': 'readonly'})

    class Meta:
        model = ChildHivPendingResults
        fields = '__all__'
