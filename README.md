# Sprout AI: Intelligent Health Assistance System

Sprout AI is an intelligent health assistance system designed to analyze user-provided symptoms and provide safe, explainable, and early-stage health guidance using Artificial Intelligence. The system predicts possible health conditions, suggests natural remedies with scientific reasoning, and identifies emergency cases that require immediate medical attention.

## Core Objective
The core objective of Sprout AI is to support users in understanding their health issues at an early stage and encourage timely action, while avoiding unsafe or misleading medical advice. The system does not replace doctors; instead, it acts as a first-level health intelligence and awareness tool.

## Key Features
- **Hybrid Diagnosis Pipeline:** Combines Vector Search (ChromaDB), Machine Learning (Scikit-Learn), and Rules for high-accuracy predictions.
- **Smart Personalization:** Adapts remedies based on User Profile (Age, Body Type - Vata/Pitta/Kapha).
- **Safety First:** Filters unsafe advice for Children (<12) and Seniors (>65).
- **Emergency Detection:** Scans for high-risk symptoms and triggers "Lockdown Mode" forcing medical consultation.
- **Natural Remedies:** Recommends safe, explainable home treatments.

## Advanced Tech Stack (FAANG Level)
- **Vector Database:** integrated ChromaDB for semantic search.
- **Web Interface:** Modern Flask + Tailwind-like UI.
- **Scalability:** Modular architecture ready for cloud deployment.

## Project Structure
- `src/`: Source code for the application.
  - `main.py`: Entry point for the CLI application.
  - `app.py`: Entry point for the Web application (Flask).
  - `templates/`: HTML templates for the web interface.
  - `static/`: CSS and JavaScript files.
  - `diagnosis.py`: Logic for symptom analysis and condition prediction.
  - `emergency.py`: Emergency detection module.
  - `remedies.py`: Module for suggesting natural remedies.
- `data/`: Data storage (knowledge base).
