import contextvars
import time
from uuid import uuid4

from fastapi import Request, Response
from fastapi.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware

REQUEST_UUID = contextvars.ContextVar("request_uuid", default=None)


class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        logger,
    ):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next):
        uuid = uuid4()
        REQUEST_UUID.set(uuid)

        self.logger.warning(
            f"Start request path={request.url.path}; method={request.method}; "
            f"headers={await request.body()}"
        )
        start_time = time.time()

        response: Response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = "{0:.2f}".format(process_time)

        if request.url.path in ["/docs", "/openapi.json"]:
            self.logger.warning(
                f"Request completed in {formatted_process_time}ms; "
                f"Status Code={response.status_code};"
            )
            return response

        res_body = [section async for section in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(res_body))
        res_body = res_body[0].decode()

        self.logger.warning(
            f"Request completed in {formatted_process_time}ms; "
            f"Status Code={response.status_code}; body={res_body};"
        )
        return response
