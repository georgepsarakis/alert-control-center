from django.db import models
from django.contrib.auth.models import User

MAX_BODY_LENGTH = 1024 ** 2


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(BaseModel):
    name = models.CharField(max_length=100)


class Team(BaseModel):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class EscalationPolicy(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'escalation_policies'


class EscalationRule(BaseModel):
    name = models.CharField(max_length=100)


class EscalationRulePolicy(BaseModel):
    rule = models.ForeignKey(EscalationRule, on_delete=models.CASCADE)
    policy = models.ForeignKey(EscalationPolicy, on_delete=models.CASCADE)


class Alert(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    received_at = models.DateTimeField(auto_now_add=True)


class Assignee(BaseModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    is_team = models.BooleanField(blank=False)


class AlertAssignee(BaseModel):
    assignee = models.ForeignKey(Assignee, on_delete=models.CASCADE)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)


class IncomingChannel(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=MAX_BODY_LENGTH)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


from alert_control_center.utils.url import short_url_token
from django.db import models


class IncomingWebhookManager(models.Manager):
    def from_url(self, token):
        return self.filter(url=token).first()


from django.db.models import UniqueConstraint


class AlertVendor(BaseModel):
    name = models.CharField(max_length=50, unique=True)


class IncomingWebhook(BaseModel):
    url = models.CharField(max_length=50,
                           unique=True,
                           default=short_url_token)
    channel = models.ForeignKey(IncomingChannel, on_delete=models.CASCADE)
    vendor = models.ForeignKey(AlertVendor, on_delete=models.CASCADE)
    objects = IncomingWebhookManager()

    class Meta:
        constraints = (
            UniqueConstraint(fields=['url'], name='uq_url'),
        )

    def get_organization(self):
        return self.channel_set.organization_set.first()


import uuid

class IncomingWebhookLog(BaseModel):
    webhook = models.ForeignKey(IncomingWebhook, on_delete=models.CASCADE)
    payload = models.TextField()
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)


class AlertGroup(BaseModel):
    name = models.CharField(max_length=50)


class AlertGroupRule(BaseModel):
    name = models.CharField(max_length=50)
    pattern = None


class IncidentSeverity(BaseModel):
    name = models.CharField(max_length=50)
    ordinal = models.PositiveSmallIntegerField()


class IncidentReport(BaseModel):
    alert_group = models.ForeignKey(AlertGroup, on_delete=models.CASCADE)
    severity = models.ForeignKey(IncidentSeverity, on_delete=models.CASCADE)


class IncidentReportSection(BaseModel):
    incident_report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()


class IncidentTimelineEntry(BaseModel):
    incident_report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)
    occurred_at = models.DateTimeField()
    duration_seconds = models.PositiveIntegerField()
