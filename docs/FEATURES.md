# Features

This document lists the key features of the Crop Stress Advisory application.

## Core Features

*   **Weather Monitoring:**
    *   Fetches and displays real-time weather data for the user's location, including temperature, humidity, rainfall, and wind speed.

*   **Crop Stress Prediction:**
    *   Utilizes a machine learning model to predict the level of stress a crop is experiencing based on weather data and crop-specific information (crop type and growth stage).
    *   Provides a stress level (Healthy, Mild Stress, Severe Stress) and a confidence score for the prediction.

*   **Reporting and Analysis:**
    *   Allows users to submit detailed crop stress reports, including crop type, growth stage, and observational notes.
    *   Integrates with a Large Language Model (LLM) to provide an AI-powered analysis of the user's observations.

*   **Interactive Map:**
    *   Displays all submitted reports on an interactive map, allowing users to see the geographic distribution of crop stress.
    *   Shows the user's current location on the map.

*   **Recommendations:**
    *   Provides actionable recommendations based on the predicted stress level and the user's observations.

*   **Data Visualization:**
    *   Uses charts and graphs to visualize data, making it easier to understand.

*   **Multi-language Support:**
    *   The user interface is available in multiple languages, including English and Tamil.

*   **Health Check Endpoint:**
    *   Provides a `/api/health` endpoint to monitor the status of the backend service.

*   **CI/CD Pipeline:**
    *   An automated CI/CD pipeline using GitHub Actions to build, test, and deploy the application.
