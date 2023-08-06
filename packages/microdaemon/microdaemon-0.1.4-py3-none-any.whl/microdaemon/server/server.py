# -*- coding: utf-8 -*-

""" Isambard server, the main isambard object. """

import socketio
import eventlet
import eventlet.wsgi
import urllib.parse
import collections
import mimetypes
import logging
import subprocess
import os.path

mimetypes.add_type('application/json',".map")
mimetypes.add_type('application/x-font-woff2',".woff2")
mimetypes.add_type('application/x-font-opentype',".otf")
mimetypes.add_type('application/x-font-truetype',".ttf")
mimetypes.add_type('text/x-less',".less")

from microdaemon import config,common,channels,threads

from . import pages,exceptions,decorators
from . import request as reqmodule

logger_onshow=logging.getLogger("%s.onshow" % __name__)

class Server(object):
    """Main object. 

    *bus* (channels.Bus)
        Communication bus common to all objects.
    *port* (int)
        Port to bind.
    *host* (str)
        Host to bind.

    A  `Server` object  is  the interface  between user  and
    other components of a Microdaemon. It  run a WSGI server listening on
    host *host* and port *port* (default 7373 on localhost).  The user
    can connect with a  browser to "http://*host*:*port*" and interact
    in this way.

    Attributes:
        *bus* (channels.Bus)
            Communication bus common to all objects.

    """

    class InfoNamespace(socketio.Namespace):
        def __init__(self,server,*args,**kwargs):
            socketio.Namespace.__init__(self,*args,**kwargs)
            self._server=server
            self.size=0

        def on_connect(self,sid, environ):
            common.log('SIO connect %s' % sid)
            self.size+=1

        def on_disconnect(self,sid):
            common.log('SIO disconnect %s' % sid)
            self.size-=1
            if self.size<0: self.size=0

    def _process_css(self): 
        cmd=[
            config.CMD_LESSC, 
            "--include-path=%s" % config.MD_LESS_DIR,
            config.LESS_INPUT,
            os.path.join(config.STATIC_DIR,config.CSS_OUTPUT),
        ]
        res=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if not res.returncode: 
            common.log("Css file %s built" % config.CSS_OUTPUT)
            return
        common.log("Error on processing less file")
        common.log(" ".join(res.args))
        common.log(res.stdout.decode())


    def __init__(self,bus,host="localhost",port=7373):
        self.bus=bus
        self.bus["configuration"]=channels.SimpleChannel()
        self.bus["onshow"]=channels.SimpleChannel()

        self._http_host=host
        self._http_port=port

        self._process_css()

        self.application=decorators.log_decorator(decorators.exception_decorator(self)(self._application))
        self.welcome_message="%s %s Started on http://%s:%d/ " % (config.SERVER_NAME,
                                                                  config.VERSION,
                                                                  self._http_host,
                                                                  self._http_port)

    ### Application

    def _application(self,request):
        page=self.page_factory(request)
        response=page.dispatch(request)
        return response

    def page_factory(self,request):
        """Transform a request in a Page object.

        *request* (Request)
            Request from user.

        Return    a   Page    (or    subclass)    object   or    raise
        pages.Http404NotFound(request) if *request* has no valid path.

        """

        if len(request.path_split)==0: 
            return pages.HomePage(self)

        if request.path.startswith("/"+config.STATIC_REL_PATH):
            obj_path=request.path[len(config.STATIC_REL_PATH)+2:]
            return pages.StaticPage(self,obj_path)

        if len(request.path_split)==1:
            if request.path_split[0] == "favicon.ico":
                obj_path=config.FAVICON
                return pages.StaticPage(self,obj_path)
            if request.path_split[0] == "configurator":
                return pages.ConfiguratorPage(self)
            for req,label,title in [ ("license","gplv3","License"),
                                     ("about","about","About") ]:
                if request.path_split[0] == req:
                    return pages.TextPage(self,label,title)
        raise exceptions.Http404NotFound(request)


    ####################################
    ### main logic

    def start(self):
        """ Main function.

        Run a WSGI simple server with `self.wsgi` as main function.
        """

        common.log(self.welcome_message)
        socket=eventlet.listen((self._http_host, self._http_port))
        eventlet.wsgi.server(socket,
                             self._socketio_decorator(self.wsgi),
                             log_output=False,debug=False)

    def _socketio_decorator(self,wsgi):
        sio=socketio.Server(async_mode="eventlet")
        namespace=self.InfoNamespace(self,"/info")
        sio.register_namespace(namespace)
        self.bus["browser/info"]=channels.BrowserChannel(namespace=namespace)
        return socketio.Middleware(sio,wsgi)

    def wsgi(self,environ, start_response):
        """WSGI function interface.

        *environ* (dict)
            WSGI environ.
        *start_response* (callable)
            WSGI start_response

        Build  a request  around  *environ*, call  `self.application`,
        obtain   a  response   and   call  (as   per  WSGI   protocol)
        `start_response(response.status, response.headers)`.
        Return `response.body_iterable` (as per WSGI protocol).

        """
        request=reqmodule.Request(self,environ)
        response=self.application(request)
        start_response(response.status, response.headers)
        return response.body_iterable

            
