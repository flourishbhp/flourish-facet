from edc_form_validators import FormValidator


class ChildHivPendingResultsFormValidator(FormValidator):
    def clean(self):
        super().clean()
