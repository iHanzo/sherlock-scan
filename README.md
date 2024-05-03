# Django Login Clustering Project

This Django project aims to implement login functionality and clustering analysis of login attempts using DBSCAN in Linux OS.

## Project Structure

- **`myapp`**: Django app containing the main functionality for user authentication and request logging.
  - **`models.py`**: Defines the database models for storing login attempts.
  - **`views.py`**: Contains the views for handling user authentication and request logging.
  - **`forms.py`**: Defines forms for user registration and login.
  - **`urls.py`**: URL routing configuration for the app.
  - **`templates`**: Directory containing HTML templates for rendering login, registration, and home pages.
  - **`migrations`**: Directory containing database migration files.

- **`db.sqlite3`**: SQLite database file storing login attempt data.

- **`scan.py`**: Python script for clustering analysis of login attempts using DBSCAN.

## Getting Started

### Prerequisites

- Python 3.6+
- Django 3.1+
- scikit-learn for clustering analysis
- Beautiful Soup for HTML parsing in auxiliary scripts
- Tkinter for building a GUI in associated utilities

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/iHanzo/sherlock-scan
    ```

2. Install dependencies:

    ```bash
    sudo apt update
    sudo apt install python3
    pip install django
    pip install scikit-learn
    pip install beautifulsoup4
    sudo apt install python3-tk
    ```

3. Apply migrations to create the database schema:

    ```bash
    python manage.py migrate
    ```

### Usage

1. Start the Django development server:

    ```bash
    python manage.py runserver 127.0.0.1:8000
    ```

2. Access the web application at [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/) to register, [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/) to login, and access myapp_requestlog table in db.sqlite3 to view login attempts.

3. Run SAP to imitate password attacks:

    ``bash
    python sap.py
    ```

4. Run the clustering analysis script:

    ```bash
    python scan.py
    ```

## Contributors

- [iHanzo](https://github.com/iHanzo)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

