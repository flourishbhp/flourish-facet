from django.db import models
from ..model_mixins import CrfModelMixin
from ...choices import (AGE_BREASTFEEDING_ENDED, POS_NEG_IND, REASON_RESULTS_UNAVAILABLE, TEST_VENUE, YES_NO_DNK,
                        REASON_CHILD_NOT_TESTED)
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO


class ChildHivTesting(CrfModelMixin):

    child_tested = models.CharField(
        verbose_name='Has your child ever been tested for HIV ?',
        max_length=15,
        choices=YES_NO_DNK,
        help_text='If no, go to question 4 , If yes go to question 6'
    )

    reason_not_tested = models.CharField(
        verbose_name='What is the reason your child has never been tested for HIV?',
        max_length=35,
        choices=REASON_CHILD_NOT_TESTED,
        null=True,
        blank=True
    )

    reason_not_tested_other = OtherCharField()

    child_tested_6_weeks = models.CharField(
        verbose_name='Was your child tested for HIV at their 6-week visit?',
        max_length=15,
        choices=YES_NO_DNK,
        help_text='If no, go to question 12 , If yes go to question 7'
    )
    result_6_weeks_in = models.CharField(
        verbose_name='Have you received the results of this test?',
        max_length=15,
        choices=YES_NO,
        help_text='If no, go to question  9, If yes go to question 8'
    )

    hiv_result_6_weeks = models.CharField(
        verbose_name="What was your child’s HIV test result at 6 weeks",
        choices=POS_NEG_IND,
        blank=True,
        max_length=15,
        help_text='If Positive, take off-study , If Negative go to question 14')

    reason_results_unavailable = models.CharField(
        max_length=40,
        choices=REASON_RESULTS_UNAVAILABLE,
        verbose_name="If you have never received the HIV test results for 6 weeks,why?",
        null=True,
        blank=True
    )
    reason_results_unavailable_other = OtherCharField()

    preferred_test_venue = models.CharField(
        max_length=35,
        choices=TEST_VENUE,
        verbose_name="Where would you like to test your child at?",
        null=True,
        blank=True
    )

    reason_not_tested_6_weeks = models.CharField(
        max_length=35,
        choices=REASON_CHILD_NOT_TESTED,
        verbose_name="If your child was not tested for HIV at their 6-week visit, what was the reason? ",
        null=True,
        blank=True
    )
    reason_not_tested_6_weeks_other = OtherCharField()

    child_breastfed = models.CharField(
        verbose_name='Have you ever breastfed your child?',
        max_length=15,
        choices=YES_NO_DNK,
        help_text='If no, go to question 16 , If yes go to question 15'
    )

    child_breastfeeding = models.CharField(
        verbose_name='Are you currently still breatfeeding your child ?',
        max_length=15,
        null=True,
        blank=True,
        choices=YES_NO_DNK,
    )

    child_breastfed_end = models.CharField(
        verbose_name=(
            'If you already stopped breastfeeding your child,''How old was your child when you stopped breastfeeding?'),
        choices=AGE_BREASTFEEDING_ENDED,
        max_length=20,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'flourish_facet'
        verbose_name = 'Child HIV Testing'
        verbose_name_plural = 'Child HIV Testing'
