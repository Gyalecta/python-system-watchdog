import psutil
import datetime

# 1. Otteniamo il Timestamp
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 2. Otteniamo la RAM
memory = psutil.virtual_memory()
ram_usage = memory.percent
ram_usage_gb = (((memory.total / 1024) / 1024) / 1024)

# 3. Otteniamo il Disco (della root /)
disk = psutil.disk_usage('/')
disk_usage = disk.percent

# 4. Otteniamo la CPU (Media)
cpu_usage = psutil.cpu_percent(interval=1)

# --- STAMPA DEL REPORT ---
print(f"--- Report: {now} ---")
print(f"💾 RAM Usata: {ram_usage}%")
print(f"💾 RAM Usata: {ram_usage_gb:.2f}GB")
print(f"💿 Disco Usato: {disk_usage}%")
print(f"🧠 CPU Usata: {cpu_usage}%")

# --- LOGICA DI ALLARME (Molto più facile che in Bash!) ---
if disk_usage > 80:
    print("⚠️  ALLARME: Disco quasi pieno!")
elif ram_usage > 90:
    print("⚠️  ALLARME: RAM satura!")
else:
    print("✅ Tutto nella norma.")
