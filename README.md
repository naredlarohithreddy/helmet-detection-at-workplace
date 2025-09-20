# PPE Detection MLOps System

A complete, end-to-end MLOps project demonstrating a full-stack system for real-time workplace safety monitoring. This application uses trained YOLOv8 and YOLOv12 models to detect PPE (Hard Hats), is served via a FastAPI backend and a React frontend, containerized with Docker, and features a fully automated CI/CD pipeline for deployment.

## Table of Contents
- [Problem Statement](#problem-statement)
- [ML Experimentation & Model Selection](#ml-experimentation--model-selection)
  - [Why YOLO?](#why-yolo)
  - [Model Comparison & Results](#model-comparison--results)
  - [Final Model Choice](#final-model-choice)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [CI/CD Pipeline](#cicd-pipeline)

---

## Problem Statement

In industrial environments such as construction sites, worker safety is paramount. A key piece of Personal Protective Equipment (PPE) is the hard hat. Manually monitoring a large worksite to ensure every individual is wearing a hard hat is inefficient, prone to human error, and not scalable.

This project aims to solve this problem by creating an automated system that can analyze images from a worksite and instantly identify individuals who are not in compliance with safety regulations, providing a foundation for real-time alerts and safety analytics.

---

## ML Experimentation & Model Selection

A core part of this project was to not just train a model, but to select the *right* model by balancing performance with operational requirements like inference speed.

### Why YOLO?

The YOLO (You Only Look Once) family of models was chosen for this task due to several key advantages:

- **Real-Time Performance:** YOLO delivers fast inference speeds, making it suitable for real-time video stream analysis
- **Strong Accuracy:** Modern YOLO variants provide excellent object detection performance with good precision and recall balance
- **Scalability:** Multiple model sizes (nano, small, medium) allow for trade-offs between speed and accuracy based on deployment hardware
- **Mature Ecosystem:** The ultralytics library provides a robust framework for training, validation, and deployment

### Model Comparison & Results

Several YOLO model variants were trained and evaluated to find the optimal architecture. All experiments were tracked using MLflow for reproducibility. The key performance metrics on the validation set are summarized below:

| Model | Precision | Recall | mAP@50 | mAP@50-95 |
| :--- | :--- | :--- | :--- | :--- |
| YOLOv8n (nano) | 0.946 | 0.575 | 0.624 | 0.407 |
| YOLOv8s (small) | 0.944 | 0.590 | 0.634 | 0.418 |
| YOLOv8m (medium) | 0.955 | 0.590 | 0.639 | 0.421 |
| YOLOv12s (small) | 0.920 | 0.874 | 0.934 | 0.612 |
| **YOLOv12s (small)** | **0.920** | **0.874** | **0.934** | **0.612** |

### Final Model Choice

The selection process was guided by the need for a model that could be deployed for real-time inference, where low latency is critical.

- **small vs. nano:** The YOLOv8s model provided noticeable accuracy improvements over YOLOv8n with only a minor increase in model size, making it a better baseline
- **small vs. medium:** While YOLOv8m showed slightly higher precision, the overall accuracy gains were marginal and did not justify the significant increase in model size and inference time
- **Final Model:** The YOLOv12s architecture was selected as the optimal choice. After optimization, it achieved significantly better recall and mAP scores, making it ideal for safety-critical applications where missing hard hats (false negatives) must be minimized

---

## Architecture & Tech Stack

This project uses a modern, containerized, and decoupled full-stack architecture.

- **Frontend:** A responsive React application built with Vite provides the user interface for image uploads and results visualization
- **Backend:** A high-performance API built with FastAPI serves the YOLOv12s model and includes custom OpenCV logic for rendering clear, non-overlapping annotations
- **MLOps:** The pipeline is fully reproducible using DVC for data/model versioning and MLflow for experiment tracking and model registry
- **DevOps:** The entire application is containerized with Docker and Docker Compose. A complete CI/CD pipeline using GitHub Actions automates building, testing, and pushing to GitHub Container Registry (GHCR)

---

## CI/CD Pipeline

This project is configured with a complete Continuous Integration and Continuous Deployment pipeline using GitHub Actions. On every push to the main branch, the following automated workflow is triggered:

1. **Build Stage:** Backend and frontend Docker images are built with proper caching for efficient builds
2. **Test Stage:** Automated tests are run to ensure code quality and functionality
3. **Push Stage:** Successfully built images are tagged and pushed to GitHub Container Registry
4. **Deploy Stage:** Updated containers can be automatically deployed to the target environment

The pipeline ensures that every code change goes through proper validation before being deployed, maintaining system reliability and enabling rapid iteration on the ML models and application features.
