import os
import requests

# Questi valori verranno passati in automatico da GitHub Actions
GITHUB_TOKEN = os.environ.get("GIST_TOKEN")
GIST_ID = os.environ.get("GIST_ID")

def get_new_spam_numbers():
    """
    Qui inseriamo la logica dello scraper.
    In futuro potremmo usare BeautifulSoup per leggere da siti pubblici,
    oppure collegarci a feed API open source di numeri spam.
    Per ora, simulo il recupero di un paio di numeri di test.
    """
    print("Cerco nuovi numeri spam sul web...")
    
    # Esempio: numeri appena segnalati
    return ["+390212345678", "+390698765432"]

def update_gist():
    if not GITHUB_TOKEN or not GIST_ID:
        print("Errore: GIST_TOKEN o GIST_ID mancanti (Verifica i Secrets su GitHub).")
        return

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_TOKEN}",
    }

    gist_url = f"https://api.github.com/gists/{GIST_ID}"
    
    # 1. Recupera il contenuto attuale del Gist
    print("Recupero la tua lista attuale dal Gist...")
    response = requests.get(gist_url, headers=headers)
    response.raise_for_status()
    gist_data = response.json()
    
    # Trova il nome del file nel Gist (es. 'blacklist.txt')
    filename = list(gist_data['files'].keys())[0]
    current_content = gist_data['files'][filename]['content']
    
    # 2. Ottieni i nuovi numeri trovati dallo scraper
    new_numbers = get_new_spam_numbers()
    
    # 3. Unisci le liste evitando i duplicati (così non appesantiamo l'app)
    existing_lines = [line.strip() for line in current_content.strip().split('\n') if line.strip()]
    updated = False
    
    for num in new_numbers:
        if num not in existing_lines:
            existing_lines.append(num)
            updated = True
            print(f"Trovato e aggiunto nuovo numero spam: {num}")
            
    if not updated:
        print("Nessun nuovo numero trovato. Il Gist è già aggiornato.")
        return
        
    # Ordina la lista in ordine alfabetico (opzionale, ma tiene il file pulito)
    existing_lines.sort()
    new_content = "\n".join(existing_lines)
    
    # 4. Invia l'aggiornamento a GitHub
    print("Invio l'aggiornamento a GitHub...")
    payload = {
        "files": {
            filename: {
                "content": new_content
            }
        }
    }
    
    patch_resp = requests.patch(gist_url, headers=headers, json=payload)
    patch_resp.raise_for_status()
    print("VITTORIA! Gist aggiornato con successo. La tua app Android scaricherà i nuovi dati al prossimo avvio.")

if __name__ == "__main__":
    update_gist()
