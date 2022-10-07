import os
from django.http import HttpRequest, JsonResponse
from functools import wraps
from rest_framework.status import HTTP_401_UNAUTHORIZED
from django.middleware.common import MiddlewareMixin


class WorkflowAuthMiddleware(MiddlewareMixin):
    """Authenticate workflow views."""

    def process_view(self, request, view_func, *_):
        if not getattr(view_func, "workflow_auth_required", False):
            # Not required, passthrough
            return None

        if not self.valid_request(request):
            return JsonResponse({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "unauthorized",
            }, status=HTTP_401_UNAUTHORIZED)

        # All good
        return None

    @staticmethod
    def valid_request(request: HttpRequest) -> bool:
        if "Authorization" not in request.headers:
            return False

        secret = os.getenv("WORKFLOW_TOKEN")
        if secret is None:
            # If we haven't defined a token, we should block all requests just
            # to be safe.
            return False

        if secret != request.headers.get("Authorization"):
            return False

        return True


def workflow_auth_required(view_func):
    """
    Mark a view function as requiring workflow authentication.
    """
    def wrapped(*view_args, **view_kwargs):
        return view_func(*view_args, **view_kwargs)

    wrapped.workflow_auth_required = True
    return wraps(view_func)(wrapped)
