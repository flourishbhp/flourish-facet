
from edc_constants.constants import POS
from edc_metadata_rules import PredicateCollection
from ...models import MotherChildConsent
from flourish_caregiver.helper_classes import MaternalStatusHelper
from django.apps import apps as django_apps


class ChildPredicates(PredicateCollection):
    app_label = "flourish_facet"
    visit_model = f"{app_label}.facetvisit"

    def func_hiv_exposed(self, visit=None, **kwargs):
        """
        Check if the child is exposed, the child is exposed
        if the mother is HIV positive 
        """

        try:

            consent = MotherChildConsent.objects.get(
                subject_identifier=visit.subject_identifier
            )

        except MotherChildConsent.DoesNotExist:
            pass

        else:

            maternal_status_helper = MaternalStatusHelper(
                subject_identifier=consent.facet_consent.subject_identifier)

            return maternal_status_helper.hiv_status == POS

    def func_pending_results(self, visit=None, **kwargs):
        child_hiv_testing_model_cls = django_apps.get_model(
            f'{self.app_label}.childhivtesting')

        try:
            child_hiv_obj = child_hiv_testing_model_cls.objects.get(
                facet_visit__subject_identifier=visit.subject_identifier
            )
        except child_hiv_testing_model_cls.DoesNotExist:
            pass
        else:
            venues = ['facet_study', 'local_clinic']
            return (
                child_hiv_obj.preferred_test_venue in venues
            )
        return False
