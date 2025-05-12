# Archeo
Software per la gestione della documentazione dei siti archeologici

## Funzionalità principali

- Creazione e gestione di:
  - Anagrafiche (persone o soggetti coinvolti)
  - Località archeologiche
  - Enti (università, musei, ecc.)
  - Schede US (Unità Stratigrafiche)
- Visualizzazione delle entità salvate
- Definizione di:
  - Sequenze fisiche (relazioni stratigrafiche sopra/sotto)
  - Sequenze stratigrafiche (ordine cronologico)

 ## Requisiti

- Docker Compose

## Deployment con Docker

Creare i seguenti file in una directory:

**docker-compose.yml**:

```yaml
services:
  app:
    image: ghcr.io/e4ld3rs0n/archeo:latest
    container_name: archeo-app
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - /docker/archeo/uploads:/app/static/uploads
    depends_on:
      - db
    command: ["dockerize", "-wait", "tcp://db:5432", "-timeout", "30s", "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "120", "main:app"]

  db:
    image: postgres:16
    container_name: archeo-db
    environment:
      POSTGRES_DB: ${DB_NAME}             
      POSTGRES_USER: ${DB_USER}         
      POSTGRES_PASSWORD: ${DB_PASSWORD} 
    volumes:
      - /docker/archeo/dbdata:/var/lib/postgresql/data
```

**.env**:

```
DB_NAME=archeo
DB_USER=archeo
DB_PASSWORD=PLEASE_CHANGEME
SECRET_KEY=PLEASE_CHANGEME
```

Sostituire `PLEASE_CHANGEME` con delle stringhe lunghe generate casualmente. Avviare il progetto con:

```bash
docker compose up -d
```

## Stato del progetto

In sviluppo — molte sezioni sono ancora in fase di completamento.

## Licenza

Distribuito sotto licenza Apache 2.0.
