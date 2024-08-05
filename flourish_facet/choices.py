from edc_constants.constants import OTHER, MALE, FEMALE, DONT_KNOW, ALIVE, DEAD, PARTICIPANT, UNKNOWN
from django.utils.translation import ugettext_lazy as _
from edc_constants.constants import YES, NO, NEG, POS, IND, FAILED_ELIGIBILITY, OFF_STUDY, ON_STUDY, NOT_APPLICABLE
from edc_visit_tracking.constants import COMPLETED_PROTOCOL_VISIT, MISSED_VISIT, \
    LOST_VISIT, SCHEDULED, UNSCHEDULED


REASONS_UNWILLING_FACET = (
    ('unable_to_provide_consent ', 'Mother unavailable to provide consent'),
    ('refuses_to_provide_consent', 'Mother refuses to provide consent'),
    ('unwilling_to_give_personal_info',
     'Unwilling to give Personal Info'),
    ('cannot_come_to_clinic', 'Cannot physically come to clinic'),
    ('not_interested', 'Not Interested in participating'),
    (OTHER, 'Other (Specify'),)

IDENTITY_TYPE = (
    ('country_id', 'Country ID number'),
    ('country_id_rcpt', 'Country ID receipt'),
    ('passport', 'Passport'),
    (OTHER, 'Other'),
)

GENDER_OTHER = (
    (MALE, _('Male')),
    (FEMALE, _('Female')),
    (OTHER, _('Other')),
)

CHILD_IDENTITY_TYPE = (
    ('country_id', 'Country ID number'),
    ('birth_cert', 'Birth Certificate number'),
    ('country_id_rcpt', 'Country ID receipt'),
    ('passport', 'Passport'),
    (OTHER, 'Other'),
)

CHILD_CONSENT_VERSION = (
    ('1', 'Consent version 1'),
    ('2', 'Consent version 2'),
    ('2.1', 'Consent version 2.1'),
    ('3', 'Consent version 3')
)

HIGHEST_EDUCATION = (
    ('pre_school', 'Pre-school'),
    ('no_schooling', 'No Schooling '),
    (OTHER, 'Other'),
)

YES_NO_DNK = (
    (YES, YES),
    (NO, NO),
    (DONT_KNOW, 'Do not know')
)

POS_NEG_IND = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (IND, 'Indeterminate'),
)

AGE_BREASTFEEDING_ENDED = (
    ('older_than_6_weeks', 'Older than 6 weeks'),
    ('under_6_weeks', 'Under six weeks'),
    (DONT_KNOW, 'Do not know')

)

VISIT_REASON = [
    (SCHEDULED, 'Scheduled visit/contact'),
    (MISSED_VISIT, 'Missed Scheduled visit'),
    (UNSCHEDULED,
     'Unscheduled visit at which lab samples or data are being submitted'),
    (LOST_VISIT, 'Lost to follow-up (use only when taking subject off study)'),
    (FAILED_ELIGIBILITY, 'Subject failed enrollment eligibility'),
    (COMPLETED_PROTOCOL_VISIT, 'Subject has completed the study')
]

INFO_PROVIDER = (
    ('MOTHER', 'Mother'),
    ('GRANDMOTHER', 'Grandmother'),
    ('FATHER', 'Father'),
    ('GRANDFATHER', 'Grandfather'),
    ('SIBLING', 'Sibling'),
    ('self', 'Self'),
    (OTHER, 'Other'),
)

VISIT_STUDY_STATUS = (
    (ON_STUDY, 'On study'),
    (OFF_STUDY,
     'Off study-no further follow-up (including death); use only '
     'for last study contact'),
)
ALIVE_DEAD_UNKNOWN = (
    (ALIVE, 'Alive'),
    (DEAD, 'Dead'),
    (UNKNOWN, 'Unknown'),
)

VISIT_INFO_SOURCE = [
    (PARTICIPANT, 'Clinic visit with participant'),
    ('participant_home', 'Participant home'),
    ('other_contact',
     'Other contact with participant (for example telephone call)'),
    ('other_doctor',
     'Contact with external health care provider/medical doctor'),
    ('family',
     'Contact with family or designated person who can provide information'),
    ('chart', 'Hospital chart or other medical record'),
    (OTHER, 'Other')]

WEIGHT_RECORDED = [
    ('with_infant_scale', 'With infant scale'),
    ('with_adult_scale,', 'With adult scale,')
]

OCCURENCES = [
    ('never', 'Never'),
    ('rarely/sometimes', 'Rarely/Sometimes'),
    ('often', 'Often'),
]

MATERNAL_VISIT_STUDY_STATUS = (
    (ON_STUDY, 'On study'),
    (OFF_STUDY,
     'Off study-no further follow-up (including death); use only '
     'for last study contact'),
)

DRUG_COMBINATION = [
    ('TDF_+_3TC_+EFV', 'TDF + 3TC +EFV'),
    ('TDF_+_3TC_+_DTG', 'TDF + 3TC+ DTG'),
    ('AZT_+_3TC_+_EFV', 'AZT + 3TC +EFV'),
    ('AZT_+ 3TC_+_ATV/r', 'AZT + 3TC +ATV/r'),
    ('TDF_+_3TC_+_ATV/r', 'TDF + 3TC + ATV/r'),
    ('TDF_+_3TC_+_LPV/r', 'TDF + 3TC + LPV/r'),
    (OTHER, 'Other regimen, specify')
]

REASONS_REGIMEN_CHANGE = [
    ('drug_resistance', 'Drug resistance'),
    ('side_effects', 'Side Effects'),
    ('recommendations_in_pregnancy', 'Recommendations in pregnancy'),
    (DONT_KNOW, 'Do not know'),
    (OTHER, 'Other (Specify)'),
]

OCCURENCES_MORE = [
    ('never', 'Never'),
    ('rarely', 'Rarely'),
    ('sometimes', 'Sometimes'),
    ('fairly_often', 'Fairly often'),
    ('frequently', 'Frequently'),
    (NOT_APPLICABLE, 'Not applicable'),
]

REASON_CHILD_NOT_TESTED = [
    (NOT_APPLICABLE, 'Not applicable'),
    ('not_sought_clinic',
     'Mother or caregiver have not yet sought to clinic'),
    ('could_not_book',
     'Mother or caregiver went to the clinic but could not get a booking'),
    ('health_worker_na',
     'Health worker responsible for testing not available'),
    ('father_not_willling',
     'Child’s father does not want child to be tested'),
    ('family_not_willling',
     'Family other than child’s father does not want child to be tested'),
    ('work_constraints',
     'Mother or caregiver work constraints'),
    ('no_transport_fare',
     'Mother or caregiver did not have transport fare to go to clinic for testing'),
    ('hiv_testing_kits_na', 'HIV Testing kits not available'),
    ('mother_forgot',
     'Mother or caregiver forgot and did not take child for testing'),
    ('d_m_not_working', 'Diagnostic machines not working'),
    ('no_apparent_reason', 'No apparent reason'),
    (OTHER, 'Other (Specify)'),
]

REASON_RESULTS_UNAVAILABLE = [
    ('results_pending',
     'Results still pending'),
    ('results_misplaced_clinic',
     'Clinic misplaced the results'),
    ('results_misplaced_parent',
     'Parent misplaced the results'),
    ('results_never_collect',
     'Results never Collected'),
    (OTHER, 'Other (Specify)'),
]

TEST_VENUE = [
    ('local_clinic',
     'Local clinic'),
    ('facet_study',
     'FACET study'),
    ('test_denied',
     'No ,I do not want to test my child'),
]

LOCATION_INTERVIEW = [
    ('facet_clinic_site', 'Facet clinic site'),
    ('ra_office', 'RA Office'),
    (OTHER, 'Other (Specify)'),
]

LANGUAGES_BOTH = [
    ('setwana', 'Setswana'),
    ('english', 'English'),
    ('both', 'Both'),
]

COMPLETE_UNVERIFIED = [
    ('incomplete', 'Incomplete'),
    ('unverified', 'Unverified'),
    ('complete', 'Complete')
]

QUALITATIVE_TYPE = [
    ('Focus_group_discuss', 'Focus group discussion'),
    ('in_depth_interview', 'In-depth interview')
]
TRANSCRIPTION_HOURS = [
    ('2_4_hours', '2-4 hours'),
    ('4_6_hours', '4-6 hours'),
    ('6_8_hours', '6-8 hours'),
    ('8_10_hours', '8-10 hours'),
    ('10_+_hours', '10+ hours'),
]

FACET_STAFF = [
    ('kedi', 'Kedi'),
    ('irene', 'Irene'),
    ('sam', 'Sam'),
    ('gosego', 'Gosego'),
    ('martha', 'Martha'),
]

OFTEN_DONE = [
    ('never', 'Never'),
    ('very_rarely', 'Very Rarely'),
    ('less_half_time', 'Less than half the time'),
    ('about_half_time', 'About half the time'),
    ('more_half_time', 'More than half the time'),
    ('almost_always', 'Almost always'),
    ('always', 'Always'),
    (NOT_APPLICABLE, 'NA(Does not apply)'),
]
