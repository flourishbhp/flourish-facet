from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ...admin_site import flourish_facet_admin
from ...forms import FacetCaregiverContactForm
from ...models import FacetCaregiverContact
from ..modeladmin_mixins import ModelAdminMixin


@admin.register(FacetCaregiverContact, site=flourish_facet_admin)
class FacetCaregiverContactAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = FacetCaregiverContactForm

    search_fields = ['subject_identifier']

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'report_datetime',
                'contact_type',
                'contact_datetime',
                'call_reason',
                'call_reason_other',
                'contact_success',
                'contact_comment',
                'call_rescheduled',
                'reason_rescheduled',
                'reason_rescheduled_other',
            )}
         ), audit_fieldset_tuple)

    list_display = [
        'subject_identifier', 'contact_type',
        'contact_datetime', 'call_reason', 'contact_success']

    list_filter = ['contact_type', 'call_reason', 'contact_success']

    radio_fields = {
        'contact_type': admin.VERTICAL,
        'call_reason': admin.VERTICAL,
        'contact_success': admin.VERTICAL,
        'call_rescheduled': admin.VERTICAL,
        'reason_rescheduled': admin.VERTICAL,
    }
