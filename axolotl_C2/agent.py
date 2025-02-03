class Agent:
    def __init__(self, name, listener, remoteIp, hostname, encryptionKey):
        # Private Members
        self._listener           = listener
        self._remoteIp           = remoteIp
        self._hostname           = hostname
        self._encryptionKey      = encryptionKey
        self._sleepTimeSec       = 3
        
        # Public Members
        self.name                = name
        self.path                = "/data/listeners/{}/agents/{}".format(
                                        self._listener, 
                                        self.name)
        self.taskPath            = "{}tasks".format(self.path)

        _createPath()
    
    # Private Methods
    def _createPath(self):
        if not(os.path.exists(self._path)):
            os.mkdir(self._path)

    # Public Methods
    def getTask(self):
        pass
    def setTask(self, task):
        pass
    def setName(self, name):
        pass

