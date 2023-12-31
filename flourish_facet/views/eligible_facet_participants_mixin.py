from django.apps import apps as django_apps
from edc_base.utils import get_utcnow
from dateutil.relativedelta import relativedelta
from edc_constants.constants import YES
from django.db.models import Max


class EligibleFacetParticipantsMixin:
    child_hiv_rapid_test_model = 'flourish_child.childhivrapidtestcounseling'
    antenatal_enrollment_model = 'flourish_caregiver.antenatalenrollment'
    facet_screening_model = 'flourish_facet.facetsubjectscreening'
    facet_consent_model = 'flourish_facet.facetconsent'
    subject_consent_model = 'flourish_caregiver.subjectconsent'

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    @property
    def flourish_child_consent_cls(self):
        return django_apps.get_model(self.flourish_child_consent_model)

    @property
    def facet_screening_cls(self):
        return django_apps.get_model(self.facet_screening_model)

    @property
    def facet_consent_cls(self):
        return django_apps.get_model(self.facet_consent_model)

    @property
    def child_hiv_rapid_test_cls(self):
        return django_apps.get_model(self.child_hiv_rapid_test_model)

    def eligible_participants(self, queryset):
        dates_before = (get_utcnow() - relativedelta(months=6, days=10)
                        ).date().isoformat()

        today = get_utcnow().date().isoformat()

        anc_subject_identifiers = self.antenatal_enrollment_cls.objects. \
            values_list('subject_identifier', flat=True)

        subject_identifiers = self.flourish_child_consent_cls.objects.filter(
            child_dob__range=[dates_before, today],
            subject_consent__subject_identifier__in=anc_subject_identifiers,
            subject_consent__future_contact=YES
        ).values_list('subject_consent__subject_identifier', flat=True)

        facet_screened_identifiers = self.facet_screening_cls.objects.values_list(
            'subject_identifier', flat=True)

        subject_identifiers = set(
            [*subject_identifiers, *facet_screened_identifiers])

        consent_ids = []

        for subject_identifier in subject_identifiers:
            consent = self.subject_consent_cls.objects.filter(
                subject_identifier=subject_identifier
            ).latest('version')

            consent_ids.append(consent.id)

        return queryset.filter(id__in=consent_ids,
                               subject_identifier__startswith='B').annotate(
            child_dob=Max('caregiverchildconsent__child_dob'), ).order_by('child_dob')
