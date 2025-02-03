import os
from abc import ABC, abstractmethod

class Task(ABC):
    def __init__(self, taskPath):
        # Private members
        self._taskPath = taskPath
    
    @property
    def taskPath(self):
        return self._taskPath

    @taskPath.setter
    def taskPath(self, newPath):
        if not isinstance(newPath, str) or not newPath:
            raise ValueError("[Task: setter] : Path need to be not empty.")
        
        self._taskPath = newPath

    @property
    @abstractmethod
    def taskType(self):
        pass

    @abstractmethod
    def writeTask(self):
        pass

    @abstractmethod
    def clearTask(self):
        pass

class TaskShell(Task):
    taskType = "shell"

    def __init__(self, taskPath, command):
        # Private members
        super().__init__(taskPath)
        self._command = command

    def writeTask(self):
        with open(self.taskPath, "w") as f:
            f.write(f"{self.taskType}: {self._command}")

    def clearTask(self):
        if os.path.exists(self.taskPath):
            os.remove(self.taskPath)
        else:
            pass
