# Object Detection Microservice

This repository contains a containerized microservice for object detection using YOLOv8. The project leverages Docker, FastAPI, and YOLOv8 to provide an efficient and user-friendly solution for object detection.

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Docker**: For containerization of services.
- **Docker Compose**: To manage multi-container applications.
- **Ubuntu**: This guide assumes an Ubuntu-based system.

---

## Installation

Follow these steps to set up Docker and Docker Compose on your system.

### Step 1: Update System Packages
```bash
sudo apt update && sudo apt upgrade -y
```
### Step 2: Remove Older Docker Versions
```bash
sudo apt remove docker docker-engine docker.io containerd runc
```
### Step 3: Install Dependencies
```bash
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
```
### Step 4: Add Docker’s GPG Key
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```
### Step 5: Add Docker Repository
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Step 6: Install Docker
```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
docker --version
```
### Step 7: Install Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```
### Step 8: Add User to Docker Group
```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Project Setup
### Step 1: Clone the Repository
```bash
sudo usermod -aG docker $USER
newgrp docker
```
```plaintext
object_detection_microservice/
├── ai_backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── models/
│   │   └── yolov8s.pt
│   ├── output/
│   └── requirements.txt
├── ui_backend/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── docker-compose.yml
└── images/
    └── img1.jpg
```
### Step 2: Pre-download YOLOv8s Weights
```bash
mkdir -p ai_backend/models
wget https://github.com/ultralytics/yolov3/releases/download/v9.6.0/yolov8s.pt -O ai_backend/models/yolov8s.pt
```

## Running the Microservice
### Step 1: Start the Services
```bash
docker-compose up --build
```
### Step 2: Test the Microservice
```bash
curl -X POST "http://localhost:8000/detect/" -F "file=@images/img1.jpg"
```
## Ouput
### JSON File: Contains detection details
JSON: ai_backend/output/<image_name>_detections.json
### Processed Image: The image with bounding boxes drawn
Image: ai_backend/output/predict_<image_name>.jpg 

## Restarting the Services
```bash
docker-compose down
docker-compose up
```


