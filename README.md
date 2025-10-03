Structura de la api:

smartcity-mqtt-sim/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ mqtt_client.py
│  │  ├─ db.py
│  │  └─ auth.py
│  ├─ requirements.txt
│  └─ Dockerfile
├─ simulator/
│  ├─ sim_publisher.py
│  └─ requirements.txt
│  └─ Dockerfile
├─ frontend/   (opcional)
│  └─ (skeleton Vite React)
├─ mosquitto/
│  └─ mosquitto.conf
└─ docker-compose.yml

# Simulator Notes
Si ejecutas el simulador en Docker (ver docker-compose), asegúrate de poner BROKER_HOST=mosquitto

# Para ejecutar, desde raiz correr:
docker-compose up --build

# Para ver backend:
Swagger: http://localhost:8000/docs
WebSocket: ws://localhost:8000/ws/telemetry (útil con wscat o en frontend)


.github\workflow
Bandit: escanea tu código Python (backend/app). La fase Fail on Bandit... carga el JSON y falla si se detecta alguna issue con severidad >= BANDIT_FAIL_ON. Actualmente BANDIT_FAIL_ON=HIGH. Cambia a MEDIUM/LOW si quieres ser más estricto.
Trivy: escanea las imágenes Docker que construimos (nombres: smartcity-backend:latest y smartcity-frontend:latest). Está configurado para fallar si encuentra vulnerabilidades CRITICAL o HIGH. Cambia TRIVY_SEVERITY en el env si quieres otro umbral.
CodeQL: añade análisis estático avanzado. No falla el pipeline por sí solo a menos que detectes alertas y configures políticas posteriores.
pip-audit: escanea dependencias Python (opcional). No está configurado para forzar fallo, solo reporta.