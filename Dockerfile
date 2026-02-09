# 1. Usiamo un'immagine base di Python (leggera)
FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1

# 2. Impostiamo la cartella di lavoro dentro il container
WORKDIR /app

# 3. Copiamo la lista delle librerie
COPY requirements.txt .

# 4. Installiamo le librerie
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamo il resto del codice (il tuo script)
COPY telegram_alert.py .

# 6. Il comando che parte all'avvio
CMD ["python", "telegram_alert.py"]
