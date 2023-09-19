from ...form_validators import CaregiverReferralFUFormValidator
from ...models import FacetCaregiverGadPostReferral
from flourish_facet.forms.form_mixins import SubjectModelFormMixin


class FacetCaregiverGadPostReferralForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFUFormValidator

    class Meta:
        model = FacetCaregiverGadPostReferral
        fields = '__all__'
