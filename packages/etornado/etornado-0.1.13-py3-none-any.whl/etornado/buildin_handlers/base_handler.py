import json
import logging
import inspect
from enum import Enum
from tornado.web import RequestHandler
from etornado.error_code_manager import ErrorCode, error_code_manager, ErrorCodeException


class AggregateHttMethodMeta(type):

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.head = cls.process
        cls.get = cls.process
        cls.post = cls.process
        cls.delete = cls.process
        cls.patch = cls.process
        cls.put = cls.process
        cls.options = cls.process


class BaseHandler(RequestHandler, metaclass=AggregateHttMethodMeta):

    def initialize(self, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        for k, v in kwargs.items():
            if hasattr(self, k):
                self.logger.exception("member [%s] has exists", k)
                raise Exception("member [%s] has exists" % k)
            setattr(self, k, v)
        self.url_args = []

    async def process(self, *args, **kwargs):
        method = getattr(self, "do_" + self.request.method.lower(), None)
        self.url_args = args
        ec_exception = ErrorCodeException(ErrorCode.NONE)
        results = None
        if method is None:
            ec_exception = ErrorCodeException(
                    ErrorCode.UNSUPPORTED_METHOD,
                    {"method": self.request.method, "url": self.request.uri})
        else:
            try:
                results = method()
                if inspect.isawaitable(results):
                    results = await results
            except ErrorCodeException as e:
                self.logger.exception("error_code_exception [%s] catched when call [%s],"\
                                      " request[%s], request body[%s]",
                                      e, method, self.request, self.request.body)
                ec_exception = e
            except Exception as e:
                self.logger.exception("exception [%s] catched when call [%s],"\
                                      " request[%s], request body[%s]",
                                      e, method, self.request, self.request.body)
                ec_exception = ErrorCodeException(ErrorCode.UNKNOWN)
        self.send_response(ec_exception, results)

    def send_response(self, ec_exception, results=None):
        response = error_code_manager.format_error_info(
                ec_exception.error_code, **ec_exception.error_info)
        if ec_exception.error_code == ErrorCode.NONE and results is not None:
            response["results"] = results
        self.write(json.dumps({"response": response}, ensure_ascii=False))
        self.finish()
