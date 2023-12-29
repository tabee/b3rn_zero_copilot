# b3rn_zero_copilot school

## Anleitung zum Starten und Testen der Anwendung

Diese Anleitung hilft Ihnen dabei, die FastAPI/gRPC-Anwendung in einem Docker-Container zu starten und zu testen.

### Elasticsearch
```bash
curl http://localhost:9200/_search?q=Altersrente
````

### Voraussetzungen

- Docker und Docker Compose müssen auf Ihrem System installiert sein.
- Stellen Sie sicher, dass Sie die neueste Version des Projekts aus dem Repository geklont haben.

### Schritte zum Starten der Anwendung

1. **Starten Sie die Docker-Container:**
   - Öffnen Sie ein Terminal.
   - Navigieren Sie zum Hauptverzeichnis des Projekts, wo sich die `docker-compose.yml`-Datei befindet.
   - Führen Sie den folgenden Befehl aus, um die Docker-Container im Hintergrund zu starten:
     ```
     docker-compose up --build
     ```

### Testen der FastAPI-Anwendung

1. **Zugriff auf die Anwendung:**
   - http://127.0.0.1/openapi.json
   - http://127.0.0.1/docs#
   - Da der Port 80 des FastAPI-Containers auf den Port 8000 Ihres Host-Systems weitergeleitet wird, können Sie auf die Anwendung zugreifen, indem Sie den folgenden Befehl in Ihrem Terminal ausführen:
     ```
     curl http://0.0.0.0:80
     curl http://0.0.0.0:80/agent/{topic}
     ```
   - Sie sollten eine Antwort wie `{"message":"Hello World"}` erhalten, was bedeutet, dass Ihre Anwendung erfolgreich läuft und auf Anfragen reagiert.

### Problembehandlung

- Überprüfen Sie die Container-Logs auf Fehlermeldungen mit `docker logs [container_name]`.
