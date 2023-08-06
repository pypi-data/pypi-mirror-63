# -*- coding: utf-8 -*-

import collections
import collections.abc
import json
import os
import re
import pytz
import datetime
import logging
import logging.config
import sys
import pwd,grp

from . import jsonlib,configurator

class LogConfig(dict):

    version=1

    class ErrorOnlyFilter(logging.Filter):
        def __init__(self): pass
        def filter(self,record):
            if record.levelno >= logging.ERROR:
                return record
            return None

    def _log_handler_rot(self,fname,formatter="simple"):
        return {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": formatter,
            "filename": os.path.join(self.log_dir,fname),
            "when": "d",
            "interval": 1,
            "backupCount": 3
        }

    def _log_logger(self,*handlers,level="INFO"):
        return {
            "level": level,
            "handlers": handlers,
            "propagate": True
        }

    def __init__(self,config):
        self.log_dir=config.LOG_DIR
        self._config=config
        dict.__init__(self)
        self["version"]=self.version
        self["formatters"]=self.get_formatters()
        self["filters"]=self.get_filters()
        self["handlers"]= self.get_handlers()
        self["loggers"]=self.get_loggers()

    def get_formatters(self):
        return {
            "simple": {
                "format": '%(asctime)s [%(levelname)s] %(message)s',
            },
            "with_logger": {
                "format": '%(asctime)s [%(name)s:%(levelname)s] %(message)s',
            }
        }

    def get_filters(self):
        return {
            "error_only": {
                "()": self.ErrorOnlyFilter,
            }
        }
        

    def get_handlers(self):
        if self._config.DAEMON:
            console=self._log_handler_rot("console.log",formatter="with_logger")
            console_error=self._log_handler_rot("errors.log",formatter="with_logger")
            console_error["filters"]=[ "error_only" ]
        else:
            console={
                "class": "logging.StreamHandler",
                "formatter": "with_logger",
                "stream": "ext://sys.stdout",
            }
            console_error={
                "class": "logging.StreamHandler",
                "formatter": "with_logger",
                "stream": "ext://sys.stdout",
                "filters": [ "error_only" ],
            }

        return {
            "console":           console,
            "console_error":     console_error,
            "socketio.log":      self._log_handler_rot("socketio.log"),
            "engineio.log":      self._log_handler_rot("engineio.log"),
            "common.log":        self._log_handler_rot("common.log"),
            "onshow.log":        self._log_handler_rot("onshow.log"),
            "pages_access.log":  self._log_handler_rot("pages_access.log"),
            "pages_error.log":   self._log_handler_rot("pages_error.log"),
            
        }

    def get_loggers(self):
        return {
            "socketio":                             self._log_logger("socketio.log",level="INFO"),
            "engineio":                             self._log_logger("socketio.log",level="INFO"),
            self._config.LIB_NAME+".server.onshow": self._log_logger("onshow.log"),
            self._config.LIB_NAME+".pages.access":  self._log_logger("pages_access.log"),
            self._config.LIB_NAME+".pages.error":   self._log_logger("pages_error.log"),
            "microdaemon.server.server.onshow":     self._log_logger("onshow.log"),
            "microdaemon.server.pages.access":      self._log_logger("pages_access.log"),
            "microdaemon.server.pages.error":       self._log_logger("pages_error.log"),
            "microdaemon.server.decorators.access": self._log_logger("pages_access.log"),
            "microdaemon.server.decorators.error":  self._log_logger("pages_error.log"),
            "root":                                 self._log_logger("console","common.log"),
            "": {
                "level": "ERROR",
                "handlers": ["console_error"],
                "propagate": True
            },
        }


class Config(object):

    class ConfigurationError(Exception): pass

    log_config_class=LogConfig

    @property
    def _name(self):
        t=self.__module__.split(".")
        if len(t) == 1: return t[0]
        return ".".join(t[:-1])

    STATIC_REL_PATH = "static"  #: Static path, relative to base url (=script name in wsgi invocation)
    FAVICON="img/logo.png" #: Favicon, relative to static path

    ## change even in share/isambard/htdocs static files
    COPY_NAME="Gianozia Orientale"
    COPY_URL="http://www.gianoziaorientale.org"

    BASE_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    MD_TEMPLATE_DIR=os.path.join(BASE_DIR,"share","microdaemon","templates")
    MD_STATIC_DIR=os.path.join(BASE_DIR,"share","microdaemon","static")
    MD_LESS_DIR=os.path.join(BASE_DIR,"share","microdaemon","sources","less")

    CMD_LESSC="/usr/bin/lessc"

    SERVER_NAME="Microdaemon"

    UID=None
    GID=None
    UMASK=None
    DEBUG=False
    DAEMON=True
    USER=pwd.getpwuid(os.getuid())
    GROUP=grp.getgrgid(os.getgid())
    UMASK=os.umask(0) # a bit odd, but that's
    os.umask(UMASK)

    ## wsgi server
    HOST="localhost"
    PORT=7373

    ## business logic
    TZ_LABEL="Europe/Rome"      #: Timezone name
    LOCALE="it-IT"              #: Locale definition

    PID_SUFFIX=".pid"

    def __init__(self):
        ## daemon
        self.LIB_NAME=self._name
        self.VAR_DIR=self._base_rel("var",self._name)
        self.CONFIG_DIR=self._base_rel("etc",self._name)
        self.CONFIG_FILE=self._config_rel(self._name+".conf")
        self.PID_FILE_NAME=self._name+self.PID_SUFFIX

        self.CSS_OUTPUT="css/%s.css" % self._name # relative to STATIC_DIR
        self.LESS_INPUT=self._share_rel("sources","less","%s.less" % self._name)

        self.default=self._get_default()
        self.configurator=configurator.Configurator(self)

    def _get_default(self):
        return {
            ## running mode
            "debug": self.DEBUG,
            "daemon": self.DAEMON,
            ## process
            "var": self._base_rel("var",self._name),
            "etc": self._base_rel("etc",self._name),
            "pid_file_name": self.PID_FILE_NAME,
            "user": self.USER,
            "group": self.GROUP,
            "umask": self.UMASK,
            ## wsgi server
            "host": self.HOST,
            "port": self.PORT,
            ## business logic
            "time_zone": self.TZ_LABEL,
            "locale": self.LOCALE,
        }

    def setup_config(self,options):
        configuration_file=options.conf_file

        with open(configuration_file) as fd:
            try:
                conf=jsonlib.json_fd_load(fd)
            except json.decoder.JSONDecodeError as e:
                raise self.ConfigurationError(e)

        self.CONFIG_FILE=configuration_file

        if options.port is not None:
            self.PORT=options.port
        elif "port" in conf:
            self.PORT=conf["port"]

        if options.host is not None:
            self.HOST=options.host
        elif "host" in conf:
            self.HOST=conf["host"]

        if options.daemon is not None:
            self.DAEMON=options.daemon
        elif "daemon" in conf:
            try:
                self.DAEMON=bool(conf["daemon"])
            except ValueError as e:
                raise self.ConfigurationError(e)

        if "time_zone" in conf:
            self.TZ_LABEL=conf["time_zone"]
            try:
                self.TZ
            except ValueError as e:
                raise self.ConfigurationError(e)

        if "debug" in conf:
            try:
                self.DEBUG=bool(conf["debug"])
            except ValueError as e:
                raise self.ConfigurationError(e)

        if "user" in conf:
            if os.getuid()==0 or os.geteuid()==0:
                if isinstance(conf["user"],int):
                    self.USER=pwd.getpwuid(conf["user"])
                else:
                    self.USER=pwd.getpwnam(conf["user"])

        if "group" in conf:
            if os.getgid()==0 or os.getegid()==0:
                if isinstance(conf["group"],int):
                    self.GROUP=pwd.getgrgid(conf["group"])
                else:
                    self.GROUP=pwd.getgrnam(conf["group"])

        if "umask" in conf:
            try:
                self.UMASK=int(conf["umask"],base=8)
            except ValueError as e:
                raise self.ConfigurationError(e)

        if "locale" in conf:
            self.LOCALE=conf["locale"]

        if "var" in conf:
            if conf["var"].startswith("/"):
                self.VAR_DIR=conf["var"]
            else:
                self.VAR_DIR=self._base_rel(*(conf["var"].split("/")))

            os.makedirs(self.VAR_DIR,exist_ok=True)

        if "etc" in conf:
            if conf["etc"].startswith("/"):
                self.CONFIG_DIR=conf["etc"]
            else:
                self.CONFIG_DIR=self._base_rel(*(conf["etc"].split("/")))

        if "config_dir" in conf:
            if conf["config_dir"].startswith("/"):
                self.CONFIG_DIR=conf["config_dir"]
            else:
                self.CONFIG_DIR=self._base_rel(*(conf["config_dir"].split("/")))

        if "pid_file_name" in conf:
            self.PID_FILE_NAME=conf["pid_file_name"]

        conf=self.local_setup_config(conf,options)

        os.makedirs(self._var_rel("run"),exist_ok=True)

        self.configurator.reset_params()

        return conf

    def local_setup_config(self,conf,options):
        return conf

    def setup_log(self):
        os.makedirs(self.LOG_DIR,exist_ok=True)
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s [%(name)s:%(levelname)s] %(message)s")
        logging.config.dictConfig(self.log_config_class(self))

    def _base_rel(self,*rel):
        return os.path.join(self.BASE_DIR,*rel)

    def _var_rel(self,*rel):
        return os.path.join(self.VAR_DIR,*rel)

    def _db_rel(self,*rel):
        return os.path.join(self.VAR_DIR,"db",*rel)

    def _config_rel(self,*rel):
        return os.path.join(self.CONFIG_DIR,*rel)

    def _share_rel(self,*rel):
        return os.path.join(self.BASE_DIR,"share",self._name,*rel)

    @property
    def COPY_YEAR(self):
        year=datetime.datetime.today().year
        if year==2018:
            copy_year="2018" 
        else:
            copy_year="2018-%d" % year
        return copy_year

    @property
    def VERSION(self):
        version_file=self._base_rel("VERSION")
        try:
            with open(version_file, "r") as fd:
                version=fd.read().strip()      
        except FileNotFoundError as e:
            version="0.0.1"
        return version

    @property
    def TZ(self):
        return pytz.timezone(self.TZ_LABEL)

    @property
    def LOG_DIR(self): return self._var_rel("log")                     

    @property
    def WORKING_DIR(self): return self.VAR_DIR

    @property
    def PID_FILE(self): return self._var_rel("run",self.PID_FILE_NAME)                     

    @property
    def DATABASE_DIR(self): return self._var_rel("db")                     

    @property
    def DEFAULT_DIR(self): return self._db_rel("default")

    @property
    def TEMPLATE_DIR(self): return self._share_rel("templates")                #: Template dir

    @property
    def STATIC_DIR(self): return self._share_rel("static")                     #: Static dir

    @property
    def STAGE_DIR(self): return self._db_rel("stage")                     

    @property
    def STORAGE_SERIALIZER_CHANNELS(self): return self._db_rel("serializer_channels")

    @property
    def SEQUENCES_DIR(self): return self._db_rel("sequences")



