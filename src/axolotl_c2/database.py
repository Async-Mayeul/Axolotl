import os
import json
from agent import Agent

class Database():
    """
    Database type used to store information about agents.
    Now it's simply used a json file for each agent, with this format : 
    {
        "name": "example",
        "ip": "example",
        "hostname": "example",
        "key": "example"
    }
    """

    def __init__(self):
        self._agentsList = {}
        self._databasePath = 'data/database/'

        if not os.path.exists(self._databasePath):
            os.makedirs(self._databasePath)
            with open('data/database/agents.json', 'w+') as f:
               data = {'agents': []}
               json.dump(data,f,indent=4)

    def _save_agent(self, agent):
        """
        Private methods used to save an agent in json format.
        """
        agentJson = {
            'name': agent.getName(),
            'ip': agent.getIp(),
            'hostname': agent.getHostname(),
            'key': agent.getKey(),
            'path': agent.getPath(),
            'listener': agent.getListener()
        }

        with open('{}agents.json'.format(self._databasePath), 'r') as f:
            data = json.load(f)

        with open('{}agents.json'.format(self._databasePath), 'w') as f:
            data["agents"].append(agentJson)
            json.dump(data, f, indent=4)

    def _retrieve_agents(self):
        """
        Private methods used to retrieve an agent in json format.
        """
        with open('{}agents.json'.format(self._databasePath), 'r') as f:
                data = json.load(f)
                agentsList = data['agents']
                for agent in agentsList:
                    newAgent = Agent(
                        agent.get('name'),
                        agent.get('ip'),
                        agent.get('hostname'),
                        agent.get('key'),
                        agent.get('path'),
                        agent.get('listener')
                    )
                    self._agentsList[newAgent.getName()] = newAgent

    def getAgents(self):
        """
        Methods that use _retrieve_agents to retrieve the agent.
        """
        self._retrieve_agents()
        return self._agentsList

    def setAgent(self, agent):
        """
        Methods that use _save_agent to save an agent.

        Params:
            agent:Agent -> agent to save.
        """
        self._save_agent(agent)
