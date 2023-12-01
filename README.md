# b3rn_zero_copilot

## Anleitung zum Starten und Testen der FastAPI-Anwendung

Diese Anleitung hilft Ihnen dabei, die FastAPI-Anwendung in einem Docker-Container zu starten und zu testen.

### Voraussetzungen

- Docker und Docker Compose müssen auf Ihrem System installiert sein.
- Stellen Sie sicher, dass Sie die neueste Version des Projekts aus dem Repository geklont haben.

### Schritte zum Starten der Anwendung

1. **Starten Sie die Docker-Container:**
   - Öffnen Sie ein Terminal.
   - Navigieren Sie zum Hauptverzeichnis des Projekts, wo sich die `docker-compose.yml`-Datei befindet.
   - Führen Sie den folgenden Befehl aus, um die Docker-Container im Hintergrund zu starten:
     ```
     docker-compose up -d
     ```

2. **Überprüfen Sie, ob die Container laufen:**
   - Überprüfen Sie den Status der Container mit:
     ```
     docker ps
     ```
   - Stellen Sie sicher, dass die Container für die FastAPI- und Langchain-Dienste in der Liste der laufenden Container angezeigt werden.

### Testen der FastAPI-Anwendung

1. **Zugriff auf die Anwendung:**
   - Da der Port 80 des FastAPI-Containers auf den Port 8000 Ihres Host-Systems weitergeleitet wird, können Sie auf die Anwendung zugreifen, indem Sie den folgenden Befehl in Ihrem Terminal ausführen:
     ```
     curl http://localhost:8000
     ```
   - Sie sollten eine Antwort wie `{"message":"Hello World"}` erhalten, was bedeutet, dass Ihre Anwendung erfolgreich läuft und auf Anfragen reagiert.

### Problembehandlung

- Wenn die Container nicht starten, überprüfen Sie Ihre `docker-compose.yml` und andere Konfigurationsdateien auf Fehler.
- Wenn Sie keine Verbindung zur Anwendung herstellen können, stellen Sie sicher, dass keine Netzwerkeinstellungen oder Firewalls den Zugriff auf den Port 8000 blockieren.
- Überprüfen Sie die Container-Logs auf Fehlermeldungen mit `docker logs [container_name]`.
