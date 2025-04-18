"""
Consolidated Document Solutions Website Redesign Implementation
This script sets up a Flask-based website with modern frontend technologies
for the redesign of the Consolidated Document Solutions website.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_assets import Environment, Bundle
from werkzeug.utils import secure_filename
from datetime import datetime
import logging
import os

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-key' # Placeholder secret key
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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


assets.register('scss_all', scss_bundle)
assets.register('js_all', js_bundle)

# Site content - would typically come from a database
services = [
    {
        'id': 'commercial-printing',
        'title': 'Commercial Printing',
        'icon': 'printing-icon.svg',
        'description': 'We serve as a one-stop-shop for all your printing needs. Whether you need 5 or 50,000 copies.',
        'link': '/services/commercial-printing'
    },
    {
        'id': 'promotional-items',
        'title': 'Promotional Items',
        'icon': 'promo-icon.svg',
        'description': 'Since we handle a lot of our clients\' printing and other marketing needs, providing branded merchandise.',
        'link': '/services/promotional-items'
    },
    {
        'id': 'graphic-design',
        'title': 'Graphic Design',
        'icon': 'design-icon.svg',
        'description': 'Do you need a new logo, business form, T-Shirt design or brochure? Let our creative team help.',
        'link': '/services/graphic-design'
    },
    {
        'id': 'thermal-transfer-tags',
        'title': 'Thermal Transfer Tags',
        'icon': 'tags-icon.svg',
        'description': 'As a certified distributor of Inkanto Thermal Transfer Ribbons, our thermal tag solutions.',
        'link': '/services/thermal-transfer-tags'
    },
    {
        'id': 'packaging-fulfillment',
        'title': 'Packaging & Fulfillment',
        'icon': 'packaging-icon.svg',
        'description': 'We provide packaging and fulfillment services for a variety of industries and customer requirements.',
        'link': '/services/packaging-fulfillment'
    }
]

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

# Routes
@app.route('/')
def home():
    return render_template('index.html', 
                          services=services, 
                          testimonials=testimonials, 
                          year=datetime.now().year)

@app.route('/about')
def about():
    return render_template('about.html', year=datetime.now().year)

@app.route('/testimonials')
def testimonials_page():
    return render_template('testimonials.html', 
                          testimonials=testimonials, 
                          year=datetime.now().year)

@app.route('/industries')
def industries_page():
    return render_template('industries.html', 
                          industries=industries, 
                          year=datetime.now().year)

@app.route('/services/<service_id>')
def service_detail(service_id):
    # Find the requested service
    service = next((s for s in services if s['id'] == service_id), None)
    if service:
        return render_template('service_detail.html', 
                              service=service, 
                              year=datetime.now().year)
    return redirect(url_for('home'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        
        # Log the submitted data
        logging.info(f"Contact Form Submission: Name={name}, Email={email}, Message={message}")
        
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
        
    return render_template('contact.html', form=form, year=datetime.now().year)

@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(file_path)
            logging.info(f"File uploaded successfully: {filename}")
            flash(f'File "{filename}" uploaded successfully!', 'success')
            return redirect(url_for('file_upload'))
        except Exception as e:
            logging.error(f"Error saving file {filename}: {e}")
            flash(f'Error uploading file "{filename}". Please try again.', 'danger')
            
    return render_template('file_upload.html', form=form, year=datetime.now().year)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', year=datetime.now().year), 404

@app.errorhandler(500)
def server_error(e):
    logging.exception('An internal server error occurred')
    return render_template('500.html', year=datetime.now().year), 500

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
