from django.apps import apps as django_apps
from django.conf import settings
from django.db.models import Q
from edc_constants.constants import YES
from edc_model_wrapper import ModelWrapper


class LocatorModelWrapper(ModelWrapper):
    model = 'flourish_caregiver.caregiverlocator'

    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'facet_flourish_consent_listboard_url')
    next_url_attrs = ['subject_identifier']
