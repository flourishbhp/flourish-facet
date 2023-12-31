from django.contrib import admin
from edc_fieldsets.fieldlist import Fieldlist
from edc_model_admin import audit_fieldset_tuple
from edc_constants.constants import POS
from ...admin_site import flourish_facet_admin
from ...models import MaternalHivArt
from ...forms import MaternalHivArtForm
from ..modeladmin_mixins import CrfModelAdminMixin
from flourish_caregiver.helper_classes import MaternalStatusHelper


@admin.register(MaternalHivArt, site=flourish_facet_admin)
class MaternalHivArtAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = MaternalHivArtForm

    hiv_pos_mothers = (
        'hiv_test_date',
        'art_received',
        'drug_combination_before',
        'drug_combination_before_other',
        'art_start_date',
        'art_received_preg',
        'drug_combination_during',
        'drug_combination_during_other',
        'art_switch',
        'art_regimen',
        'art_regimen_other',
        'art_regimen_start',
        'reason_regimen_change',
        'reason_regimen_change_other',
        'art_challenges',
        'art_challenges_other'
    )

    hiv_neg_mothers = (
        'father_hiv',
        'father_hiv_no',
        'father_hiv_dont',
        'comment',
        'hiv_result_father',
        'hiv_test_date_father',
        'father_art',
        'father_art_start',
        'hiv_status_disclosure',
        'hiv_status_disclosure_reaction',
        'comment_end',

    )

    fieldsets = (
        (None, {
            'fields': (
                'facet_visit',
                'report_datetime',
            ),
        },),)

    radio_fields = {
        'art_received': admin.VERTICAL,
        'drug_combination_before': admin.VERTICAL,
        'art_received_preg': admin.VERTICAL,
        'drug_combination_during': admin.VERTICAL,
        'art_switch': admin.VERTICAL,
        'art_regimen': admin.VERTICAL,
        'reason_regimen_change': admin.VERTICAL,
        'father_hiv': admin.VERTICAL,
        'father_hiv_no': admin.VERTICAL,
        'father_hiv_dont': admin.VERTICAL,
        'hiv_result_father': admin.VERTICAL,
        'father_art': admin.VERTICAL,
        'hiv_status_disclosure': admin.VERTICAL,
    }

    filter_horizontal = (
        'art_challenges', 'hiv_status_disclosure_reaction'
    )

    conditional_fieldlists = {
        'hiv_pos': Fieldlist(
            insert_fields=hiv_pos_mothers,
            remove_fields=hiv_neg_mothers,
            insert_after='report_datetime',),
        'hiv_neg': Fieldlist(
            insert_fields=hiv_neg_mothers,
            remove_fields=hiv_pos_mothers,
            insert_after='report_datetime',), }

    def get_key(self, request, obj=None):

        subject_identifier = request.GET.get('subject_identifier', None)

        if not subject_identifier:

            subject_identifier = obj.facet_visit.subject_identifier

        status = MaternalStatusHelper(subject_identifier=subject_identifier)
        return 'hiv_pos' if status.hiv_status == POS else 'hiv_neg'
