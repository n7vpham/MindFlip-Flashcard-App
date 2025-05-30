# MindFlip – Flashcard Web App

**MindFlip** is a full-stack flashcard web application designed to help students study. Users can sign up, create study sets, and interact with the material through dynamic flashcards. Built with Flask and MongoDB on the backend and styled with Bootstrap and JavaScript for a responsive, interactive frontend.

---

## ✨ Features

* 🛬 Landing page with call-to-action buttons (Login / Get Started)
* 🔐 User registration, login, and logout
* 🏠 Home page displaying all flashcard sets with direct "Study" access
* 📚 Study mode with card-flip animations
* 🧰 Manage Sets page with Edit/Delete options and basic filtering
* 📝 Manage Flashcards view with advanced filtering by front/back/both
* 👤 Profile page with editable user information (name, email, password)
* ✅ Input validation on both frontend and backend
* 🌌 Canvas-based particle background animation for enhanced UI

---

## 🛠 Tech Stack

| Layer    | Technologies                                                                              |
| -------- | ----------------------------------------------------------------------------------------- |
| Frontend | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Jinja, Canvas API, Google Fonts, Popper.js |
| Backend  | Python, Flask                                                                             |
| Database | MongoDB Atlas                                                                             |
| Tools    | Git, GitHub, Jira, virtualenv                                                             |

---

## 🎓 Project Context

This project was developed as part of **ITSC 4155 – Software Development Projects** at UNC Charlotte.
I, **Nam Pham**, handled the **entire frontend development**, including:

* Creating all HTML templates
* Implementing flashcard and canvas animations
* Adding frontend input validation

I also supported backend development by assisting with backend validation logic, integrating profile update functionality, and implementing the filtering systems for sets and flashcards.

---

## ⚙️ Getting Started

### MongoDB Atlas Setup

1. **Create a MongoDB Atlas Account**

* Go to [MongoDB Atlas](https://account.mongodb.com/account/register).
* Sign up using Google, GitHub, or manually with email and password.
  ![MongoDB Atlas Signup](images/1.png)

2. **Deploy a Cluster**

* After logging in, click "Create a Cluster".
* Choose the Free Tier.
* Select:

  * Provider: AWS (default)
  * Region: N. Virginia (us-east-1) (recommended)
  * Cluster name: leave as default (Cluster0)
* Click "Create Deployment".
  ![MongoDB Atlas Signup](images/3.png)

3. **Connect to Your Cluster**

* Click **Connect** next to your cluster.
* MongoDB will automatically detect your IP address.
* It will also **auto-generate a Database User** with random username and password.
* You can accept the auto-generated user, or create your own username and password manually.
* This database user is needed later for your application to connect.
  ![Create Database User](images/4.png)

4. **Choose a Connection Method**

* After creating your database user, MongoDB Atlas asks you to **choose a connection method**.
* Select **Drivers** (Node.js, Python, etc.).
  ![Choose Driver Option](images/5.png)

5. **Copy the Connection String**

* MongoDB will now display your **connection string**.
* This string is needed to connect from your application.
* Replace `<username>` and `<password>` in the connection string with your database credentials.
  ![Choose Driver Option](images/8.png)

### 🐍 Python Virtual Environment Setup

Before starting the app, you will need to configure your environment variables. Create a file named `.env` in the root directory and add the following lines:

```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.p59rbqf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
SECRET_KEY=<secret_key>
```

Then, in your terminal or bash shell, run the following commands:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
flask run
```

---

## 👥 Team Members

* Nam Pham (Frontend lead, backend support)
* Isaac Reed (Backend lead, unit tests, database integration)
* Ebert Amaya (Backend, deployment)
* Janie Ita (Pentesting & QA)
* Brody Banner (Project management, idea development)

---

## 🔗 Badges

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Framework-000000?logo=flask)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?logo=mongodb)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?logo=javascript)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5\&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3\&logoColor=white)
