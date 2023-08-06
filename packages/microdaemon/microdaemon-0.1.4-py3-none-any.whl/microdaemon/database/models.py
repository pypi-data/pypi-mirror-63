class Database(object):
    def __init__(self,configuration_file):
        self._configuration_file=configuration_file
        self.onshow=[]

    def __str__(self): 
        return self._configuration_file
