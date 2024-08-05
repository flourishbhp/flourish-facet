from django.contrib import admin
from ...models import ChildHivPendingResults
from ...admin_site import flourish_facet_admin
from ...forms import ChildHivPendingResultsForm
from edc_model_admin import audit_fieldset_tuple
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(ChildHivPendingResults, site=flourish_facet_admin)
class ChildHivPendingResultsAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = ChildHivPendingResultsForm

    fieldsets = (
        (None, {
            'fields': [
                'facet_visit',
                'report_datetime',
                'hiv_test_date',
                'test_venue',
                'hiv_result'
            ]}), audit_fieldset_tuple
    )

    radio_fields = {
        'hiv_result': admin.VERTICAL
    }
