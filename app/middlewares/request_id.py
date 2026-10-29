"""
Correlation & Request ID Middleware.
Attaches a unique UUID to each incoming request for end-to-end distributed tracing.
"""

import uuid
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

HEADER_REQUEST_ID = "X-Request-ID"


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Check if caller supplied an existing trace ID, otherwise generate a new one
        request_id = request.headers.get(HEADER_REQUEST_ID) or str(uuid.uuid4())
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers[HEADER_REQUEST_ID] = request_id
        return response
