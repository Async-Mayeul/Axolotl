import os
import PyInstaller.__main__

class Agent:
    """
    An agent is a program on infected device that communicate with the C2.

    Params:
        name:String -> Name of the agent.
        remoteIp:String -> IP address of the victim device.
        hostname:String -> Hostname of the victim device, to distinguish each agents.
        encryptionKey:String -> Key generate by the agent to encrypt the traffic.
        path:String -> Path where the agent is registered on the C2.
        listener:String -> C2 listener that manager the agent.
    """
    def __init__(self, name, remoteIp, hostname, encryptionKey, path, listener):
        # Private Members
        self._remoteIp           = remoteIp
        self._hostname           = hostname
        self._encryptionKey      = encryptionKey
        self._sleepTimeSec       = 3
        self._task               = None
        self._name               = name
        self._path               = path
        self._listener           = listener

        if not os.path.exists(self._path):
            os.makedirs(self._path)

    # Public Methods
    def getListener(self):
        """
        Methods that return the name of agent's listener.
        """
        return self._listener

    def getPath(self):
        """
        Methods that return the agent's path.
        """
        return self._path

    def getIp(self):
        """
        Methods that return ip of the victim device.
        """
        return self._remoteIp

    def getHostname(self):
        """
        Methods that return hostname of the victim device.
        """
        return self._hostname

    def getKey(self):
        """
        Methods that return the symmetric key of the agent.
        """
        return self._encryptionKey

    def getTask(self):
        """
        Methods that return current task of the agent.

        Returns:
            Task object.
        """
        return self._task

    def setTask(self, task):
        """
        Methods to set the task of the agent.

        Params:
            task:Task -> task to be assigned.
        """
        self._task = task

    def getName(self):
        """
        Methods that return the agent's name.
        """
        return self._name

    def setName(self, name):
        """
        Methods that set the agent's name.

        Params:
            name:String -> new agent's name.
        """
        self._name = name
