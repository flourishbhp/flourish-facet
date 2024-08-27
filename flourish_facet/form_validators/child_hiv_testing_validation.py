from edc_form_validators import FormValidator
from edc_constants.constants import NO, YES, OTHER


class ChildHivTestingFormValidator(FormValidator):
    def clean(self):
        super().clean()

        self.required_if(NO, field='child_tested',
                         field_required='reason_not_tested')

        self.required_if(NO, field='child_tested_6_weeks',
                         field_required='reason_not_tested_6_weeks')

        self.required_if(YES, field='child_breastfed',
                         field_required='child_breastfeeding')

        self.required_if(NO, field='child_breastfeeding',
                         field_required='child_breastfed_end')

        self.not_applicable_if(YES, field='child_tested',
                               field_applicable='reason_not_tested')
        self.required_if(YES, field='result_6_weeks_in',
                         field_required='hiv_result_6_weeks')

        results_not_in = ['reason_results_unavailable', 'preferred_test_venue']
        for results in results_not_in:
            self.required_if(NO, field='result_6_weeks_in',
                             field_required=results)

        self.not_applicable_if(
            YES, field='child_tested_6_weeks', field_applicable='reason_not_tested_6_weeks')

        self.validate_other_specify(
            field='reason_not_tested', other_specify_field='reason_not_tested_other')

        self.validate_other_specify(
            field='reason_results_unavailable', other_specify_field='reason_results_unavailable_other')

        self.validate_other_specify(
            field='reason_not_tested_6_weeks', other_specify_field='reason_not_tested_6_weeks_other')
