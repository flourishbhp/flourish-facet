from flourish_form_validations.form_validators import CaregiverReferralFUFormValidator

from ...models import FacetCaregiverPhqPostReferral
from flourish_caregiver.forms.form_mixins import SubjectModelFormMixin


class FacetCaregiverPhqPostReferralForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFUFormValidator

    class Meta:
        model = FacetCaregiverPhqPostReferral
        fields = '__all__'
