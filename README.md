cd ~/multi-tier-docker-app

# Multi-Tier Docker App

This project demonstrates a **multi-tier web application** using **Docker**. It includes:

- **Frontend:** Static HTML served by Nginx
- **Backend:** Python Flask API
- **Database:** PostgreSQL

All components run in **separate Docker containers** and are orchestrated with **Docker Compose**.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Setup & Run](#setup--run)
3. [Usage](#usage)
4. [How It Works](#how-it-works)
5. [Docker Concepts Demonstrated](#docker-concepts-demonstrated)
6. [Interview Prep](#interview-prep)

---

## Project Structure

```text
multi-tier-docker-app/
  ├── backend/
  │   ├── app.py           # Flask API code
  │   ├── requirements.txt # Python dependencies
  │   └── Dockerfile       # Dockerfile to build backend image
  ├── frontend/
  │   ├── index.html       # Static HTML frontend
  │   └── Dockerfile       # Dockerfile to build frontend image
  └── docker-compose.yml   # Compose file to orchestrate all services

---

## Setup & Run

1. **Build and start containers**

\`\`\`bash
docker-compose up --build
\`\`\`

2. **Open the app**

- **Frontend (HTML page):** http://localhost:9090  
- **Backend home:** http://localhost:5000  
- **Backend API:** http://localhost:5000/users  

> Note: Port 9090 is used to avoid conflicts in KodeKloud Playground.

3. **Stop containers**

\`\`\`bash
docker-compose down
\`\`\`

---

## Usage

- Frontend shows a welcome page linking to the backend users API.  
- Backend connects to PostgreSQL and returns a list of users in JSON.  
- Database data persists using Docker **volumes**.

---

## How It Works

1. **Dockerfiles**

- **Backend Dockerfile**
\`\`\`dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "run"]
\`\`\`

Explanation:

- `FROM python:3.11-slim` → lightweight Python image  
- `WORKDIR /app` → sets container working directory  
- `COPY requirements.txt` & `RUN pip install` → install dependencies  
- `COPY . .` → copy source code  
- `EXPOSE 5000` → container listens on port 5000  
- `ENV FLASK_APP` & `ENV FLASK_RUN_HOST` → Flask configuration  
- `CMD ["flask", "run"]` → start the server  

- **Frontend Dockerfile**
\`\`\`dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
\`\`\`

Explanation:

- Uses lightweight Nginx image  
- Copies static HTML to Nginx default folder  
- EXPOSE 80 allows container port mapping  

2. **Docker Compose**

\`\`\`yaml
version: "3.9"
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: testdb
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      POSTGRES_HOST: db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: testdb
    ports:
      - "5000:5000"
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "9090:80"
    depends_on:
      - backend

volumes:
  db_data: {}
\`\`\`

Explanation:

- **db** → PostgreSQL container  
- **backend** → Flask app connects to `db` by service name  
- **frontend** → Nginx serves HTML on port 9090  
- `depends_on` → ensures containers start in order  
- `volumes` → database persists even if container stops  

3. **Networking**

- Docker Compose creates a **private network**.  
- Backend can reach database using **host `db`**.  
- Frontend uses mapped host ports to reach backend.

---

## Docker Concepts Demonstrated

- Dockerfiles (build container images)  
- Multi-container orchestration with Docker Compose  
- Container networking (service name resolution)  
- Volumes for data persistence  
- Port mapping (container → host)  

---
