# Consolidated Document Solutions Website

A modern, professional website redesign for Consolidated Document Solutions, a printing and document services company established in 1966.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for version control)

### Installation

1. Clone the repository (or download and extract the ZIP file)
   ```
   git clone https://github.com/your-username/cds-website.git
   cd cds-website
   ```

2. Create and activate a virtual environment (recommended)
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages
   ```
   pip install -r requirements.txt
   ```

4. Create necessary directories
   ```
   mkdir -p static/uploads
   ```

5. Run the development server
   ```
   python app.py
   ```

6. Open your browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Project Structure

```
cds-website/
│
├── app.py                     # Main Flask application file
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
│
├── static/                    # Static assets
│   ├── css/                   # Compiled CSS files
│   ├── src/                   # Source files for processing
│   │   ├── scss/              # SCSS source files
│   │   └── js/                # JavaScript source files
│   ├── js/                    # Compiled JavaScript files
│   ├── images/                # Image assets
│   └── uploads/               # User uploaded files
│
├── templates/                 # HTML templates
│   ├── base.html              # Base template with common elements
│   ├── index.html             # Homepage
│   └── ...                    # Other templates
│
└── utils/                     # Utility functions
```

## Development

### SCSS Compilation

This project uses SCSS for styling. To compile SCSS to CSS, you have two options:

1. Use Flask-Assets (setup in app.py)
   - The SCSS files will be automatically compiled when you run the Flask application

2. Manual compilation (if you prefer)
   ```
   # Install sass globally if you haven't already
   npm install -g sass

   # Compile
   sass static/src/scss/main.scss:static/css/main.css
   ```

### JavaScript

The JavaScript files in `static/src/js/` are concatenated and minified to `static/js/main.min.js` using Flask-Assets.

### Templates

The templates use Jinja2, Flask's templating engine. The base template (`base.html`) contains the common elements (header, footer, navigation) and other templates extend from it.

## Deployment

For production deployment, consider the following steps:

1. Set environment variables for production
   ```
   export FLASK_ENV=production
   export SECRET_KEY=your-secure-secret-key
   ```

2. Use a production WSGI server like Gunicorn
   ```
   gunicorn -w 4 wsgi:app
   ```

3. Set up a reverse proxy (like Nginx or Apache) to serve static files and forward requests to the WSGI server

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
