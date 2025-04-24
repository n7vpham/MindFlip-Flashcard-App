# 4155-study-project

## Project Introduction
Hello! This is our project for ITSC-4155. The aim of our project is to create a study helper for each user! We will accomplish this through this initial functionality:
 1. Letting users sign up
 2. Once a user is signed in, prompt the user to create their studyset
 3. Once a studyset is created, the user will be given a list of options (flashcards, tests) to study in their favorite medium. 
 
## Team Members
 - Ebert Amaya
 - Janie Ita
 - Brody Banner
 - Isaac Reed
 - Nam Pham

## Backend Development
To start the backend development server, first navigate to /4155-study-project (root folder).
Configure your connection to the database by creating a .env file and adding these lines:
```bash
URI=mongodb+srv://<username>:<password>@fsb-cluster.7u2uh.mongodb.net/?retryWrites=true&w=majority&appName=fsb-cluster
SECRET_KEY=<secret_key>
```
Make sure to replace &lt;username&gt; and &lt;password&gt; with your credentials found on Mongo, then replace &lt;secret_key&gt; with the secret key provided by the development team.

### Python Virtual Environment Setup (recommended)
**1. Create a virtual environment in the root directory**
```bash
python -m venv venv
```
**2. Activate the virtual environment:**
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

## Start the Server
In the root directory, run:
```bash
python run.py
```
