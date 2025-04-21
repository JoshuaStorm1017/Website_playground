import pytest
# Import app and helper functions directly for testing helpers
from app import app, get_all_categories, get_services_by_category, get_service_by_slug, service_categories

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing forms if needed later
    with app.test_client() as client:
        yield client

# --- Route Tests ---

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Consolidated Document Solutions" in response.data # Basic check

def test_about_route(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b"About Us" in response.data

def test_contact_route(client):
    response = client.get('/contact')
    assert response.status_code == 200
    assert b"Contact Us" in response.data

def test_services_index_route(client):
    response = client.get('/services')
    assert response.status_code == 200
    assert b"Our Products & Services" in response.data
    # Check if a known category name is present
    assert b"Membership Cards" in response.data

def test_testimonials_route(client):
    response = client.get('/testimonials')
    assert response.status_code == 200
    assert b"Testimonials" in response.data

def test_industries_route(client):
    response = client.get('/industries')
    assert response.status_code == 200
    assert b"Industries We Serve" in response.data

def test_quote_request_route_get(client):
    response = client.get('/quote_request')
    assert response.status_code == 200
    assert b"Request a Quote" in response.data

def test_file_upload_route_get(client):
    response = client.get('/upload')
    assert response.status_code == 200
    assert b"Upload Files" in response.data

def test_service_detail_valid_slug(client):
    # Use a valid category and service slug from the new structure
    response = client.get('/services/membership-cards/realcard')
    assert response.status_code == 200
    assert b"RealCard" in response.data # Check for service name
    assert b"Placeholder details for RealCard" in response.data # Check for placeholder detail

def test_service_detail_graphic_design_links(client):
    # Test the special case for graphic design links
    response = client.get('/services/graphic-design/main')
    assert response.status_code == 200
    assert b"Graphic Design" in response.data
    # Check if the placeholder URLs were correctly inserted
    assert b'href="/upload"' in response.data # Check for file upload link
    assert b'href="#"' in response.data # Check for artwork specs placeholder link

def test_service_detail_invalid_category_slug(client):
    response = client.get('/services/invalid-category/some-service')
    assert response.status_code == 404

def test_service_detail_invalid_service_slug(client):
    response = client.get('/services/membership-cards/invalid-service')
    assert response.status_code == 404

def test_404_error_handler(client):
    response = client.get('/non-existent-page')
    assert response.status_code == 404
    assert b"Page Not Found" in response.data

# --- Helper Function Tests ---

def test_get_all_categories():
    categories = get_all_categories()
    assert isinstance(categories, list)
    assert len(categories) == len(service_categories)
    # Check if it returns dictionaries with expected keys
    if categories:
        assert 'slug' in categories[0]
        assert 'name' in categories[0]
        assert 'services' in categories[0]
    # Check sorting (example: Embroidery should come before Graphic Design)
    names = [cat['name'] for cat in categories]
    assert names.index("Embroidery & Screen printing") < names.index("Graphic Design")

def test_get_services_by_category_valid():
    category_slug = "printing"
    services = get_services_by_category(category_slug)
    assert isinstance(services, list)
    assert len(services) == len(service_categories[category_slug]['services'])
    if services:
        assert services[0]['slug'].startswith(category_slug + '/')
        assert 'name' in services[0]

def test_get_services_by_category_invalid():
    services = get_services_by_category("invalid-category")
    assert isinstance(services, list)
    assert len(services) == 0

def test_get_service_by_slug_valid():
    category_slug = "membership-cards"
    service_slug_part = "realcard"
    service = get_service_by_slug(category_slug, service_slug_part)
    assert service is not None
    assert isinstance(service, dict)
    assert service['slug'] == f"{category_slug}/{service_slug_part}"
    assert service['name'] == "RealCard®"

def test_get_service_by_slug_valid_single_service_category():
    category_slug = "graphic-design"
    service_slug_part = "main"
    service = get_service_by_slug(category_slug, service_slug_part)
    assert service is not None
    assert isinstance(service, dict)
    assert service['slug'] == f"{category_slug}/{service_slug_part}"
    assert service['name'] == "Graphic Design"

def test_get_service_by_slug_invalid_category():
    service = get_service_by_slug("invalid-category", "realcard")
    assert service is None

def test_get_service_by_slug_invalid_service():
    service = get_service_by_slug("membership-cards", "invalid-service")
    assert service is None

def test_get_service_by_slug_mismatched_slugs():
    # Ensure it doesn't accidentally match a service from another category
    service = get_service_by_slug("printing", "realcard")
    assert service is None