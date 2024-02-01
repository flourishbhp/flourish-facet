from edc_form_validators import FormValidator
from edc_constants.choices import NOT_APPLICABLE


class FacetVisitFormValidator(FormValidator):
    def clean(self):
        super().clean()
        self.validate_other_specify(field='info_source')
