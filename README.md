A complete, end-to-end MLOps project demonstrating a full-stack system for real-time workplace safety monitoring. This application uses a fine-tuned YOLOv8 and YOLOv12 model to detect PPE (Hard Hats), is served via a FastAPI backend and a React frontend, containerized with Docker, and features a fully automated CI/CD pipeline for deployment.

## Table of Contents

- [Problem Statement](#-problem-statement)
- [ML Experimentation & Model Selection](#-ml-experimentation--model-selection)
  - [Why YOLO?](#why-yolo)
  - [Model Comparison & Results](#model-comparison--results)
  - [Final Model Choice](#final-model-choice)
- [Architecture & Tech Stack](#️-architecture--tech-stack)
- [CI/CD Pipeline](#-cicd-pipeline)


---

## Problem Statement

In industrial environments such as construction sites, worker safety is paramount. A key piece of Personal Protective Equipment (PPE) is the hard hat. Manually monitoring a large worksite to ensure every individual is wearing a hard hat is inefficient, prone to human error, and not scalable.

This project aims to solve this problem by creating an automated system that can analyze images from a worksite and instantly identify individuals who are not in compliance with safety regulations, providing a foundation for real-time alerts and safety analytics.

---

## ML Experimentation & Model Selection

A core part of this project was to not just train a model, but to select the *right* model by balancing performance with operational requirements like inference speed.

### Why YOLO?

The YOLO (You Only Look Once) family of models was chosen for this task due to several key advantages:
- **Real-Time Performance:** YOLO is renowned for its incredible speed, making it suitable for real-time video stream analysis.
- **High Accuracy:** It represents the state-of-the-art in object detection, providing a strong balance of precision and recall.
- **Scalability:** The availability of various model sizes (nano, small, medium, etc.) allows for easy trade-offs between speed and accuracy depending on the deployment hardware.
- **Excellent Ecosystem:** The `ultralytics` library provides a powerful framework for easy training, validation, and deployment.

### Model Comparison & Results

Several YOLOv8 model variants were trained and evaluated to find the optimal architecture. All experiments were tracked using **MLflow**. The key performance metrics on the validation set are summarized below:

| Model | Precision | Recall | mAP@50 | mAP@50-95 |
| :--- | :--- | :--- | :--- | :--- |
| `YOLOv8n` (nano) | 0.946 | 0.575 | 0.624 | 0.407 |
| `YOLOv8s` (small) | 0.944 | 0.590 | 0.634 | 0.418 |
| `YOLOv8m` (medium) | **0.955** | 0.590 | 0.639 | 0.421 |
| `YOLOv12s` (small) | 0.920 | 0.874 | 0.934 | 0.612 |
| **`YOLOv12s (Final)`** | **0.920** | **0.874** | **0.935** | **0.612** |

*Note: `YOLOv12s (Final)` represents the `yolov12s` model after further training and optimization, which became the champion model for this project.*

### Final Model Choice

The selection process was guided by the need for a model that could eventually be deployed for real-time inference, where **low latency is a critical feature.**

- **`small` vs. `nano`:** The `yolov8s` model provided a noticeable improvement in accuracy (mAP) over the `yolov8n` model with only a minor increase in size, making it a better baseline.
- **`small` vs. `medium`:** While the `yolov8m` model showed slightly higher precision, the overall accuracy gain was marginal and did not justify the significant increase in model size and inference time (latency).
- **Final Model:** The `yolov12s` architecture was selected as the best trade-off. After further training, it achieved a far superior Recall and mAP, making it the clear choice for the final application.

---

## Architecture & Tech Stack

This project uses a modern, containerized, and decoupled full-stack architecture.

- **Frontend:** A responsive **React** application built with Vite provides the user interface for image uploads.
- **Backend:** A high-performance API built with **FastAPI** serves the YOLOv12s model and includes custom **OpenCV** logic for rendering clear, non-overlapping annotations.
- **MLOps:** The pipeline is fully reproducible using **DVC** for data/model versioning and **MLflow** for experiment tracking.
- **DevOps:** The entire application is containerized with **Docker** and **Docker Compose**. A full CI/CD pipeline using **GitHub Actions** automates building, testing, pushing to **GitHub Container Registry (GHCR)**

---

CI/CD Pipeline
This project is configured with a complete Continuous Integration and Continuous Deployment pipeline using GitHub Actions. On every push to the main branch, the following automated workflow is triggered:

The backend and frontend Docker images are built.The new images are pushed to GitHub Container Registry.