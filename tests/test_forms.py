import pytest
from app import app
from flask_wtf.csrf import generate_csrf

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True # Ensure CSRF is enabled for testing
    app.config['SECRET_KEY'] = 'testing_secret_key' # Set a secret key for CSRF
    with app.test_client() as client:
        with app.app_context(): # Push an application context
            yield client

def test_quote_request_valid_submission(client):
    # Assuming the form fields are 'name', 'email', 'service', 'message'
    # and that 'document-scanning' is a valid service value
    csrf_token = generate_csrf()
    response = client.post('/quote_request', data={
        'csrf_token': csrf_token,
        'name': 'Test User',
        'email': 'test@example.com',
        'service': 'document-scanning',
        'message': 'This is a test message.'
    }, follow_redirects=True) # Follow redirect after successful submission
    assert response.status_code == 200 # Assuming it redirects to a success page or the same page with a flash message
    # Further assertions could check for flash messages or content on the redirected page

def test_quote_request_invalid_submission(client):
    csrf_token = generate_csrf()
    response = client.post('/quote_request', data={
        'csrf_token': csrf_token,
        'name': '', # Invalid: Missing name
        'email': 'invalid-email', # Invalid: Invalid email format
        'service': '', # Invalid: Missing service
        'message': '' # Invalid: Missing message
    })
    assert response.status_code == 200 # Assuming it re-renders the form page
    # Further assertions could check for specific error messages on the page

def test_quote_request_csrf_protection(client):
    # Attempt submission without CSRF token
    response = client.post('/quote_request', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'service': 'document-scanning',
        'message': 'This is a test message.'
    })
    assert response.status_code == 400 # Expecting a CSRF error (Bad Request)