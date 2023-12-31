from uuid import uuid4

from django.db import models
from django.db.models import options
from django_crypto_fields.fields import EncryptedTextField
from edc_base.model_validators import datetime_not_future
from edc_base.sites import CurrentSiteManager
from edc_base.utils import formatted_age, age
from edc_protocol.validators import datetime_not_before_study_start

from edc_consent.field_mixins import VerificationFieldsMixin
from edc_consent.managers import ObjectConsentManager, ConsentManager


class FacetConsentModelMixin(VerificationFieldsMixin, models.Model):

    """Mixin for a Consent model class such as SubjectConsent.

    Declare with edc_identifier's NonUniqueSubjectIdentifierModelMixin
    """

    consent_datetime = models.DateTimeField(
        verbose_name='Consent date and time',
        validators=[
            datetime_not_before_study_start,
            datetime_not_future])

    report_datetime = models.DateTimeField(
        null=True,
        editable=False)

    version = models.CharField(
        verbose_name='Consent version',
        max_length=10,
        help_text='See \'Consent Type\' for consent versions by period.',
        editable=False)

    updates_versions = models.BooleanField(default=False)

    sid = models.CharField(
        verbose_name='SID',
        max_length=15,
        null=True,
        blank=True,
        editable=False,
        help_text='Used for randomization against a prepared rando-list.')

    comment = EncryptedTextField(
        verbose_name='Comment',
        max_length=250,
        blank=True,
        null=True)

    dm_comment = models.CharField(
        verbose_name='Data Management comment',
        max_length=150,
        null=True,
        editable=False,
        help_text='see also edc.data manager.')

    consent_identifier = models.UUIDField(
        default=uuid4,
        editable=False,
        help_text='A unique identifier for this consent instance')

    objects = ObjectConsentManager()

    consent = ConsentManager()

    on_site = CurrentSiteManager()

    def __str__(self):
        return (f'{self.subject_identifier} v{self.version}')

    def natural_key(self):
        return (self.subject_identifier_as_pk, )

    @property
    def age_at_consent(self):
        """Returns a relativedelta.
        """
        return age(self.dob, self.consent_datetime)

    @property
    def formatted_age_at_consent(self):
        """Returns a string representation.
        """
        return formatted_age(self.dob, self.consent_datetime)

    class Meta:
        abstract = True
        consent_group = None
        get_latest_by = 'consent_datetime'
        unique_together = (
            ('first_name', 'dob', 'initials',
             'version'), ('subject_identifier', 'version'))
        ordering = ('created', )
