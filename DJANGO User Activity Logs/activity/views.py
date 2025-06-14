from django.core.cache import cache
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserActivityLog
from .serializers import UserActivityLogSerializer


class UserActivityLogViewSet(viewsets.ModelViewSet):
    """
    list:
    Return all logs for the authenticated user (filterable).

    create:
    Store a new activity log for the authenticated user.

    partial_update:
    PATCH to change the status (workflow).
    """

    serializer_class = UserActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = UserActivityLog.objects.filter(user=user)

        # filters ?action=LOGIN&start=yyyy-mm-dd&end=...
        action = self.request.query_params.get("action")
        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")
        if action:
            qs = qs.filter(action=action)
        if start and end:
            qs = qs.filter(timestamp__range=[start, end])
        return qs

    # ---------- Caching ----------
    def list(self, request, *args, **kwargs):
        cache_key = f"logs:{request.user.id}:{request.get_full_path()}"
        data = cache.get(cache_key)
        if data:
            return Response(data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)
        return response

    def perform_create(self, serializer):
        instance = serializer.save()
        # Invalidate any cached list for this user
        pattern = f"logs:{self.request.user.id}:*"
        cache.delete_pattern(pattern)

    # ---------- Extra endpoint ----------
    @action(detail=True, methods=["patch"])
    def transition(self, request, pk=None):
        """PATCH /logs/{id}/transition/ with {"status": "IN_PROGRESS"}"""
        log = self.get_object()
        serializer = self.get_serializer(log, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
