use std::collections::HashMap;
use hostname;
use reqwest::blocking::Client;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let ip = "10.0.2.15".to_string();
    let port = "4444".to_string();
    let key = "REPLACE_KEY".to_string();
    let n: u32 = 3;

    let hname_os = hostname::get()?;

    let hname = hname_os.into_string().unwrap_or_else(|_| "unknown".to_string());

    let type_field = "p";

    let regl = format!("http://{}:{}/reg", ip, port);

    let mut data = HashMap::new();
    data.insert("name", hname);
    data.insert("type", type_field.to_string());

    let client = Client::new();

    let response = client.post(&regl)
        .form(&data)
        .send()?;

    let name = response.text()?;
    println!("contenu de la réponse :{}", name);

    Ok(())
}
