from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .facet_contact_model_wrapper import FacetCaregiverContactModelWrapper


class FacetCaregiverContactModelWrapperMixin:

    facet_contact_model_wrapper_cls = FacetCaregiverContactModelWrapper

    @property
    def facet_contact_model_obj(self):
        """Returns a facet caregiver contact model instance or None.
        """
        try:
            return self.facet_contact_cls.objects.get(
                **self.facet_contact_options)
        except ObjectDoesNotExist:
            return None

    @property
    def facet_contact(self):
        """Returns a wrapped unsaved facet caregiver contact.
        """
        model_obj = self.facet_contact_cls(
            **self.create_facet_contact_options)
        return self.facet_contact_model_wrapper_cls(model_obj=model_obj)

    @property
    def facet_contact_cls(self):
        return django_apps.get_model('flourish_facet.facetcaregivercontact')

    @property
    def create_facet_contact_options(self):
        """Returns a dictionary of options to create a new
        unpersisted facet caregiver contact model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def facet_contact_options(self):
        """Returns a dictionary of options to get an existing
        facet caregiver contact model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
