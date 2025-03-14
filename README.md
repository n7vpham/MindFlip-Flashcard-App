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
To start the backend development server, first navigate to /4155-study-project/backend.
Configure your connection to the database by creating a .env file and adding this line:
```bash
URI=mongodb+srv://<username>:<password>@fsb-cluster.7u2uh.mongodb.net/?retryWrites=true&w=majority&appName=fsb-cluster
```
Make sure to replace <username> and <password> with your credentials found on Mongo.

Run the server by entering this in the command line:
```bash
python run.py
```
