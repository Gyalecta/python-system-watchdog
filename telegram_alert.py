import psutil
import requests
import os
import time
import redis  # ### NUOVO ###

# --- CONFIGURAZIONE ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# Redis Host: 'redis' è il nome del servizio che definiremo nel docker-compose
REDIS_HOST = os.getenv("REDIS_HOST", "redis") 

# Connessione al Database (Memoria)
try:
    cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    cache.ping() # Test connessione
    print("✅ Connesso a Redis!")
except Exception as e:
    print(f"⚠️ Warning: Redis non disponibile ({e}). Funzionerò senza memoria.")
    cache = None

def send_telegram_message(message):
    if not TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"❌ Errore connessione: {e}")

print("🚀 Bot Avviato con Memoria...")

while True:
    try:
        # 1. Check Risorse
        disk = psutil.disk_usage('/').percent
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(interval=1)
        
        print(f"Check: CPU {cpu}% | RAM {ram}% | DISK {disk}%")

        alerts = []
        
        # --- LOGICA INTELLIGENTE ---
        # Se c'è un problema, controlliamo se l'abbiamo già segnalato
        
        # SOGLIA DISCO (Metti 10 per testare, 80 in prod)
        if disk > 10: 
            # Chiediamo a Redis: esiste già la chiave 'alert_disk'?
            if cache and cache.get("alert_disk"):
                print("zzz... Allarme Disco già inviato recente. Dormo.")
            else:
                alerts.append(f"💿 Disk Critical: {disk}%")
                # Impostiamo la memoria: "Ricordatelo per 300 secondi (5 min)"
                if cache: cache.setex("alert_disk", 300, "sent")

        # SOGLIA RAM
        if ram > 90:
            if cache and cache.get("alert_ram"):
                print("zzz... Allarme RAM già inviato recente.")
            else:
                alerts.append(f"💾 RAM Critical: {ram}%")
                if cache: cache.setex("alert_ram", 300, "sent")

        # 2. Invio Cumulativo
        if alerts:
            msg = "⚠️ ALLARME SISTEMA ⚠️\n\n" + "\n".join(alerts)
            send_telegram_message(msg)
            print("✅ Messaggio inviato!")

        time.sleep(60)

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Errore: {e}")
        time.sleep(60)
