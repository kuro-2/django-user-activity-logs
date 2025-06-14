import json
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import UserActivityLog

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="pass")


@pytest.fixture
def client(user):
    c = APIClient()
    c.login(username="alice", password="pass")
    return c


def test_model_creation(user):
    log = UserActivityLog.objects.create(user=user, action="LOGIN")
    assert str(log).startswith("alice - LOGIN")


def test_post_and_get(client):
    url = reverse("logs-list")
    # POST
    res = client.post(url, {"action": "LOGIN"})
    assert res.status_code == 201
    # GET
    res = client.get(url)
    assert len(res.data) == 1


def test_filtering(client):
    base = timezone.now()
    UserActivityLog.objects.create(user=client.handler._force_user, action="LOGIN")
    UserActivityLog.objects.create(
        user=client.handler._force_user,
        action="UPLOAD_FILE",
        timestamp=base - timedelta(days=2),
    )
    url = reverse("logs-list")
    assert client.get(f"{url}?action=LOGIN").json()[0]["action"] == "LOGIN"


def test_status_transition(client):
    log_id = client.post(reverse("logs-list"), {"action": "LOGIN"}).json()["id"]
    res = client.patch(
        reverse("logs-transition", args=[log_id]), {"status": "IN_PROGRESS"}
    )
    assert res.data["status"] == "IN_PROGRESS"


def test_caching(client, settings, mocker):
    url = reverse("logs-list")
    client.post(url, {"action": "LOGIN"})  # creates 1 log
    client.get(url)  # populates cache

    # spy on cache backend
    spy = mocker.spy(settings.CACHES["default"]["OPTIONS"]["CLIENT_CLASS"], "get")
    client.get(url)  # second call should hit cache
    assert spy.call_count >= 1
