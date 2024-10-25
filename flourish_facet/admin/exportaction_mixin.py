import datetime
import uuid
from django.apps import apps as django_apps
from django.db.models.fields.reverse_related import OneToOneRel
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from flourish_export.admin_export_helper import AdminExportHelper
from flourish_facet.models.child.mother_child_consent import MotherChildConsent
from flourish_facet.models.mother.facet_consent import FacetConsent
import xlwt
from flourish_caregiver.helper_classes import MaternalStatusHelper
from django.db.models import ManyToManyField, ForeignKey, OneToOneField, ManyToOneRel, FileField, ImageField


class ExportActionMixin(AdminExportHelper):

    def update_variables(self, data={}):
        """ Update study identifiers to desired variable name(s).
        """
        replace_idx = {}
        for old_idx, new_idx in replace_idx.items():
            try:
                data[new_idx] = data.pop(old_idx)
            except KeyError:
                continue
        return data

    def study_status(self, subject_identifier=None):
        if not subject_identifier:
            return ''
        caregiver_offstudy_cls = django_apps.get_model(
            'flourish_prn.caregiveroffstudy')
        is_offstudy = caregiver_offstudy_cls.objects.filter(
            subject_identifier=subject_identifier).exists()

        return 'off_study' if is_offstudy else 'on_study'

    def export_as_csv(self, request, queryset):
        records = []

        for obj in queryset:
            data = self.process_object_fields(obj)

            subject_identifier = getattr(obj, 'subject_identifier', None)
            screening_identifier = self.screening_identifier(
                subject_identifier=subject_identifier)

            # Update variable names for study identifiers
            data = self.update_variables(data)

            records.append(data)
        response = self.write_to_csv(records=records)
        return response

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]

    def write_rows(self, data=None, row_num=None, ws=None):

        for col_num in range(len(data)):
            if isinstance(data[col_num], uuid.UUID):
                ws.write(row_num, col_num, str(data[col_num]))
            elif isinstance(data[col_num], datetime.datetime):
                dt = data[col_num]
                if dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None:
                    dt = timezone.make_naive(dt)
                dt = dt.strftime('%Y/%m/%d')
                ws.write(row_num, col_num, dt, xlwt.easyxf(
                    num_format_str='YYYY/MM/DD'))
            elif isinstance(data[col_num], datetime.date):
                ws.write(row_num, col_num, data[col_num], xlwt.easyxf(
                    num_format_str='YYYY/MM/DD'))
            else:
                ws.write(row_num, col_num, data[col_num])

    def update_headers_inline(self, inline_fields=None, field_names=None,
                              ws=None, row_num=None, font_style=None):
        top_num = len(field_names)
        for col_num in range(len(inline_fields)):
            ws.write(row_num, top_num, inline_fields[col_num], font_style)
            top_num += 1
            self.inline_header = True

    def screening_identifier(self, subject_identifier=None):
        """Returns a screening identifier.
        """
        consent = self.consent_obj(subject_identifier=subject_identifier)

        if consent:
            return getattr(consent, 'screening_identifier', None)
        return None

    def caregiver_hiv_status(self, subject_identifier=None):

        status_helper = MaternalStatusHelper(
            subject_identifier=subject_identifier)

        return status_helper.hiv_status

    def consent_obj(self, subject_identifier: str):
        consent_cls = django_apps.get_model('flourish_facet.facetconsent')
        consent = consent_cls.objects.filter(
            subject_identifier=subject_identifier)

        if consent.exists():
            return consent.last()
        return None

    def is_consent(self, obj):
        consent_cls = django_apps.get_model('flourish_facet.facetconsent')
        return isinstance(obj, consent_cls)

    def is_visit(self, obj):
        visit_cls = django_apps.get_model('flourish_facet.facetvisit')
        return isinstance(obj, visit_cls)
    
    def is_appointment(self, obj):
        appointment_cls = django_apps.get_model('flourish_facet.appointment')
        return isinstance(obj, appointment_cls)
    def is_facet_clinician_notes(self, obj):
        facet_clinician_cls = django_apps.get_model('flourish_facet.facetcliniciannotes')
        return isinstance(obj, facet_clinician_cls)
    def is_clinician_notes_image(self, obj):
        clinician_cls= django_apps.get_model('flourish_facet.cliniciannotesimage')
        return isinstance(obj, clinician_cls)

    @property
    def get_model_fields(self):
        return [field for field in self.model._meta.get_fields()
                if field.name not in self.exclude_fields and not isinstance(field,
                                                                            OneToOneRel)]

    def inline_exclude(self, field_names=[]):
        return [field_name for field_name in field_names
                if field_name not in self.exclude_fields]

    @property
    def exclude_fields(self):
        return ['_state', 'hostname_created', 'hostname_modified',
                'revision', 'device_created', 'device_modified', 'id', 'site_id',
                'modified_time', 'report_datetime_time', 'registration_datetime_time',
                'screening_datetime_time', 'modified', 'form_as_json', 'consent_model',
                'randomization_datetime', 'registration_datetime', 'is_verified_datetime',
                'first_name', 'last_name', 'initials', 'identity', 'facet_visit_id',
                'confirm_identity', 'motherchildconsent', 'slug']

    def process_object_fields(self, obj):
        data = obj.__dict__.copy()

        subject_identifier = getattr(obj, 'subject_identifier', None)
        caregiver_hiv_status = self.caregiver_hiv_status(
            subject_identifier=subject_identifier)

        if getattr(obj, 'facet_visit', None):
            data.update(subject_identifier=subject_identifier,
                        visit_code=obj.visit_code)

        for field in self.get_model_fields:

            field_name = field.name
            if (field_name == 'consent_version') and self.is_visit(obj):
                data.update({f'{field_name}': '1'})
                continue
            if isinstance(field, (ForeignKey, OneToOneField, OneToOneRel)):
                continue
            if isinstance(field, (FileField, ImageField)):
                file_obj = getattr(obj, field_name, '')
                data.update({f'{field_name}': getattr(file_obj, 'name', '')})
                continue
            if isinstance(field, ManyToManyField):
                data.update(self.m2m_data_dict(obj, field))
                continue
            if not (self.is_consent(obj) or self.is_visit(obj)) and isinstance(field, ManyToOneRel):
                data.update(self.inline_data_dict(obj, field))
                continue

        data.update(study_status=self.study_status(
            subject_identifier) or '')
        data.update(hiv_status=caregiver_hiv_status,)
        # Exclude identifying values
        data = self.remove_exclude_fields(data)
        # Correct date formats
        data = self.fix_date_formats(data)

        return data

    def get_flat_model_data(self, model):
        data = []
        model_name = model.__name__.lower()
        # Temporarily set self.model to the current model
        self.model = model
        try:
            for obj in model.objects.all():
                result_dict = self.check_all_methods(obj)
                if any(result for result in result_dict.values()):
                    continue
                relation_identifier = {}
                if isinstance(obj, MotherChildConsent):
                    facet_consent = getattr(obj, 'facet_consent', None)
                    mother_subject_identifier = getattr(facet_consent, 'subject_identifier', None)
                    relation_identifier = {"mother_identifier": mother_subject_identifier}
                
                elif isinstance(obj, FacetConsent):
                    mother_child_consent = obj.motherchildconsent_set.first()
                    child_subject_identifier = getattr(mother_child_consent, 'subject_identifier', None) if mother_child_consent else None
                    relation_identifier = {"child_identifier": child_subject_identifier}
            
                record = self.process_object_fields(obj)
                prefixed_record = {
                    f"{model_name}_{key}": value for key, value in record.items()}
                prefixed_record.update(relation_identifier)
                data.append(prefixed_record)
        finally:
            # Reset self.model after processing
            self.model = None

        return data
    
    def check_all_methods(self, obj):
        # List of method names to check
        method_names = ['is_visit', 'is_appointment', 'is_facet_clinician_notes', 'is_clinician_notes_image']

        # Dictionary to store results
        results = {}

        for method_name in method_names:
            # Use getattr to dynamically call the method
            method = getattr(self, method_name, None)
            
            if method and callable(method):
                # Call the method with obj and store the result
                results[method_name] = method(obj)
        
        return results
