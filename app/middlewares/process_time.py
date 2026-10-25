"""
Process Time Measurement Middleware.
Appends processing latency to response headers for telemetry and performance profiling.
"""

import time
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

HEADER_PROCESS_TIME = "X-Process-Time-Ms"


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time_ms = (time.perf_counter() - start_time) * 1000.0
        response.headers[HEADER_PROCESS_TIME] = f"{process_time_ms:.2f}"
        return response
