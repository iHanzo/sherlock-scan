# Django Login Clustering Project

This Django project aims to implement login functionality and clustering analysis of login attempts using DBSCAN.

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

- Python 3.x
- Django
- scikit-learn

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/django-login-clustering.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Apply migrations to create the database schema:

    ```bash
    python manage.py migrate
    ```

### Usage

1. Start the Django development server:

    ```bash
    python manage.py runserver
    ```

2. Access the web application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to register, login, and view login attempts.

3. Run the clustering analysis script:

    ```bash
    python scan.py
    ```

## Contributors

- [Cyclingbanana](https://github.com/Cyclingbanana)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

