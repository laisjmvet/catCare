# Cat Care Diagnoser

Welcome to the Cat Care Diagnoser! This application is an app designed to assist cat owners in identifying potential health issues in their feline companions. Please read this README for essential information on how to set up and use the app.
**Note:** This application is currently under development, and some features may not be fully functional. We appreciate your patience as I am working on improving the app.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Running the App](#running-the-app)
5. [Database Setup](#database-setup)
6. [Usage](#usage)
7. [Disclaimer](#disclaimer)
8. [Support](#support)


## Introduction

The Cat Health Diagnostic App is a web-based platform that enables users to answer a series of questions about their cat's health. Based on the user's responses, the app calculates the three most probable diseases that their cat may be experiencing. It's important to note that while the app can provide valuable insights, it should not replace a professional veterinarian's examination. Always seek proper veterinary care for your cat's health needs.

## Features

- **Health Diagnosis**: Users can answer a set of questions related to their cat's symptoms and behaviors.

- **Probable Diseases**: The app calculates and displays the three most probable diseases based on the user's input.

- **Veterinary Consultation**: Users can book a video chat consultation with a veterinarian for more personalized guidance.

- **Local Veterinarians**: The app provides information about local veterinarians in the user's area for easy access to professional care.

## Installation

### Backend (Python-Flask)

1. Clone this repository to your local machine.

2. Navigate to the project directory in your terminal.

3. Create a virtual environment (recommended) and activate it:

4. Install the Python dependencies from `requirements.txt`:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   pip install -r requirements.txt

## Frontend (React)

1. Navigate to the `frontend` directory:

    ```bash
    cd frontend
    ```

2. Install the Node.js dependencies:

    ```bash
    npm install
    ```

## Running the App

### Server (Python-Flask)

1. Make sure you are in the project's root directory.

2. Run the Flask development server:

    ```bash
    pipenv run dev
    ```

### Client (React)

1. Make sure you are in the `client` directory.

2. Start the development server:

    ```bash
    npm run dev
    ```

3. Open your web browser and navigate to [http://localhost:5173](http://localhost:5173) to access the app.

## Database Setup

To store user data and facilitate local veterinarian information, the app requires a database setup. Follow these steps to configure the database:

1. Create a `.env` file in the project's root directory.

2. In the `.env` file, specify your database URL using the following format:

    ```makefile
    DATABASE_URL=your_database_url_here
    ```

3. Run the database population script to set up the necessary database tables and seed data:

    ```bash
    python populatedb.py
    ```

## Usage

1. Access the app via your web browser at [http://localhost:5173](http://localhost:5173).

2. Follow the on-screen instructions to answer the questions related to your cat's health.

3. After completing the questions, the app will display the three most probable diseases. Remember that this is for informational purposes and not a substitute for professional veterinary care.

4. If needed, you can book a video chat consultation with a veterinarian or find local veterinarians in your area.

## Disclaimer

This app provides potential disease suggestions based on user responses but is not a replacement for professional veterinary care. Always consult with a licensed veterinarian for accurate diagnosis and treatment of your cat's health issues.

## Support

If you encounter any issues or have questions about the app, please reach out at [laisjmvet@gmail.com](mailto:laisjmvet@gmail.com).
