from collections import OrderedDict

class Menu():

    def __init__(self, name):
        self.name = name
        self.commands = OrderedDict()
        self.commands["help"] = ["Show help.", ""]
        self.commands["home"] = ["Return home.", ""]
        self.commands["exit"] = ["Exit Axolotl.", ""]

    def parseCmd(self):
        cmdPrompt = input(" ["+self.name+"]" + "> ")
        cmdInput = cmdPrompt.split()
        command = cmdInput[0]
        args = []

        for i in range(1, len(cmdInput)):
            args.append(cmdInput[i])

        return command, args

    def registerCmd(self, command, description,  args):
        self.commands[command] = [description, args]

    def showHelp(self):
        print("\tAvailable command : \n")
        for i in self.commands:
            print(f"\t{i} - {self.commands[i][0]} - {self.commands[i][1]}")
