# Expense Tracker

A simple expense tracking web app built with Django. Users can sign up, log in, and manage their own expenses.

## Features

- User registration and authentication
- Create, view, edit and delete expenses
- Each user can only see and manage their own expenses
- Expense fields: title, description, amount and category

## Tech Stack

- Python
- Django
- SQLite

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/applejuice8/expense-tracker.git
   cd expense-tracker
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations
   ```bash
   python manage.py migrate
   ```

4. Run the development server
   ```bash
   python manage.py runserver
   ```

5. Visit `http://127.0.0.1:8000` in your browser

## Usage

- Sign up for an account at `/accounts/signup/`
- Log in at `/accounts/login/`
- View your expenses at `/expenses/`
- Create a new expense at `/expenses/create/`

## Running Tests

```bash
python manage.py test
```

## Project Structure

```
expense-tracker/
├── expenses/       # Main expenses app
├── accounts/       # User registration
├── mysite/         # Project settings and URL config
└── templates/      # HTML templates
```