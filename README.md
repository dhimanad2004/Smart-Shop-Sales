# Smart Shop Sales Prediction

A Django web application integrated with a Machine Learning pipeline to predict store sales. 

🔗 **[View Live Demo](https://smart-shop-sales.onrender.com/)**

## Features
* **Machine Learning Pipeline:** Uses a Random Forest Regressor to predict sales.
* **Prediction Form:** Interactive UI to input store parameters and get instant sales estimates.
* **Audit Trail:** Historical tracking logs to review past predictions.
* **Analytics Dashboard:** Executive analytics dashboard displaying sales insights.

## Tech Stack
* **Backend:** Django (Python)
* **Machine Learning:** Scikit-Learn, Pandas, NumPy
* **Database:** SQLite (Development) / PostgreSQL (Production via Neon)
* **Hosting:** Render

---

## Installation & Local Setup Guidelines

Follow these instructions to get a copy of the project up and running on your local machine for development and testing.

### Prerequisites
Make sure you have **Python 3.x** and **Git** installed on your system.

### 1. Clone the Repository
Clone this repository to your local machine using git:
```bash
git clone https://github.com
cd YOUR-REPO-NAME
```

### 2. Create and Activate a Virtual Environment
It is highly recommended to isolate your project dependencies using a virtual environment:
* **Windows (PowerShell):**
  ```powershell
  python -m venv env
  .\env\Scripts\Activate.ps1
  ```
* **Mac / Linux:**
  ```bash
  python3 -m venv env
  source env/bin/activate
  ```

### 3. Install Dependencies
Install all the required Python packages and libraries listed in the requirements file:
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
Set up your local SQLite database schemas:
```bash
python manage.py migrate
```

### 5. Start the Development Server
Launch the built-in Django development server:
```bash
python manage.py runserver
```
Open your browser and navigate to `http://127.0.0` to view the application.
****
