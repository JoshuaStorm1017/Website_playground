"""
Consolidated Document Solutions Website Redesign Implementation
This script sets up a Flask-based website with modern frontend technologies
for the redesign of the Consolidated Document Solutions website.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_wtf.csrf import CSRFProtect
from flask_assets import Environment, Bundle
from werkzeug.utils import secure_filename
from datetime import datetime
import logging
import os

from flask_wtf import FlaskForm
from forms import QuoteForm # Import the QuoteForm from forms.py
from wtforms import StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed

app = Flask(__name__)
# Load SECRET_KEY from environment variable for production
# Required Environment Variables:
# SECRET_KEY: A strong, random string for security purposes (e.g., session management, CSRF protection)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-fallback-secret-key-for-development') # Fallback for development, use env var in production
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Configure logging
# Log to standard output for production environments (e.g., Docker, systemd)
# Logging level can be configured via environment variable LOG_LEVEL (e.g., INFO, DEBUG, WARNING, ERROR)
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=getattr(logging, log_level), format='%(asctime)s - %(levelname)s - %(message)s')

# Define WTForms
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

class UploadForm(FlaskForm):
    file = FileField('Select File', validators=[FileRequired(), FileAllowed(['pdf', 'doc', 'docx', 'txt'], 'PDFs, Documents, and Text files only!')])
    submit = SubmitField('Upload File')

# Setup Flask-Assets for SCSS processing and JS bundling
assets = Environment(app)
assets.load_path = ['static/src/scss', 'static/src/js']

# Bundle and minify SCSS and JS
scss_bundle = Bundle(
    'main.scss', 
    'components.scss', 
    'responsive.scss',
    filters='libsass,cssmin', 
    output='css/main.min.css'
)

js_bundle = Bundle(
    'main.js', 
    filters='jsmin', 
    output='js/main.min.js'
)

assets.register('scss_all', scss_bundle)
assets.register('js_all', js_bundle)

# Updated hierarchical service data structure
# Slugs are used for URL generation (e.g., /services/category-slug/service-slug)
# Details/benefits are placeholders.
service_categories = {
    "membership-cards": {
        "slug": "membership-cards",
        "name": "Membership Cards",
        "description": "Durable and professional membership cards for various applications.", # Optional category description
        "services": [
            {"slug": "realcard", "name": "RealCard®", "details": "Placeholder details for RealCard®.", "benefits": "Placeholder benefits for RealCard®."},
            {"slug": "docucopy-integrated", "name": "DocuCopy® Integrated ID Cards", "details": "Placeholder details for DocuCopy®.", "benefits": "Placeholder benefits for DocuCopy®."},
            {"slug": "poly-ez-release", "name": "Poly EZ Release Membership Cards", "details": "Placeholder details for Poly EZ Release.", "benefits": "Placeholder benefits for Poly EZ Release."},
            {"slug": "integrated-membership", "name": "Integrated Membership Cards", "details": "Placeholder details for Integrated Membership.", "benefits": "Placeholder benefits for Integrated Membership."},
            {"slug": "laserwell", "name": "LaserWell Membership Cards", "details": "Placeholder details for LaserWell.", "benefits": "Placeholder benefits for LaserWell."},
            {"slug": "heavy-gauge-plastic", "name": "Heavy Gauge Plastic Cards", "details": "Placeholder details for Heavy Gauge Plastic.", "benefits": "Placeholder benefits for Heavy Gauge Plastic."},
        ]
    },
    "printing": {
        "slug": "printing",
        "name": "Printing",
        "description": "Comprehensive printing solutions for businesses.",
        "services": [
            {"slug": "commercial-printing", "name": "Commercial Printing", "details": "Placeholder details for Commercial Printing.", "benefits": "Placeholder benefits for Commercial Printing."},
            {"slug": "digital-printing", "name": "Digital Printing Services", "details": "Placeholder details for Digital Printing.", "benefits": "Placeholder benefits for Digital Printing."},
            {"slug": "business-forms", "name": "Business Forms", "details": "Placeholder details for Business Forms.", "benefits": "Placeholder benefits for Business Forms."},
            {"slug": "tags-labels", "name": "Tags & Labels", "details": "Placeholder details for Tags & Labels.", "benefits": "Placeholder benefits for Tags & Labels."},
        ]
    },
    "thermal-transfer-printing": { # Renamed slug for clarity
        "slug": "thermal-transfer-printing",
        "name": "Thermal Transfer Printing",
        "description": "High-quality thermal printing supplies.",
        "services": [
            {"slug": "thermal-tags", "name": "Thermal Tags", "details": "Placeholder details for Thermal Tags.", "benefits": "Placeholder benefits for Thermal Tags."},
            {"slug": "thermal-labels", "name": "Thermal Labels", "details": "Placeholder details for Thermal Labels.", "benefits": "Placeholder benefits for Thermal Labels."},
            {"slug": "thermal-ribbon", "name": "Thermal Ribbon", "details": "Placeholder details for Thermal Ribbon.", "benefits": "Placeholder benefits for Thermal Ribbon."},
        ]
    },
    "packaging-fulfillment": {
        "slug": "packaging-fulfillment",
        "name": "Packaging & Fulfillment",
        "description": "Streamlined packaging and fulfillment services.",
        "services": [
             # For categories without sub-services, we list the main service itself.
             # The slug here is just 'main' as it represents the core service of the category.
             {"slug": "main", "name": "Packaging & Fulfillment", "details": "Placeholder details for Packaging & Fulfillment.", "benefits": "Placeholder benefits for Packaging & Fulfillment."}
        ]
    },
    "graphic-design": {
        "slug": "graphic-design",
        "name": "Graphic Design",
        "description": "Creative graphic design services to elevate your brand.",
        "services": [
            {"slug": "main", "name": "Graphic Design", "details": "Placeholder details for Graphic Design. Upload your files [here]({file_upload_url}) or view our [artwork specifications]({artwork_specs_url}).", "benefits": "Placeholder benefits for Graphic Design.", "needs_links": True} # Flag for special links
        ]
    },
    "embroidery-screenprinting": {
        "slug": "embroidery-screenprinting",
        "name": "Embroidery & Screen printing", # Keep name as is
        "description": "Custom apparel decoration.",
        "services": [
            {"slug": "main", "name": "Embroidery & Screen printing", "details": "Placeholder details for Embroidery & Screen printing.", "benefits": "Placeholder benefits for Embroidery & Screen printing."}
        ]
    }
}

# Helper functions
def get_all_categories():
    """Returns a list of all service categories."""
    # Return categories sorted alphabetically by name
    return sorted(service_categories.values(), key=lambda cat: cat['name'])

def get_services_by_category(category_slug):
    """Returns the list of services for a given category slug."""
    category = service_categories.get(category_slug)
    return category['services'] if category else []

def get_service_by_slug(category_slug, service_slug):
    """Finds a specific service by its category and service slugs."""
    category = service_categories.get(category_slug)
    if category:
        # Construct the expected full slug
        # Find service by its own slug within the category's services list
        for service in category['services']:
            # Service slug is now relative to the category (e.g., 'realcard', not 'membership-cards/realcard')
            if service['slug'] == service_slug:
                # Add category info to the service dict for context in the template
                service_with_category_info = service.copy()
                service_with_category_info['category_slug'] = category_slug
                service_with_category_info['category_name'] = category['name']
                return service_with_category_info
    return None


@app.context_processor
def inject_categories():
   """Injects service categories into the template context."""
   # Sort categories alphabetically by name for consistent display
   sorted_categories = dict(sorted(service_categories.items(), key=lambda item: item[1]['name']))
   return dict(service_categories=sorted_categories)


# Sample industries served
industries = [
    'Accountants & Accounting Firms',
    'Advertising Agencies',
    'Automotive',
    'Churches',
    'Country Clubs / Golf Courses',
    'Fuel & Oil',
    'Healthcare / Pharmaceutical',
    'Horticulture / Farms / Nursery',
    'Industrial / Manufacturing',
    'Insurance',
    'Metals / Metal Processing',
    'Municipalities',
    'Museums',
    'Nonprofits / Charitable Organizations',
    'Real Estate',
    'Robotics',
    'Schools / Colleges'
]

# Sample testimonials
testimonials = [
    {
        'content': 'Our non-profit charity has been using Consolidated Document Solutions for all our printing needs for over six years. Their designs are professional, and the quality is outstanding and consistent.',
        'author': 'Larry Collette',
        'company': 'Special Dreams Farm'
    },
    {
        'content': 'Since I found Consolidated Document Solutions, I have never gone back to my other vendors. I can bring Beth any project and the print team can find a way to make it work.',
        'author': 'Erica Rivord',
        'company': 'Eastside Eye Physicians'
    },
    {
        'content': 'I just wanted to let you know how impressed I am with your talent. When I leave the creative part of my marketing to you, I am constantly impressed with your artistic eye.',
        'author': 'Bill The Realtor',
        'company': ''
    }
]

@app.context_processor
def inject_categories():
    """Injects service categories into the context for all templates."""
    # You might want to sort them here if needed consistently
    # sorted_categories = sorted(service_categories.values(), key=lambda cat: cat['name'])
    return dict(categories=service_categories.values()) # Pass the list of category dicts

# Routes
@app.route('/')
def home():
    """Renders the home page with services and testimonials."""
    return render_template('index.html',
                           testimonials=testimonials,
                           year=datetime.now().year)

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html', year=datetime.now().year)

@app.route('/testimonials')
def testimonials_page():
    """Renders the testimonials page."""
    return render_template('testimonials.html',
                           testimonials=testimonials,
                           year=datetime.now().year)

@app.route('/industries')
def industries_page():
    """Renders the industries page."""
    return render_template('industries.html',
                           industries=industries,
                           year=datetime.now().year)

@app.route('/services/<category_slug>/<service_slug>')
def service_detail(category_slug, service_slug):
    """Renders the detail page for a specific service within a category."""
    service = get_service_by_slug(category_slug, service_slug)
    if service:
        # Handle special links for Graphic Design
        if service.get('needs_links'):
            service['details'] = service['details'].format(
                file_upload_url=url_for('file_upload'),
                artwork_specs_url=url_for('artwork_specifications') # Use url_for for the new route
            )
        return render_template('service_detail.html',
                               service=service, # service dict now includes category info
                               year=datetime.now().year)
    else:
        # Use abort(404) for cleaner handling of not found errors
        from flask import abort
        logging.warning(f"Service not found for category '{category_slug}' and service '{service_slug}'")
        abort(404) # Flask will automatically render the 404 error page

@app.route('/services')
def services_index():
    """Renders the index page for all service categories."""
    categories = get_all_categories()
    return render_template('services_index.html',
                           categories=categories, # Pass categories instead of flat services list
                           year=datetime.now().year)

@app.route('/quote_request', methods=['GET', 'POST'])
def quote_request():
    """Handles the quote request form submission and renders the quote request page."""
    form = QuoteForm()
    if form.validate_on_submit():
        # Process form data on POST request
        name = form.name.data
        email = form.email.data
        company = form.company.data
        service = form.service_interested_in.data
        message = form.message.data

        # Basic input sanitization (escaping for display in flash message)
        from markupsafe import escape
        sanitized_name = escape(name)
        sanitized_email = escape(email)
        sanitized_company = escape(company)
        sanitized_service = escape(service)
        sanitized_message = escape(message)


        # Log the submitted data (replace with actual processing/email sending later)
        logging.info(f"Quote Request Submission: Name={sanitized_name}, Email={sanitized_email}, Company={sanitized_company}, Service={sanitized_service}, Message={sanitized_message}")

        # Show success message and redirect to avoid form resubmission
        flash('Your quote request has been sent successfully!', 'success')
        return redirect(url_for('quote_request'))

    # Render the quote request page with the form on GET request or if validation fails
    return render_template('quote_request.html', form=form, year=datetime.now().year)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handles the contact form submission and renders the contact page."""
    form = ContactForm()
    if form.validate_on_submit():
        # Process form data on POST request
        name = form.name.data
        email = form.email.data
        message = form.message.data
        
        # Log the submitted data (replace with actual email sending later)
        logging.info(f"Contact Form Submission: Name={name}, Email={email}, Message={message}")
        
        # Show success message and redirect to avoid form resubmission
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
        
    # Render the contact page with the form on GET request or if validation fails
    return render_template('contact.html', form=form, year=datetime.now().year)

@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    """Handles file uploads and renders the file upload page."""
    form = UploadForm()
    if form.validate_on_submit():
        # Process file upload on POST request
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            # Save the uploaded file
            file.save(file_path)
            logging.info(f"File uploaded successfully: {filename}")
            flash(f'File "{filename}" uploaded successfully!', 'success')
            # Redirect to the upload page after successful upload
            return redirect(url_for('file_upload'))
        except Exception as e:
            # Log error and show error message if saving fails
            logging.error(f"Error saving file {filename}: {e}")
            flash(f'Error uploading file "{filename}". Please try again.', 'danger')
            
    # Render the upload page with the form on GET request or if validation fails
    return render_template('file_upload.html', form=form, year=datetime.now().year)

@app.route('/resources/artwork-specifications')
def artwork_specifications():
    """Renders the artwork specifications page."""
    # This route assumes a template named 'artwork_specifications.html' exists
    # in the 'templates' folder.
    return render_template('artwork_specifications.html', year=datetime.now().year)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    """Renders the custom 404 error page."""
    return render_template('404.html', year=datetime.now().year), 404

@app.errorhandler(500)
def server_error(e):
    """Renders the custom 500 error page and logs the exception."""
    logging.exception('An internal server error occurred')
    return render_template('500.html', year=datetime.now().year), 500

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
