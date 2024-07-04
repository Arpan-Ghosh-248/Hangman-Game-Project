
This repository contains a Django Rest Framework based backend API and the frontend application for a Hangman game built using React.

## Prerequisites

- Python 3.x and Node.js installed on your system.
- pip package manager.
- npm (Node Package Manager).

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>

## Running the Project

2. Commands to run the backend
   ```bash
   cd hangman_proj
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver

4. Commands to run the frontend
   ```bash
   cd hangman_frontend
   npm install
   npm start
