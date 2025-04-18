"""
WSGI entry point for Consolidated Document Solutions website
Used for production deployment with Gunicorn or other WSGI servers
"""

from app import app

if __name__ == "__main__":
    app.run()
