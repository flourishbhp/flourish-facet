from edc_metadata_rules import CrfRule, CrfRuleGroup, register, PF
from edc_metadata import NOT_REQUIRED, REQUIRED


app_label = 'flourish_facet'


@register()
class ChildHivTestingRuleGroup(CrfRuleGroup):
    child_hiv_testing = CrfRule(
        predicate=PF('preferred_test_venue', func=lambda preferred_test_venue: True if preferred_test_venue ==
                     'local_clinic' or preferred_test_venue == 'facet_study' else False),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.childhivpendingresults'],
    )

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.childhivtesting'
