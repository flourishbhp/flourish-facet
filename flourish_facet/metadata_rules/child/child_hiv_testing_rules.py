from edc_metadata_rules import CrfRule, CrfRuleGroup, register
from edc_metadata import NOT_REQUIRED, REQUIRED

from ..predicates import ChildPredicates


app_label = 'flourish_facet'
pc = ChildPredicates()


@register()
class ChildHivTestingRuleGroup(CrfRuleGroup):
    child_hiv_testing = CrfRule(
        predicate=pc.func_pending_results,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.childhivpendingresults'],
    )

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.childhivtesting'
