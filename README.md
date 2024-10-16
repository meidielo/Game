# Math Quiz Game

This project is a Django-based math quiz game designed with three difficulty levels: easy, medium, and hard. The game dynamically generates arithmetic questions, provides real-time validation, and tracks user progress via a point system. This `README` will guide you through setting up and running the project in Visual Studio Code (VS Code).

## Prerequisites

Before running the game, ensure you have the following installed:

1. **Python 3.8 or above**: [Download Python](https://www.python.org/downloads/)
2. **Visual Studio Code (VS Code)**: [Download VS Code](https://code.visualstudio.com/)
3. **Django 3.x**: Install Django using `pip` (shown in setup steps below).

## Project Setup

### 1. Clone the Repository
First, clone the repository to your local machine:
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a Virtual Environment
To avoid dependency issues, create a virtual environment. Run the following commands in your terminal within the project folder:
```bash
# For Windows:
python -m venv venv

# For macOS/Linux:
python3 -m venv venv
```

Activate the virtual environment:
```bash
# For Windows:
venv\Scripts\activate

# For macOS/Linux:
source venv/bin/activate
```

### 3. Install Project Dependencies
Once your virtual environment is activated, install the necessary dependencies:
```bash
pip install -r requirements.txt
```

If `requirements.txt` is not provided, you can manually install Django:
```bash
pip install django
```

### 4. Set Up the Database
Migrate the database to create the necessary tables:
```bash
python manage.py migrate
```

### 5. Run the Development Server
You can now start the Django development server to run the game:
```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000` to play the game.

## Running the Project in VS Code

### 1. Open the Project in VS Code
- Launch Visual Studio Code.
- Open the project folder by navigating to **File > Open Folder**, then select your project directory.

### 2. Install the Python Extension
To improve your development experience, install the Python extension for VS Code:
- Go to the Extensions tab (or press `Ctrl+Shift+X`).
- Search for "Python" and install the official Python extension by Microsoft.

### 3. Select the Python Interpreter
VS Code needs to know which Python interpreter to use:
- Press `Ctrl+Shift+P` to open the command palette.
- Type `Python: Select Interpreter` and select the interpreter from the `venv` (virtual environment) you created.

### 4. Run the Django Server in VS Code
- Open the terminal in VS Code by going to **Terminal > New Terminal**.
- Ensure the virtual environment is activated:
  - For Windows: `venv\Scripts\activate`
  - For macOS/Linux: `source venv/bin/activate`
- Run the Django development server directly from the VS Code terminal:
  ```bash
  python manage.py runserver
  ```

### 5. Viewing the Game in the Browser
After starting the server, open your browser and go to `http://127.0.0.1:8000` to access the game.

## Project Structure

- **game/**: Contains the Django app code, including the game logic.
- **game/static/**: Stores the static assets (CSS, JavaScript).
- **game/templates/**: HTML templates for rendering the game's user interface.
- **db.sqlite3**: The SQLite database file.
- **manage.py**: Django’s management script to run the server, migrations, etc.

## Closing the Server
To stop the server, press `Ctrl+C` in the terminal where the server is running.

## Additional Notes

- **Running Migrations**: Whenever you make changes to models, remember to run:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

- **Creating a Superuser**: To access the Django admin interface, you can create a superuser account by running:
  ```bash
  python manage.py createsuperuser
  ```