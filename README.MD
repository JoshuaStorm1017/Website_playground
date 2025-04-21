# Consolidated Document Solutions Website

This is a Flask-based website for Consolidated Document Solutions, showcasing their services, testimonials, and industries served, with a form for quote requests.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv cw_env
    ```
3.  **Activate the virtual environment:**
    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Set environment variables:**
    *   You need to set a `SECRET_KEY` for Flask sessions and CSRF protection.
    *   Set `FLASK_APP=app.py`.
    *   Set `FLASK_ENV=development` for development mode (enables debug features).

    Example (Windows):
    ```bash
    set SECRET_KEY=your_secret_key_here
    set FLASK_APP=app.py
    set FLASK_ENV=development
    ```

    Example (macOS/Linux):
    ```bash
    export SECRET_KEY=your_secret_key_here
    export FLASK_APP=app.py
    export FLASK_ENV=development
    ```

## Running the Application

Make sure your virtual environment is activated and environment variables are set.

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000/`.

## Directory Structure

*   `app.py`: The main Flask application file, containing routes, data structures, and basic logic.
*   `forms.py`: Defines Flask-WTF forms used in the application.
*   `static/`: Contains static assets like CSS, JavaScript, and images.
    *   `static/css/`: Compiled CSS files.
    *   `static/js/`: Compiled JavaScript files.
    *   `static/images/`: Image assets.
    *   `static/src/`: Source files for static assets (e.g., SCSS, raw JS).
*   `templates/`: Contains Jinja2 HTML templates for rendering pages.
*   `tests/`: Contains test files for the application.
*   `requirements.txt`: Lists the project dependencies.
*   `README.md`: Project documentation.
*   `wsgi.py`: Entry point for WSGI servers (e.g., Gunicorn).

## Content Management

Content for products/services, testimonials, and industries is currently managed directly within the `app.py` file using Python data structures (lists of dictionaries).

*   **Products and Services:** Modify the `services` list in `app.py`. Each dictionary represents a service and should include keys like `slug`, `name`, `description`, etc. The `slug` is used in the URL.
*   **Testimonials:** Modify the `testimonials` list in `app.py`. Each dictionary represents a testimonial and should include keys like `quote`, `author`, etc.
*   **Industries:** Modify the `industries` list in `app.py`. Each dictionary represents an industry and should include keys like `slug`, `name`, `description`, etc. The `slug` is used in the URL.

To update content, you will need to edit `app.py` and restart the Flask development server.

## Running Tests

Make sure your virtual environment is activated and dependencies (including `pytest` and `pytest-cov`) are installed.

To run the test suite:

```bash
pytest
```

To run tests and generate a coverage report:

```bash
pytest --cov=.
```

This will run the tests and show a coverage summary in the terminal.

## Environment Requirements

The following environment variables are required to run the application:

*   `SECRET_KEY`: A strong, random string used for security purposes (sessions, CSRF protection).
*   `FLASK_APP`: Should be set to `app.py`.
*   `FLASK_ENV`: Set to `development` for development or `production` for production.
*   `LOG_LEVEL`: (Optional) Sets the logging level (e.g., INFO, DEBUG, WARNING, ERROR). Defaults to INFO.
