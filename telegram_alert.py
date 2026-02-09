import psutil
import requests
import os
import sys
import time  # <--- NUOVO IMPORT

# --- CONFIGURAZIONE ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("❌ Errore: Mancano le variabili d'ambiente.")
    sys.exit(1)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"❌ Errore connessione: {e}")

print("🚀 Bot di Monitoraggio Avviato (Controllo ogni 60s)...")

# --- IL CICLO INFINITO ---
while True:
    try:
        # 1. Raccolta Dati
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(interval=1)
        
        # Log su terminale (per debug)
        print(f"Check: CPU {cpu}% | RAM {ram}% | DISK {disk_percent}%")

        # 2. Logica Allarme
        message = "⚠️ ALLARME SERVER AWS ⚠️\n\n"
        alarm = False

        if disk_percent > 85:
            message += f"💿 Disk: {disk_percent}%\n"
            alarm = True
        
        if ram > 90:
            message += f"💾 RAM: {ram}%\n"
            alarm = True
        
        # 3. Invio (Solo se serve)
        if alarm:
            send_telegram_message(message)
            print("✅ Allarme inviato.")

        # 4. Dormi per 60 secondi
        time.sleep(60)

    except KeyboardInterrupt:
        print("\n🛑 Bot arrestato manualmente.")
        break
    except Exception as e:
        print(f"Errore imprevisto: {e}")
        time.sleep(60) # Aspetta comunque prima di riprovare
