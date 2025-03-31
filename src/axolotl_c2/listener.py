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
        self.agentsList = agentsList

    def getAgentsList(self):
        return self.agentsList

    def getName(self):
        return self.name
    
    def getIp(self):
        return self.ipaddress

    def getPort(self):
        return self.port

    def run(self):
        @self.app.route('/register', methods=['POST'])
        def register_agent():
            res = request.json
            agent = Agent(res.get('name'), res.get('ip'), res.get('hostname'), res.get('key'), '{}{}/'.format(self.agentsPath, res.get('name')), self.name)
            self.database.setAgent(agent)
            
            return(res.get('name'),200)

        @self.app.route('/getTask', methods=['GET'])
        def get_task():
            agentName = request.args.get('agent')
            
            try:
                with open('{}{}/task'.format(self.agentsPath, agentName), 'r') as f:
                    task = f.read()
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
        self.daemon = threading.Thread(name=self.name, target=self.run, daemon=True)
        self.daemon.daemon = True
        self.daemon.start()
        self.isRunning = True

    def stop(self):
        self.process.terminate()
        self.isRunning = False
