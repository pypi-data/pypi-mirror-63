import logging

from microdaemon import jsonlib
from . import responses,exceptions,pages

logger_access=logging.getLogger("%s.access" % __name__)
logger_error=logging.getLogger("%s.error" % __name__)

def log_decorator(func):
    def decorated(request):
        response=func(request)
        if isinstance(response,responses.StaticResponse):
            return response
        if request.accept=="application/json": 
            return response
        params=[request.method,
                response.status,
                request.path,
                "Accept: "+request.accept]
        if request.querystring:
            params.append("Query:")
            params.append(request.querystring)
        if request.cookies:
            params.append("Cookies:")
            params.append(request.cookies)
        logger_access.info(" ".join([str(x) for x in params]))
        if response.status.startswith("5"):
            logger_error.error(" ".join([str(x) for x in params]))
        return response
    return decorated

def exception_decorator(server):
    def decorator(func):
        def decorated(request):
            try:
                try:
                    response=func(request)
                except exceptions.Http400BadRequest as e:
                    page=pages.Error400Page(server,e)
                    response=page.dispatch(request)
                except exceptions.Http401Unauthorized as e:
                    page=pages.Error401Page(server,e)
                    response=page.dispatch(request)
                except exceptions.Http403Forbidden as e:
                    page=pages.Error403Page(server,e)
                    response=page.dispatch(request)
                except exceptions.Http405MethodNotAllowed as e:
                    page=pages.Error405Page(server,e)
                    response=page.dispatch(request)
                except exceptions.Http404NotFound as e:
                    page=pages.Error404Page(server,e)
                    response=page.dispatch(request)
                except jsonlib.JsonSerializerError as e:
                    page=pages.Error500Page(server,e)
                    response=page.dispatch(request)
                    logger_error.exception("Json Serializer Error")
            except Exception as e:
                page=pages.Error500Page(server,e)
                response=page.dispatch(request)
                logger_error.exception("Generic Error")
            return response
        return decorated
    return decorator
