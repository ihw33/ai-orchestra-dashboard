from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp
from github import Github
import os
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.github_client = Github(os.getenv("GITHUB_TOKEN"))

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Check GitHub API rate limit
        rate_limit = self.github_client.get_rate_limit()
        core_rate_limit = rate_limit.core

        remaining = core_rate_limit.remaining
        limit = core_rate_limit.limit

        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Limit"] = str(limit)

        if remaining / limit < 0.1: # 10% remaining
            response.headers["X-RateLimit-Warning"] = "GitHub API rate limit is low (less than 10% remaining)."

        return response
