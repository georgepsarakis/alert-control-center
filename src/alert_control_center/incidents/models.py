from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User

from alert_control_center.alerts.models.alerts import Alert, AlertGroup

MAX_BODY_LENGTH = 1024 ** 2


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Incident(BaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField()
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    fingerprint = models.CharField(max_length=64)  # SHA256


class IncidentRelation(BaseModel):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class UserRelation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class IncidentState(IncidentRelation, UserRelation):
    VALID_INCIDENT_STATES = (
        ('IGNORED', 'Ignored'),
        ('INVESTIGATING', 'Investigating'),
        ('CLOSED', 'Closed'),
    )

    state = models.CharField(choices=VALID_INCIDENT_STATES)

    def get_states_mapping(self):
        return dict(self.VALID_INCIDENT_STATES)


class IncidentAssignee(IncidentRelation):
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = (
            UniqueConstraint(fields=['incident_id', 'user_id'],
                             name='uq_incident_user'),
        )


class IncidentGroup(IncidentRelation, UserRelation):
    connected_with = models.ForeignKey(Incident, on_delete=models.CASCADE)


class IncidentCause(IncidentRelation, UserRelation):
    caused_by = models.ForeignKey(Incident, on_delete=models.CASCADE)


class AlertContextProvider(UserRelation):
    name = models.CharField(max_length=50)
    description = models.TextField()


class AlertContextExtractionSettings(BaseModel):
    VALID_HTTP_METHODS = (
        ('GET', 'GET'),
        ('POST', 'POST'),
    )
    provider = models.ForeignKey(AlertContextProvider, on_delete=models.CASCADE)
    dynamic_alert_parameters = models.CharField(max_length=255)
    callback_url = models.CharField()
    http_method = models.CharField()


class AlertContext(IncidentRelation):
    original_payload = models.TextField(max_length=MAX_BODY_LENGTH)
    processed_payload = models.TextField()
    is_processed = models.BooleanField(default=False, null=False)
    provider = models.ForeignKey(AlertContextProvider, on_delete=models.CASCADE)


# https://landing.google.com/sre/sre-book/chapters/postmortem/
class RootCauseAnalysis(IncidentRelation):
    VALID_STATES = (
        ('PENDING', 'Pending'),
        ('UNDER_REVIEW', 'Under Review'),
    )
    state = models.CharField()
    summary = models.TextField()
    impact = models.TextField()


class RootCauseAnalysisCause(UserRelation):
    title = models.CharField(max_length=255)
    root_cause_analysis = models.ForeignKey(RootCauseAnalysis, on_delete=models.CASCADE)


class RootCauseAnalysisAuthor(UserRelation):
    root_cause_analysis = models.ForeignKey(RootCauseAnalysis)


class RootCauseTimeline(UserRelation):
    description = models.TextField()
    event_time = models.DateTimeField(null=False)
    duration_seconds = models.PositiveIntegerField()


class ServiceLevelAgreement(UserRelation):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    total_downtime = models.TimeField(default=None, null=True)
    accepted_downtime = models.TimeField(null=False)
    accepted_downtime_interval = models.Timefield(null=False)
    frequency = models.PositiveIntegerField(default=0)
    violations = models.PositiveIntegerField(default=0)


class IncidentSeverity(BaseModel):
    name = models.CharField(max_length=50)
    ordinal = models.PositiveSmallIntegerField()


# TODO: most models should probably have a User relation
class IncidentResolutionAction(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=50, unique=True)


class IncidentResolution(BaseModel):
    alert_group = models.ForeignKey(AlertGroup, on_delete=models.CASCADE)
    severity = models.ForeignKey(IncidentSeverity, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    action = models.ForeignKey(IncidentResolutionAction)
    occurred_at = models.DateTimeField(auto_now_add=True)

