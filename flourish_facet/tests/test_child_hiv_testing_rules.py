from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata
from model_mommy import mommy
import pytz
from edc_constants.constants import YES, NO

from edc_appointment.models import Appointment
from edc_visit_tracking.constants import SCHEDULED


@tag('cht')
class TestChildHivTestingGroups(TestCase):

    def setUp(self):
        import_holidays()

        facet_screening = mommy.make_recipe(
            'flourish_facet.facetsubjectscreening',
            subject_identifier='B142-040990520-4'
        )

        facet_consent = mommy.make_recipe(
            'flourish_facet.facetconsent',
            consent_datetime=get_utcnow(),
            version='1',
            subject_identifier=facet_screening.subject_identifier
        )

        child_consent = mommy.make_recipe(
            'flourish_facet.motherchildconsent',
            facet_consent=facet_consent,
        )
        self.subject_identifier = child_consent.subject_identifier

    def test_child_hiv_pending_results_required(self):
        visit_200F = mommy.make_recipe(
            'flourish_facet.facetvisit',
            appointment=Appointment.objects.get(
                visit_code='2000F',
                subject_identifier=self.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.childhivtesting = mommy.make_recipe(
            'flourish_facet.childhivtesting',
            facet_visit=visit_200F,
            preferred_test_venue='local_clinic'
        )

        self.assertEqual(
            CrfMetadata.objects.get(
                model='flourish_facet.childhivpendingresults',
                subject_identifier=visit_200F.subject_identifier,
                visit_code='200F').entry_status, REQUIRED)
