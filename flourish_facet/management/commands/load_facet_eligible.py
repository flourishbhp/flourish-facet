from django.apps import apps as django_apps
from django.core.management import BaseCommand
from flourish_caregiver.models import (SubjectConsent,
                                       RelationshipFatherInvolvement,
                                       AntenatalEnrollment, UltraSound)
from flourish_facet.models import FacetConsent
from edc_constants.constants import (NEG, POS)
from flourish_facet.views import EligibleFacetParticipantsMixin
from edc_base import get_utcnow
import pandas as pd


class Command(BaseCommand):
    help = '''\
    Used to extract all the eligible participants for facet that are pregnant and
    without a partner for a weekly report.
    '''

    def handle(self, *args, **options):

        # Get eligible participants
        sc = SubjectConsent.objects.all()
        eligble = EligibleFacetParticipantsMixin()
        result = eligble.eligible_participants(sc)

        facet_consents = self.confirm_no_facet_consent(result)

        caregiver_ids = self.confirm_child_dob(facet_consents)

        eligible_pids = self.get_antenatal_relationship_status(caregiver_ids)

        # Convert data to DataFrame

        df = pd.DataFrame(eligible_pids)

        # Export DataFrame to CSV
        custom_headers = {
            'subject_identifier': 'Subject Identifier',
            'hiv_status': 'Current HIV Status',
            'edd_by_lmp': 'Estimated Delivery Date',
            'ga_weeks': 'Gestational Age (weeks)',
            'partner_present': 'Partner Present'
        }
        df = df.rename(columns=custom_headers)
        df.to_csv('weekly_report.csv', index=False)

        self.stdout.write(self.style.SUCCESS(
            'Weekly report for pregnant participants generated successfully.'))

    # Confirm that the eligible participants is not consented for facet
    def confirm_no_facet_consent(self, result):
        ids = []
        for identifier in result:
            try:
                FacetConsent.objects.get(
                    subject_identifier=identifier.subject_identifier)
            except FacetConsent.DoesNotExist:
                ids.append(identifier.subject_identifier)
            else:
                pass
        return ids

    # Confirm participants are still pregnant
    def confirm_child_dob(self, consent_xids):
        flourish_child_consent_model = 'flourish_caregiver.caregiverchildconsent'
        child_birth_model = 'flourish_child.childbirth'
        flourish_child_consent_cls = django_apps.get_model(
            flourish_child_consent_model)
        child_birth_cls = django_apps.get_model(child_birth_model)
        child_ids = []

        for obj in consent_xids:
            child_identifiers = flourish_child_consent_cls.objects.filter(
                child_dob__isnull=True,
                subject_consent__subject_identifier=obj
            )
            for child in child_identifiers:
                child_dob = getattr(child, 'child_dob', None)
                if child_dob is None:
                    child_ids.append(obj)
                else:
                    pass

        child_b_identifiers = child_birth_cls.objects.values_list(
            'subject_identifier', flat=True)

        child_identifiers_set = set(child_b_identifiers)
        child_consent_subject_identifiers_set = set(child_ids)
        result = child_consent_subject_identifiers_set - child_identifiers_set

        return list(result)

    def get_antenatal_relationship_status(self, xids):
        x_data = []
        for xid in xids:
            try:
                ant = AntenatalEnrollment.objects.filter(
                    subject_identifier=xid, current_hiv_status=NEG).latest('created')
            except AntenatalEnrollment.DoesNotExist:
                pass
            else:
                try:
                    rfi = RelationshipFatherInvolvement.objects.filter(
                        maternal_visit__subject_identifier=xid, partner_present='No').latest('created')
                except RelationshipFatherInvolvement.DoesNotExist:
                    pass
                else:

                    if ant.last_period_date is not None:
                        today = get_utcnow().date()
                        ga_weeks = (today - ant.last_period_date).days / 7
                        x_data.append({
                            'subject_identifier': ant.subject_identifier,
                            'hiv_status': ant.current_hiv_status,
                            'edd_by_lmp': ant.edd_by_lmp,
                            'ga_weeks': ga_weeks,
                            'partner_present': rfi.partner_present
                        })

                    else:
                        try:
                            ultrasound = UltraSound.objects.get(
                                child_subject_identifier=ant.child_subject_identifier,
                                maternal_visit__subject_identifier=xid)
                        except UltraSound.DoesNotExist:
                            pass
                        else:
                            x_data.append({
                                'subject_identifier': ant.subject_identifier,
                                'hiv_status': ant.current_hiv_status,
                                'edd_by_lmp': ultrasound.est_edd_ultrasound,
                                'ga_weeks': ultrasound.ga_confirmed,
                                'partner_present': rfi.partner_present
                            })
        return x_data
