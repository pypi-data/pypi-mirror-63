import urllib.parse
import collections

from microdaemon import common

class Request(object):
    """ Request from user. 

    *server* (IsambardServer)
        The server serving the request.
    *environ* (dict)
        The wsgi environ object.

    Attributes:
        *method* (str)
            Request methods in uppercase (GET, POST, etc.).
        *path* (str)
            Request path.
        *path_split* (list)
            List of path elements.
        *script* (str)
            Script name.
        *accept* (str)
            Response mimetype requested by client or text/html if client doesn't supply it.
        *body* (str)
            Request body.
        *querystring* (dict)
            Querystring parameters.
        *cookies* (dict)
            Cookies from client.

    """

    def __init__(self,server,environ):
        self._environ=environ
        self._server=server
        self.method=environ["REQUEST_METHOD"].upper()
        self.path=environ["PATH_INFO"]
        self.script=environ["SCRIPT_NAME"]
        if "HTTP_ACCEPT" in environ:
            self.accept=environ["HTTP_ACCEPT"]
        else:
            self.accept="text/html"
        self.path_split=self._path_split()
        self.body=self._body()
        self.querystring=self._querystring()
        self.cookies=self._cookies(environ)

    def _cookies(self,environ):
        if "HTTP_COOKIE" not in environ: return {}
        t=[ x.strip().split("=") for x in environ["HTTP_COOKIE"].split(";") ]
        t=[ (x[0],"=".join(x[1:])) for x in t ]
        return dict(t)

    def _path_split(self):
        t=self.path.split("/")
        if len(t)==0: return []
        if t[0]=="": t=t[1:]
        if len(t)==0: return []
        if t[-1]=="": t=t[:-1]
        return t

    def _body(self):
        try:
            request_body_size = int(self._environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        # When the method is POST the variable will be sent
        # in the HTTP request body which is passed by the WSGI server
        # in the file like wsgi.input environment variable.
        request_body = self._environ['wsgi.input'].read(request_body_size)
        return request_body

    def _querystring(self):
        raw_qs=urllib.parse.parse_qsl(self.body)
        qs=collections.OrderedDict()
        for raw_k,raw_val in raw_qs:
            k=raw_k.decode()
            val=common.try_cast(raw_val)
            if '[' not in k:
                key=k
                ind=None
            elif not k.endswith(']'):
                key=k
                ind=None
            else:
                t=k.split('[')
                key=t[0]
                ind=t[1][:-1]
                if ind=="": 
                    ind=-1
                else:
                    try:
                        ind=int(ind)
                    except ValueError as e:
                        print(ind)
                        key=k
                        ind=None
            if key not in qs:
                if ind is None:
                    qs[key]=val
                    continue
                qs[key]=[]
            elif type(qs[key]) is not list:
                qs[key]=[qs[key]]
            if ind==-1 or ind is None:
                qs[key].append(val)
                continue
            qs[key].insert(ind,val)

        return qs

    def _querystring_old(self):
        raw_qs=urllib.parse.parse_qs(self.body)
        print()
        qs=collections.OrderedDict()
        for raw_k in raw_qs:
            raw_val=raw_qs[raw_k]
            print("RAW",raw_k,raw_val)
            k=raw_k.decode()
            if len(raw_val)==1:
                qs[k]=common.try_cast(raw_val[0])
                continue
            qs[k]=[ common.try_cast(x) for x in raw_val ]

        print(qs)
        n_qs={}
        for k in qs:
            val=qs[k]
            if '[' not in k:
                key=k
                ind=None
            elif not k.endswith(']'):
                key=k
                ind=None
            else:
                t=k.split('[')
                key=t[0]
                ind=t[1][:-1]
                if ind=="": 
                    ind=-1
                else:
                    try:
                        ind=int(ind)
                    except ValueError as e:
                        print(ind)
                        key=k
                        ind=None
            if key not in n_qs:
                if ind is None:
                    n_qs[key]=val
                    print(key,n_qs[key])
                    continue
                n_qs[key]=[]
            elif type(n_qs[key]) is not list:
                n_qs[key]=[n_qs[key]]
            if ind==-1 or ind is None:
                n_qs[key].append(val)
                print(key,n_qs[key])
                continue
            n_qs[key].insert(ind,val)
            print(key,n_qs[key])
            continue
            

        return n_qs
