from django.conf import settings
from django.apps import apps as django_apps

from edc_model_wrapper import ModelWrapper
from flourish_dashboard.model_wrappers.consent_model_wrapper_mixin import ConsentModelWrapperMixin


class FacetCaregiverContactModelWrapper(ConsentModelWrapperMixin, ModelWrapper):

    model = 'flourish_facet.facetcaregivercontact'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'facet_flourish_consent_listboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier']

    @staticmethod
    def contact_details_exist(subject_identifier):
        """
        Helper method, to check if any contact details exist since one
        participant can have more than one contact details 
        """
        contact_details_cls = django_apps.get_model(
            'flourish_facet.facetcaregivercontact')

        return contact_details_cls.objects.filter(
            subject_identifier=subject_identifier).exists()
