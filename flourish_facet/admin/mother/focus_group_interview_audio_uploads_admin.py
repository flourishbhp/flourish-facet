from django.contrib import admin

from ...models.list_models import FgfSubjectIdentifiers
from ...models import FocusGroupInterviewAudioUploads, FacetConsent
from ...admin_site import flourish_facet_admin
from ...forms import FocusGroupInterviewAudioUploadsForm
from edc_model_admin import audit_fieldset_tuple
from ..modeladmin_mixins import ModelAdminMixin
from edc_list_data import PreloadData


@admin.register(FocusGroupInterviewAudioUploads, site=flourish_facet_admin)
class FocusGroupInterviewAudioUploadsAdmin(ModelAdminMixin, admin.ModelAdmin):
    readonly_fields = ('group_identifier',)
    form = FocusGroupInterviewAudioUploadsForm

    fieldsets = (
        (None, {
            'fields': [
                'group_identifier',
                'paticipant_ids',
                'report_datetime',
                'location',
                'location_other',
                'interview_duration',
                'interview_language',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'location': admin.VERTICAL,
        'interview_language': admin.VERTICAL,
    }

    filter_horizontal = ['paticipant_ids',]

    def add_view(self, request, form_url='', extra_context=None):
        self.load_list_data(request)
        return super().add_view(request, form_url, extra_context)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'paticipant_ids':
            kwargs['queryset'] = self.get_fgf_qs(request)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_fgf_qs(self, request):
        return FgfSubjectIdentifiers.objects.exclude(
            name__in=self.get_used_identifiers(request))

    def get_subject_identifiers(self, request):
        subject_identifiers = FacetConsent.objects.exclude(
            subject_identifier__in=self.get_used_identifiers(request)).values_list(
            'subject_identifier', flat=True)
        return subject_identifiers

    def get_used_identifiers(self, request):
        group_id = request.GET.get('group_identifier', None)
        return FocusGroupInterviewAudioUploads.objects.exclude(
            group_identifier=group_id).values_list(
            'paticipant_ids__name', flat=True)

    def load_list_data(self, request):
        subject_identifiers = list(set(self.get_subject_identifiers(request)))
        subject_id_list = [(identifier, identifier)
                           for identifier in subject_identifiers]

        list_data = {'flourish_facet.fgfsubjectidentifiers': subject_id_list}
        PreloadData(list_data=list_data)
