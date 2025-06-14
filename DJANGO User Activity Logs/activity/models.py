from django.conf import settings
from django.db import models


class UserActivityLog(models.Model):
    class Action(models.TextChoices):
        LOGIN = "LOGIN"
        LOGOUT = "LOGOUT"
        UPLOAD_FILE = "UPLOAD_FILE"

    class Status(models.TextChoices):
        PENDING = "PENDING"
        IN_PROGRESS = "IN_PROGRESS"
        DONE = "DONE"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activity_logs",
    )
    action = models.CharField(max_length=20, choices=Action.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)
    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.PENDING
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp:%Y-%m-%d %H:%M}"
