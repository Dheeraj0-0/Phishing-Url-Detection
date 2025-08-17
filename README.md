# Phishing URL Detector 🛡️

A web-based application that uses a machine learning model to detect phishing websites. The application analyzes URLs based on 30 distinct features to determine their safety, providing users with a detailed breakdown of the analysis and a confidence score.

![Screenshot of the Phishing URL Detector application]

---

## ✨ Features

-   **Machine Learning Based Detection**: Utilizes a Gradient Boosting Classifier model to predict the likelihood of a URL being a phishing attempt.
-   **Detailed Feature Analysis**: Provides a comprehensive report on all 30 features used in the analysis, explaining why each contributes to the final score.
-   **Interactive UI**: A modern, responsive user interface built with Bootstrap, featuring a threat meter, scan history, and a dark mode toggle.
-   **Dockerized Deployment**: The entire application is containerized with Docker, ensuring a consistent and easy setup process.
-   **Session-Based History**: Keeps a temporary history of your last 20 scans for quick reference.

---

## 🛠️ Tech Stack

-   **Backend**: Python, Flask
-   **Machine Learning**: Scikit-learn, Pandas, NumPy
-   **Frontend**: HTML, CSS, JavaScript, Bootstrap
-   **Containerization**: Docker
-   **Deployment**: Gunicorn

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   [Docker](https://www.docker.com/get-started) must be installed on your machine.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Build the Docker image:**
    This command builds the image and runs the `retrain.py` script inside the container to create a compatible `model.pkl` file.
    ```bash
    docker build -t phishing-detector .
    ```

3.  **Run the Docker container:**
    This command starts the application and maps your local port 8000 to the container's port 5000.
    ```bash
    docker run -p 8000:5000 phishing-detector
    ```

4.  **Access the application:**
    Open your web browser and navigate to `http://localhost:8000`.

---

## 🚢 Deployment

This application is designed to be deployed as a container.

1.  **Push the Image to a Registry**:
    Push your built Docker image to a container registry like Docker Hub, GitHub Container Registry (GHCR), or Azure Container Registry.
    ```bash
    # Example for Docker Hub
    docker tag phishing-detector YOUR_DOCKERHUB_USERNAME/phishing-detector:latest
    docker push YOUR_DOCKERHUB_USERNAME/phishing-detector:latest
    ```

2.  **Deploy to a Host**:
    Deploy the container image to a cloud service like Azure Web Apps, Heroku, or AWS Elastic Beanstalk. Ensure you configure the following environment variable on the hosting service:
    -   `WEBSITES_PORT = 5000`

---


