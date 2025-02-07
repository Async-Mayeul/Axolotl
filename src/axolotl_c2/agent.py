class Agent:
    def __init__(self, name, remoteIp, hostname, encryptionKey):
        # Private Members
        self._remoteIp           = remoteIp
        self._hostname           = hostname
        self._encryptionKey      = encryptionKey
        self._sleepTimeSec       = 3
        self._task               = None
        self._name               = name

    # Public Methods
    def getTask(self):
        return self._task

    def setTask(self, task):
        self._task = task

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
