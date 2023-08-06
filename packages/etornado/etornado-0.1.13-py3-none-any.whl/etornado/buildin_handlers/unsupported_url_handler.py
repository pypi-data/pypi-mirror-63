from etornado.buildin_handlers.base_handler import BaseHandler
from etornado.error_code_manager import ErrorCode, ErrorCodeException


class UnsupportedUrlHandler(BaseHandler):

    def process(self, *args, **kwargs):
        self.send_response(
                ErrorCodeException(ErrorCode.UNSUPPORTED_URL,
                                   {"url": self.request.uri}))
