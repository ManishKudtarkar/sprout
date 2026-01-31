# Sprout AI: Intelligent Health Assistance System

Sprout AI is an intelligent health assistance system designed to analyze user-provided symptoms and provide safe, explainable, and early-stage health guidance using Artificial Intelligence. The system predicts possible health conditions, suggests natural remedies with scientific reasoning, and identifies emergency cases that require immediate medical attention.

## Core Objective
The core objective of Sprout AI is to support users in understanding their health issues at an early stage and encourage timely action, while avoiding unsafe or misleading medical advice. The system does not replace doctors; instead, it acts as a first-level health intelligence and awareness tool.

## Key Features
- **Hybrid AI Approach:** Combines rule-based diagnosis with dataset-driven logic.
- **Natural Remedies:** Recommends appropriate natural remedies with explanations.
- **Emergency Detection:** Scans for high-risk symptoms (e.g., chest pain, difficulty breathing) and advises immediate medical consultation.
- **Modular and Scalable:** Designed for future integration with machine learning and LLMs.

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
