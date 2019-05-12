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
    body = models.TextField(max_length=MAX_BODY_LENGTH)
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
    def get_organization_by_url(self):
        return self.channel_set.organization_set.first()


class IncomingWebhook(BaseModel):
    url = models.CharField(max_length=50,
                           unique=True,
                           default=short_url_token)
    channel = models.ForeignKey(IncomingChannel, on_delete=models.CASCADE)
    objects = IncomingWebhookManager()
