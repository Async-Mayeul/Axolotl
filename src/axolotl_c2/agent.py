class Agent:
    def __init__(self, name, remoteIp, hostname, encryptionKey, path):
        # Private Members
        self._remoteIp           = remoteIp
        self._hostname           = hostname
        self._encryptionKey      = encryptionKey
        self._sleepTimeSec       = 3
        self._task               = None
        self._name               = name
        self._path               = path

    # Public Methods
    def getPath(self):
        return self._path

    def getIp(self):
        return self._remoteIp

    def getHostname(self):
        return self._hostname

    def getKey(self):
        return self._encryptionKey

    def getTask(self):
        return self._task

    def setTask(self, task):
        self._task = task

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
