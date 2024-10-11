import datetime
import re
import threading
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from django.utils.decorators import method_decorator

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from flourish_export.identifiers import ExportIdentifier
from flourish_export.models import ExportFile
from flourish_export.views.listboard_view_mixin import ListBoardViewMixin
from ..model_wrappers import FacetExportFileModelWrapper
from ..utils import FacetExportFacade


class FacetExportListBoardView(NavbarViewMixin, EdcBaseViewMixin, ListBoardViewMixin,
                               ListboardFilterViewMixin, SearchFormViewMixin, ListboardView):

    listboard_template = 'facet_export_listboard_template'
    listboard_url = 'facet_export_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    model = 'flourish_export.exportfile'
    model_wrapper_cls = FacetExportFileModelWrapper
    identifier_cls = ExportIdentifier
    navbar_name = 'flourish_facet'
    navbar_selected_item = 'facet_export_listboard'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'facet_export_listboard_url'
    description_queryset_lookups = []

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        download = self.request.GET.get('download')

        facet_facade = FacetExportFacade(self.request)

        if download == '1':

            facet_facade.generate_export()

        context.update(export_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset(self):
        return super().get_queryset().filter(study='flourish_facet', description='Flourish Facet Export(s)')
