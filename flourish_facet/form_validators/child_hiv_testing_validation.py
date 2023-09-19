from edc_form_validators import FormValidator
from edc_constants.constants import NO, YES


class ChildHivTestingFormValidator(FormValidator):
    def clean(self):
        super().clean()

        self.required_if(NO, field='child_tested',
                         field_required='reason_not_tested')

        self.required_if(NO, field='child_tested_6_weeks',
                         field_required='reason_not_tested_6_weeks')

        self.required_if(YES, field='child_breastfed',
                         field_required='child_breastfed_end')

        self.not_applicable_if(YES, field='child_tested',
                               field_applicable='reason_not_tested')

        self.not_applicable_if(
            YES, field='child_tested_6_weeks', field_applicable='reason_not_tested_6_weeks')

        self.validate_other_specify(
            field='reason_not_tested', other_specify_field='reason_not_tested_other')

        self.validate_other_specify(
            field='reason_not_tested_6_weeks', other_specify_field='reason_not_tested_6_weeks_other')
