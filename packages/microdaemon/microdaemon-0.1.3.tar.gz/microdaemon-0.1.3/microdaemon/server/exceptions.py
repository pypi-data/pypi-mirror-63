class Http405MethodNotAllowed(Exception):
    """ Raised for request with invalid method. """

    def __init__(self,request):
        self.request=request

    def __str__(self):
        return "Method %s is not allowed for page %s" % (self.request.method,self.request.path)

class Http404NotFound(Exception):
    """ Raised for request for inexistent resource. """

    def __init__(self,request):
        self.request=request

    def __str__(self):
        return "Page %s was not found on this server" % self.request.path

class Http400BadRequest(Exception):
    """ Raised for bad request. """

    def __init__(self,request):
        self.request=request

    def __str__(self):
        return "Bad request on %s" % self.request.path

class Http401Unauthorized(Exception):
    """ Raised for unauthorized. """

    def __init__(self,request):
        self.request=request

    def __str__(self):
        return "Authentication required for access to %s" % self.request.path

class Http403Forbidden(Exception):
    """ Raised for forbidden. """

    def __init__(self,request):
        self.request=request

    def __str__(self):
        return "Resource %s is forbidden" % self.request.path
