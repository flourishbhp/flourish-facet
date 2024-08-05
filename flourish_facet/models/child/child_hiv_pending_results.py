from django.db import models
from ..model_mixins import CrfModelMixin
from ...choices import POS_NEG_IND
from edc_base.model_validators import date_not_future


class ChildHivPendingResults(CrfModelMixin):
    hiv_test_date = models.DateField(
        verbose_name='When was the child tested',
        validators=[date_not_future],)

    test_venue = models.CharField(
        verbose_name="Where was the child tested",
        max_length=20,
    )

    hiv_result = models.CharField(
        verbose_name="What was the childs results",
        choices=POS_NEG_IND,
        max_length=15,)

    class Meta:
        app_label = 'flourish_facet'
        verbose_name = 'Child HIV Pending Results'
        verbose_name_plural = 'Child HIV Pending Results'
