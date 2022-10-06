import os

from django.http import HttpRequest, JsonResponse
from rest_framework.status import HTTP_401_UNAUTHORIZED


class WorkflowAuthMiddleware:
    """Authenticate workflow views."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if not request.path.endswith("kkmnow/"):
            # Not applicable, passthrough
            return self.get_response(request)

        if not self.valid_request(request):
            return JsonResponse(
                {
                    "status": HTTP_401_UNAUTHORIZED,
                    "message": "unauthorized",
                },
                status=HTTP_401_UNAUTHORIZED,
            )

        return self.get_response(request)

    def valid_request(self, request: HttpRequest) -> bool:
        if "Authorization" not in request.headers:
            return False

        if os.getenv("WORKFLOW_TOKEN", "") != request.headers.get("Authorization"):
            return False

        return True
