from flourish_facet.forms.form_mixins import SubjectModelFormMixin
from ...models import FacetCaregiverEdinburghReferral
from ...form_validators import CaregiverReferralFormValidator


class FacetCaregiverEdinburghReferralForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFormValidator

    class Meta:
        model = FacetCaregiverEdinburghReferral
        fields = '__all__'
