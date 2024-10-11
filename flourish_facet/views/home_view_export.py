from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from flourish_export.admin_export_helper import AdminExportHelper
from flourish_export.identifiers import ExportIdentifier
from flourish_export.models.export_file import ExportFile
from flourish_export.views.export_methods_view_mixin import ExportMethodsViewMixin
from flourish_export.views.listboard_view_mixin import ListBoardViewMixin
from flourish_facet.utils.facet_export_facade import FacetExportFacade


class HomeViewExport(ExportMethodsViewMixin,
                     ListBoardViewMixin, EdcBaseViewMixin,
                     NavbarViewMixin, TemplateView):

    template_name = 'flourish_facet/home_export.html'
    navbar_name = 'flourish_facet'
    navbar_selected_item = 'flourish_facet_export'
    admin_helper_cls = AdminExportHelper
    export_identifier_cls = ExportIdentifier

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        download = self.request.GET.get('download')

        facet_facade = FacetExportFacade(self.request)

        if download == '6':
            facet_facade.generate_export(flat_export=True)

        facet_exports = ExportFile.objects.filter(
            description='Flourish Facet Flat Export(s)').order_by('-uploaded_at')[:10]
        context.update(
            facet_exports=facet_exports,
        )
        return context
