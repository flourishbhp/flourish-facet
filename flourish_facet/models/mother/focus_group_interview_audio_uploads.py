from django.db import models
from edc_base.model_validators import datetime_not_future
from edc_protocol.validators import datetime_not_before_study_start
from edc_base.utils import get_utcnow
from flourish_facet.choices import LOCATION_INTERVIEW, LANGUAGES_BOTH
from edc_base.model_fields import OtherCharField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import FileExtensionValidator
from edc_base.sites import SiteModelMixin
from edc_base.model_mixins import BaseUuidModel
from flourish_facet.models.list_models import FgfSubjectIdentifiers
from ...group_identifier import FocusGroupIdentifier


class FocusGroupInterviewAudioUploads(SiteModelMixin, BaseUuidModel):

    group_identifier = models.CharField(
        verbose_name='Group identifier',
        max_length=50,
        unique=True,
        editable=False)

    paticipant_ids = models.ManyToManyField(
        FgfSubjectIdentifiers,
        related_name='paticipant_ids',
        verbose_name="Participants that are part of the focus group interview",)

    report_datetime = models.DateTimeField(
        verbose_name='Interview Date and Time',
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=get_utcnow,
        help_text='Date and time of this interview')

    location = models.CharField(
        verbose_name='Location of interview',
        choices=LOCATION_INTERVIEW,
        max_length=25,
    )

    location_other = OtherCharField()

    interview_duration = models.PositiveIntegerField(
        verbose_name="Duration of interview",
        validators=[MinValueValidator(10), MaxValueValidator(1440)],
        help_text='Minutes')

    interview_language = models.CharField(
        verbose_name='In what language was the interview performed?',
        choices=LANGUAGES_BOTH,
        max_length=15,
    )

    """returns a screening identifier as a string"""

    def __str__(self):
        return f'{self.group_identifier}'

    """returns screening identifier as tuple of type string"""

    def natural_key(self):
        return (self.group_identifier,)

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.extend(['group_identifier',])
        return fields

    def save(self, *args, **kwargs):
        if self.created and not self.group_identifier:
            self.group_identifier = self.make_new_identifier()
        super().save(*args, **kwargs)

    @property
    def group_type(self):
        """Return the letter that represents the group type.
        """
        return 'FGF'

    def make_new_identifier(self):
        """Returns a new and unique identifier.

        Override this if needed."""

        group_identifier = FocusGroupIdentifier(
            group_type=self.group_type,
            identifier_type='group',
            requesting_model=self._meta.label_lower)
        return group_identifier.identifier

    class Meta:
        app_label = 'flourish_facet'
        verbose_name = 'Focus Group Interview'
        verbose_name_plural = 'Focus Group Interview'
