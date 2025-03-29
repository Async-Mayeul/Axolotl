import os
from abc import ABC, abstractmethod

class Task(ABC):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def taskType(self):
        pass

    @abstractmethod
    def setTask(self):
        pass

    @abstractmethod
    def getTask(self):
        pass

    @abstractmethod
    def clearTask(self):
        pass

class TaskShell(Task):
    taskType = "shell"
    
    def __init__(self, command='whoami'):
        super().__init__()
        # Private Members
        self._command = command
        self._result = ""

    # Public Methods
    def setTask(self, command):
        self._command = command

    def getTask(self):
        return self._command

    def getResult(self):
        return self._result

    def receiveResult(self, result):
        self._result = result

    def clearTask(self):
        self._command = ""           
