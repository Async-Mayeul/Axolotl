import os
import json
import threading
from agent import Agent

class Database():
    """Database class
    Now, it's a simple class to save agents in json format.
    This class use Singleton design pattern.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False

        return cls._instance

    def __init__(self, agentsLocation=None):
        if not self._initialized:
            self._agentsList = {}
            self._agentsLocation = agentsLocation

    def _save_agent(self, agent):
        agentJson = {
            'name': agent.getName(),
            'ip': agent.getIp(),
            'hostname': agent.getHostname(),
            'key': agent.getKey(),
            'path': agent.getPath()
        }
        agentFileLocation = agent.getPath() + agent.getName()

        with open(agentFileLocation, 'w') as f:
            json.dump(agentJson, f)

    def _retrieve_agents(self):
        for agent in os.listdir(self._agentsLocation):
            with open(os.path.join(self._agentsLocation, agent), 'r') as f:
                agentJson = json.load(f)
                agent = Agent(
                    agentJson.get('name'),
                    agentJson.get('ip'),
                    agentJson.get('hostname'),
                    agentJson.get('key'),
                    agentJson.get('path')
                )
            self._agentsList[agent.getName()] = agent

    def getAgents(self):
        self._retrieve_agents()
        return self._agentsList

    def setAgent(self, agent):
        self._save_agent(agent)
