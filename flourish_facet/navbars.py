from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'flourish_facet' else False

flourish_facet = Navbar(name='flourish_facet')


flourish_facet.append_item(
    NavbarItem(
        name='flourish_consent_listboard',
        title='flourish_consent_listboard',
        label='Flourish Consent Listboard',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES[
            'facet_flourish_consent_listboard_url'],
        no_url_namespace=no_url_namespace))

flourish_facet.append_item(
    NavbarItem(
        name='facet_mother_listboard',
        title='facet_mother_listboard',
        label='FACET Mother Listboard',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES[
            'facet_mother_listboard_url'],
        no_url_namespace=no_url_namespace))


flourish_facet.append_item(
    NavbarItem(
        name='facet_child_listboard',
        title='facet_child_listboard',
        label='FACET Child Listboard',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES[
            'facet_child_listboard_url'],
        no_url_namespace=no_url_namespace))


flourish_facet.append_item(
    NavbarItem(
        name='group_interview_listboard',
        title='group_interview_listboard',
        label='Group Interview Listboard',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES[
            'group_interview_listboard_url'],
        no_url_namespace=no_url_namespace))


flourish_facet.append_item(
    NavbarItem(
        name='facet_export_listboard',
        title='facet_export_listboard',
        label='Export Listboard',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES[
            'facet_export_listboard_url'],
        no_url_namespace=no_url_namespace))

flourish_facet.append_item(
    NavbarItem(name='flourish_facet_export',
               label='Facet Exports',
               fa_icon='fa fa-database',
               url_name='flourish_facet:facet_export_url'))

flourish_facet.append_item(
    NavbarItem(name='flourish_facet_admin',
               label='Admin',
               fa_icon='fa-cogs',
               url_name='flourish_facet:admin_url'))

site_navbars.register(flourish_facet)
