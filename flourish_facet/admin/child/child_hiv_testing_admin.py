from django.contrib import admin
from ...models import ChildHivTesting
from ...admin_site import flourish_facet_admin
from ...forms import ChildHivTestingForm
from edc_model_admin import audit_fieldset_tuple
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(ChildHivTesting, site=flourish_facet_admin)
class ChildHivTestingAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = ChildHivTestingForm

    fieldsets = (
        (None, {
            'fields': [
                'facet_visit',
                'report_datetime',
                'child_tested',
                'reason_not_tested',
                'reason_not_tested_other',
                'child_tested_6_weeks',
                'result_6_weeks_in',
                'hiv_result_6_weeks',
                'reason_results_unavailable',
                'reason_results_unavailable_other',
                'preferred_test_venue',
                'reason_not_tested_6_weeks',
                'reason_not_tested_6_weeks_other',
                'child_breastfed',
                'child_breastfeeding',
                'child_breastfed_end'
            ]}), audit_fieldset_tuple
    )

    radio_fields = {
        'child_tested': admin.VERTICAL,
        'reason_not_tested': admin.VERTICAL,
        'child_tested_6_weeks': admin.VERTICAL,
        'hiv_result_6_weeks': admin.VERTICAL,
        'reason_not_tested_6_weeks': admin.VERTICAL,
        'child_breastfed': admin.VERTICAL,
        'child_breastfeeding': admin.VERTICAL,
        'child_breastfed_end': admin.VERTICAL,
        'result_6_weeks_in': admin.VERTICAL,
        'reason_results_unavailable': admin.VERTICAL,
        'preferred_test_venue': admin.VERTICAL,
    }
