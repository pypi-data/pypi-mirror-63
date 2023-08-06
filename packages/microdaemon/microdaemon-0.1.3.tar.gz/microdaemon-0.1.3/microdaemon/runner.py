import eventlet
eventlet.monkey_patch()

import prctl
import sys
import os
import signal
import argparse
import resource
import pwd,grp

from microdaemon import config

class Main(object):
    process_name = None
    config = None

    def __init__(self):
        if self.process_name is None:
            self.process_name=sys.argv[0].split('/')[-1]
        prctl.set_name(self.process_name)
        prctl.set_proctitle("%s %s" % (self.process_name," ".join(sys.argv[1:])))
        if self.config is not None:
            config.setup(self.config)
        self.parser=self.get_parser()
        self.options=None

    def get_parser(self):
        parser = argparse.ArgumentParser(description="Video/foto slidescreen")
        parser.add_argument('--version', action='version', version='%%(prog)s %s' % config.VERSION)

        parser.add_argument("-p", "--port", dest="port", 
                            type=int,
                            help="port to bind (default: %s)" % config.PORT, 
                            metavar="PORT")
        
        parser.add_argument("-i", "--host", dest="host", 
                            type=str,
                            help="host to bind (default: %s)" % config.HOST,
                            metavar="IP")
        
        parser.add_argument("-c", "--configuration-file", dest="conf_file", 
                            default=config.CONFIG_FILE,
                            type=str,
                            help="configuration file (default: %s)" % config.CONFIG_FILE, 
                            metavar="FILE")
        
        parser.add_argument("-D", "--daemon", dest="daemon", action="store_const",const=True,
                            help="run in daemon mode")
        
        parser.add_argument("-I", "--no-daemon", dest="daemon", action="store_const",const=False,
                            help="don't run in daemon mode")

        parser.add_argument("-K", "--kill", dest="kill", action="store_true",
                            help="kill running process")

        return parser

    def get_options(self):
        options=self.parser.parse_args()
        options.conf_file=os.path.abspath(options.conf_file)
        return options

    def _set_options(self):
        self.options=self.get_options()
        self.config.setup_config(self.options)
        self.config.setup_log()
        signal.signal(signal.SIGINT,self._signal_stop)
        signal.signal(signal.SIGTERM,self._signal_stop)
        signal.signal(signal.SIGQUIT,self._signal_stop)

    def _signal_stop(self,signum,trace):
        print(signum)
        self.stop()

    def options_no_start(self):
        if self.options.kill:
            with open(self.config.PID_FILE,"r") as fd:
                pid=int(fd.read().strip())
            os.kill(pid,signal.SIGTERM)
            sys.exit()

    def start(self):
        self._set_options()
        if self.config.DEBUG:
            common.log("Debug is enabled")
        self.options_no_start()
        if os.path.exists(self.config.PID_FILE):
            print("Error: Pid file %s exists. Abort" % self.config.PID_FILE )
            sys.exit()
        if self.config.DAEMON:
            self._daemon()
        with open(self.config.PID_FILE,"w") as fd:
            fd.write(str(os.getpid()))
        self.run()

    def stop(self,*args,**kwargs):
        try:
            os.remove(self.config.PID_FILE)
        except OSError as e:
            pass
        sys.exit(*args,**kwargs)

    def _daemon(self):
        daemon_stdout=open(os.path.join(self.config.LOG_DIR,"stdout.log"),"w")
        daemon_stderr=open(os.path.join(self.config.LOG_DIR,"stderr.log"),"w")

        core_resource = resource.RLIMIT_CORE
        resource.getrlimit(core_resource)
        core_limit = (0, 0)
        resource.setrlimit(core_resource, core_limit)

        os.umask(self.config.UMASK)
        os.chdir(self.config.WORKING_DIR)

        current_user=pwd.getpwuid(os.getuid())
        current_group=grp.getgrgid(os.getgid())

        if current_user!=self.config.USER or current_group!=self.config.GROUP:
            try:
                os.initgroups(self.config.USER.pw_name, self.config.GROUP.gr_gid)
                os.setgid(self.config.GROUP.gr_gid)	
                os.setuid(self.config.USER.pw_uid)
            except PermissionError as e:
                print("Warning: You can't change owner: %s" % str(e))

        pid = os.fork()
        if pid > 0:
            os._exit(0)

        os.dup2(os.open(os.devnull, os.O_RDWR), sys.stdin.fileno())
        os.dup2(daemon_stdout.fileno(), sys.stdout.fileno())
        os.dup2(daemon_stderr.fileno(), sys.stderr.fileno())


        


