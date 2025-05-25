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
    
    def __init__(self, taskPath, command='whoami'):
        super().__init__(taskPath)
        # Private Members
        self._command = command
        self._result = ""
        self._taskPath = '{}task'.format(taskPath)
        
        with open(self._taskPath, 'w') as f:
            f.write(f"{self.taskType}:{self._command}")

    # Public Methods
    def writeTask(self, command):
        self._command = command
        with open(self._taskPath, 'w') as f:
            f.write(f"{self.taskType}:{self._command}")

    def getResult(self):
        print(self._result)

        return self._result

    def receiveResult(self, result):
        self._result = result

    def clearTask(self):
        if os.path.exists(self._taskPath):
            os.remove(self._taskPath)
        else:
            print("[Task: clearTask] Error Path for task doesn't exist")           
    # def clearTask(self):
    #     try:
    #         with open(self.taskPath, 'w'):
    #             pass
    #     except: FileNotFoundError