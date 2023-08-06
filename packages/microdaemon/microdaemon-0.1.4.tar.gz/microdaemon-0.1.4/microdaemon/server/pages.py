# -*- coding: utf-8 -*-

"""Pages for microdaemon Server. 

A page is the abstraction of something returned to user.

The    server   build    a   page,    therefore   call    the   method
`page.dispatch(request)` to obtain a response.

"""

import datetime
import jinja2
import os.path
import abc
import logging
import traceback
import pickle
import http.cookiejar
import pytz

from microdaemon import config,common,jsonlib,channels,configurator
from . import responses,exceptions


########################################################################
## Pages

class Page(abc.ABC):
    """Abstract class.

    *server* (server.IsambardServer)
        The server.

    Page provides a method `dispatch`  for all subclasses and requests
    that all subclasses implement a `get_handler` method.

    """

    def __init__(self,server):
        self._server=server

    @abc.abstractmethod
    def get_handler(self,request): 
        """Return the callable that can handle this request.

        *request* (server.Request)
            A request object

        Return a callable with  signature response=f(request) or raise
        a Http405MethodNotAllowed(request) exception if the request is
        invalid.

        """
        raise exceptions.Http405MethodNotAllowed(request)

    def dispatch(self,request):
        """ Build the response for the request.

        *request* (server.Request)
            The client request.

        Return the response (responses.Response) or raise appropriate exception.
        """

        handler=self.get_handler(request)
        response=handler(request)
        if not request.cookies: return response
        for key in request.cookies:
            if key!="index_panel": continue
            response.add_cookie(responses.Cookie(key,request.cookies[key]))
        return response

class StaticPage(Page):
    """Page for static resource.

    *server* (server.IsambardServer)
        The server.
    *obj_path* (str)
        The path of static resource, relative to `config.STATIC_DIR`.

    HTTP  method  accepted:

       GET, served  by `self.get()`. 

    Response:

        `responses.StaticResponse`.

    Exception:

        `Http405MethodNotAllowed`
             if the http method is not *GET*;
        `Http404NotFound`
             if the resource requested is not available.

    """

    def __init__(self,server,obj_path):
        self._obj_path=obj_path
        Page.__init__(self,server)

    def get_handler(self,request):
        if request.method!="GET":
            raise exceptions.Http405MethodNotAllowed(request)
        return self.get

    def _get_path(self):
        file_path=os.path.join(config.STATIC_DIR,self._obj_path)
        if not os.path.isfile(file_path):
            file_path=os.path.join(config.MD_STATIC_DIR,self._obj_path)
            if not os.path.isfile(file_path):
                return None
        if file_path.startswith(".") or "/." in file_path:
            return None
        return file_path

    def get(self,request):
        """ Handler for GET. """
        file_path=self._get_path() 
        if file_path is None:
            raise exceptions.Http404NotFound(request)
        response=responses.StaticResponse(file_path)
        return response

class ThumbnailPage(StaticPage):
    def __init__(self,server,media_object):
        StaticPage.__init__(self,server,media_object.thumbnail_path)
        self._object=media_object

    def _get_path(self):
        return self._object.thumbnail_path

class TemplatePage(Page):
    """ Generate a page with a jinja2 template.

    HTTP  method  accepted:

       GET, served  by `self.get()`. 

    Response:

        `responses.Response`.

    Exception:

        `Http405MethodNotAllowed`
             if the http method is not *GET*;

    """

    template_name="418.html"

    _page_title=""
    @property
    def title(self):
        """ Full title of the page  (to place in "title" element of html)."""
        if not self._page_title:
            return config.SERVER_NAME
        return config.SERVER_NAME+": "+self._page_title

    def _apply_template(self,template_name,context):
        env=jinja2.Environment(
            loader=jinja2.FileSystemLoader([
                config.TEMPLATE_DIR,
                config.MD_TEMPLATE_DIR
            ])
        )
        template=env.get_template(template_name)
        T=template.render(**context)
        T=T.encode('utf-8')
        return T

    def get_context(self,request):
        """ Generate the context for the template."""
        context={
            "locale": config.LOCALE,
            "server_name": config.SERVER_NAME,
            "title": self.title,
            "base_url": request.script,
            "static_url": request.script+"/"+config.STATIC_REL_PATH,
            "version": config.VERSION,
            "copy_name": config.COPY_NAME,
            "copy_url": config.COPY_URL,
            "copy_year": config.COPY_YEAR,
        }
        return context

    def get_handler(self,request):
        if request.method!="GET":
            raise exceptions.Http405MethodNotAllowed(request)
        return self.get

    _status="200 OK"
    def get(self,request):
        """ Handler for GET. """
        context=self.get_context(request)
        response=responses.Response(self._apply_template(self.template_name,context),
                                    status=self._status)
        return response

class TextPage(TemplatePage):
    template_name="text.html"

    def __init__(self,server,label,title):
        TemplatePage.__init__(self,server)
        self._label=label
        self._title=title

    @property
    def title(self):
        """ Full title of the page  (to place in "title" element of html)."""
        if not self._page_title:
            return config.SERVER_NAME
        return config.SERVER_NAME+": "+self._title

    def get_context(self,request):
        context=TemplatePage.get_context(self,request)
        context["label"]=self._label
        return context

class ErrorPage(TemplatePage):
    """ Generate an error page.

    HTTP  method  accepted:

       all, served  by `self.get()`. 

    """

    _page_title="Error"
    template_name="error.html"

    def __init__(self,server,exception):
        self.exception=exception
        TemplatePage.__init__(self,server)

    def get_context(self,request):
        context=TemplatePage.get_context(self,request)
        context["status"]=self._status
        context["error"]=str(self.exception)
        return context

    def get_handler(self,request):
        # Error serves all method, not just GET
        return self.get

class Error404Page(ErrorPage):
    """ Generate an error 404 page."""

    _status="404 Not Found"

class Error400Page(ErrorPage):
    """ Generate an error 400 page."""

    _status="400 Bad Request"

class Error401Page(ErrorPage):
    """ Generate an error 401 page."""

    _status="401 Unauthorized"

class Error403Page(ErrorPage):
    """ Generate an error 403 page."""

    _status="403 Forbidden"

class Error405Page(ErrorPage):
    """ Generate an error 405 page."""

    _status="405 Method Not Allowed"

class Error500Page(ErrorPage):
    """ Generate an error 500 page."""

    _status="500 Internal Server Error"

    def _apply_template(self,template_name,context):
        txt="<html><head><title>{{ title }}</title></head>"
        txt+="<body><h1>Server Error</h1>"
        try:
            debug=config.DEBUG
        except Exception as e:
            debug=False
        if debug:
            txt+="<pre>"
            txt+="{{ stacktrace }}"
            txt+="</pre>"
        txt+="</body></html>"

        template = jinja2.Template(txt)

        T=template.render(**context)
        T=T.encode('utf-8')
        return T

    def get_context(self,request):
        """ Generate the context for the template."""
        context={
            "title": "%s: %s" % (config.SERVER_NAME,self._status),
            "stacktrace": traceback.format_exc()
        }
        return context

class HomePage(TemplatePage):
    """ Generate the home page."""

    template_name="index.html"

    def get_context(self,request):
        context=TemplatePage.get_context(self,request)
        return context

class ConfiguratorPage(TemplatePage):
    """ Generate the configurator page."""

    template_name="configurator.html"
    _page_title="Configurator"

    def get_context(self,request):
        context=TemplatePage.get_context(self,request)
        context["configurator"]=config.configurator
        return context

class ObjectListPage(TemplatePage):
    template_name="object_list.html"

    def __init__(self,server,collection):
        TemplatePage.__init__(self,server)
        self._collection=collection

    def get_context(self,request):
        context=TemplatePage.get_context(self,request)
        context["collection"]=self._collection
        return context

class MediaCollectionPage(ObjectListPage):
    template_name="media_collection.html"

class JsonDataPage(Page,abc.ABC):
    """ Abstract class for output related json data pages.

    *server* (server.IsambardServer)
        The server.

    HTTP  method  accepted:

       GET with accept="application/json", served  by `self.get_json()`. 

    Response:

        `responses.JsonResponse`
            when data are available;
        `responses.FoundResponse`
            when data are loading.

    Exception:

        `Http405MethodNotAllowed`
             if the http method is not *GET* or accept is not "application/json";
        `Http404NotFound`
             if requested data cannot be retrieved.

    """
    _retry_after=2 # secs

    def __init__(self,server): 
        Page.__init__(self,server)

    def get_handler(self,request):
        if (request.method=="GET") and (request.accept=="application/json"):
            return self.get_json
        raise exceptions.Http405MethodNotAllowed(request)

    @abc.abstractmethod
    def data(self,request):
        """ Generate data to return to the user.

        *request* (server.Request)
            The client request.

        Return a python object to serialize. """

        return None

    def get_json(self,request):
        """ Handle a GET request with accept="application/json"."""
        data=self.data(request)
        response=responses.JsonResponse(data)
        return response

class ActionPage(Page,abc.ABC):
    """Abstract class for pages requesting an action.

    *server* (server.IsambardServer)
        The server.

    An  ActionPage  implements  the PRG  (post/redirect/get)  pattern:
    after doing an  action, it returns a  `RedirectResponse`. The only
    method accepted is POST.

    HTTP  method  accepted:

       POST, served  by `self.post()`. 

    Response:

        `responses.RedirectResponse`.

    Exception:

        `Http405MethodNotAllowed`
             if the http method is not *POST*.

    """

    _success_url="/"

    def get_handler(self,request):
        if request.method!="POST":
            raise exceptions.Http405MethodNotAllowed(request)
        return self.post
    
    @abc.abstractmethod
    def action(self,request):
        """ Perform action requested by the user.

        *request* (server.Request)
            The client request. """
        pass

    def post(self,request):
        """ Handle a POST request."""
        self.action(request)
        response=responses.RedirectResponse(self._success_url)
        return response



