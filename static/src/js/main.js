/**
 * Main JavaScript for Consolidated Document Solutions
 * This file contains common functionality used across all pages
 */

document.addEventListener('DOMContentLoaded', function() {
  // Initialize mobile menu
  initMobileMenu();
  
  // Initialize dropdowns
  initDropdowns();
  
  // Initialize hero slider if it exists
  if (document.querySelector('.hero-slider')) {
    initHeroSlider();
  }
  
  // Initialize testimonials slider if it exists
  if (document.querySelector('.testimonials-slider')) {
    initTestimonialsSlider();
  }
  
  // Initialize industries accordions if they exist
  if (document.querySelector('.industries-list-page')) {
    initIndustriesAccordion();
  }
  
  // Initialize file upload if it exists
  if (document.querySelector('.file-upload-section')) {
    initFileUpload();
  }
  
  // Initialize back to top button
  initBackToTop();
  
  // Add animation on scroll
  initScrollAnimation();

  // Initialize quote request form validation if it exists
  if (document.querySelector('form[method="POST"]')) { // Assuming the quote request form is the only POST form without a specific ID
    initQuoteRequestFormValidation();
  }
});

/**
 * Initialize mobile menu functionality
 */
function initMobileMenu() {
  const menuToggle = document.querySelector('.mobile-menu-toggle');
  const mainNav = document.querySelector('.main-nav');
  
  if (!menuToggle || !mainNav) return;
  
  menuToggle.addEventListener('click', function() {
    menuToggle.classList.toggle('active');
    mainNav.classList.toggle('active');
    
    // Prevent body scrolling when menu is open
    document.body.classList.toggle('menu-open');
  });
  
  // Close menu when clicking outside
  document.addEventListener('click', function(event) {
    if (!event.target.closest('.mobile-menu-toggle') && !event.target.closest('.main-nav') && mainNav.classList.contains('active')) {
      menuToggle.classList.remove('active');
      mainNav.classList.remove('active');
      document.body.classList.remove('menu-open');
    }
  });
}

/**
 * Initialize dropdown functionality on mobile devices
 */
function initDropdowns() {
  const dropdowns = document.querySelectorAll('.nav-dropdown > a');
  
  dropdowns.forEach(dropdown => {
    dropdown.addEventListener('click', function(e) {
      // Only activate on mobile
      if (window.innerWidth <= 992) {
        e.preventDefault();
        
        const dropdownContent = this.nextElementSibling;
        dropdownContent.classList.toggle('active');
        
        // Close other dropdowns
        dropdowns.forEach(otherDropdown => {
          if (otherDropdown !== dropdown) {
            otherDropdown.nextElementSibling.classList.remove('active');
          }
        });
      }
    });
  });
  
  // Reset dropdowns on window resize
  window.addEventListener('resize', function() {
    if (window.innerWidth > 992) {
      document.querySelectorAll('.dropdown-content').forEach(dropdown => {
        dropdown.classList.remove('active');
      });
      
      document.querySelector('.mobile-menu-toggle')?.classList.remove('active');
      document.querySelector('.main-nav')?.classList.remove('active');
      document.body.classList.remove('menu-open');
    }
  });
}

/**
 * Initialize hero slider functionality
 */
function initHeroSlider() {
  const slides = document.querySelectorAll('.hero-slider .slide');
  const dots = document.querySelectorAll('.hero-slider .slider-dot');
  const nextBtn = document.querySelector('.hero-slider .slider-next');
  const prevBtn = document.querySelector('.hero-slider .slider-prev');
  
  if (slides.length === 0) return;
  
  let currentSlide = 0;
  let interval;
  
  // Show a specific slide
  function showSlide(index) {
    if (index >= slides.length) {
      currentSlide = 0;
    } else if (index < 0) {
      currentSlide = slides.length - 1;
    } else {
      currentSlide = index;
    }
    
    // Hide all slides
    slides.forEach(slide => {
      slide.classList.remove('active');
      slide.setAttribute('aria-hidden', 'true');
    });
    
    // Deactivate all dots
    dots.forEach(dot => {
      dot.classList.remove('active');
      dot.setAttribute('aria-current', 'false');
    });
    
    // Show current slide
    slides[currentSlide].classList.add('active');
    slides[currentSlide].setAttribute('aria-hidden', 'false');
    
    // Activate current dot
    if (dots[currentSlide]) {
      dots[currentSlide].classList.add('active');
      dots[currentSlide].setAttribute('aria-current', 'true');
    }
  }
  
  // Go to the next slide
  function nextSlide() {
    showSlide(currentSlide + 1);
  }
  
  // Go to the previous slide
  function prevSlide() {
    showSlide(currentSlide - 1);
  }
  
  // Start auto sliding
  function startAutoSlide() {
    interval = setInterval(() => {
      nextSlide();
    }, 5000);
  }
  
  // Stop auto sliding
  function stopAutoSlide() {
    clearInterval(interval);
  }
  
  // Add event listeners
  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      nextSlide();
      stopAutoSlide();
      startAutoSlide();
    });
  }
  
  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      prevSlide();
      stopAutoSlide();
      startAutoSlide();
    });
  }
  
  // Add event listeners to dots
  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      showSlide(index); // Corrected function call
      stopAutoSlide();
      startAutoSlide();
    });
  });
  
  // Initialize
  showTestimonial(0);
}

/**
 * Initialize industries accordion functionality
 */
function initIndustriesAccordion() {
  const industryToggles = document.querySelectorAll('.industry-toggle');
  
  industryToggles.forEach(toggle => {
    toggle.addEventListener('click', function() {
      const industryItem = this.closest('.industry-item');
      
      // Toggle active class
      industryItem.classList.toggle('active');
      
      // Toggle aria-expanded attribute for accessibility
      const expanded = industryItem.classList.contains('active');
      this.setAttribute('aria-expanded', expanded);
      
      // Close other accordions if needed
      if (expanded) {
        industryToggles.forEach(otherToggle => {
          if (otherToggle !== toggle) {
            const otherItem = otherToggle.closest('.industry-item');
            otherItem.classList.remove('active');
            otherToggle.setAttribute('aria-expanded', 'false');
          }
        });
      }
    });
  });
  
  // Set the first item as active by default
  if (industryToggles.length > 0) {
    const firstIndustry = industryToggles[0].closest('.industry-item');
    firstIndustry.classList.add('active');
    industryToggles[0].setAttribute('aria-expanded', 'true');
  }
}

/**
 * Initialize file upload functionality
 */
function initFileUpload() {
  const uploadArea = document.querySelector('.upload-area');
  const fileInput = document.querySelector('.file-input');
  const fileList = document.querySelector('.file-list');
  
  if (!uploadArea || !fileInput || !fileList) return;
  
  // Handle click on upload area
  uploadArea.addEventListener('click', () => {
    fileInput.click();
  });
  
  // Handle drag and drop events
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, preventDefaults, false);
  });
  
  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }
  
  // Handle drag enter and drag over
  ['dragenter', 'dragover'].forEach(eventName => {
    uploadArea.addEventListener(eventName, () => {
      uploadArea.classList.add('active');
    });
  });
  
  // Handle drag leave and drop
  ['dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, () => {
      uploadArea.classList.remove('active');
    });
  });
  
  // Handle dropped files
  uploadArea.addEventListener('drop', (e) => {
    const droppedFiles = e.dataTransfer.files;
    handleFiles(droppedFiles);
  });
  
  // Handle selected files
  fileInput.addEventListener('change', () => {
    const selectedFiles = fileInput.files;
    handleFiles(selectedFiles);
  });
  
  // Process files
  function handleFiles(files) {
    if (!files.length) return;
    
    [...files].forEach(file => {
      addFileToList(file);
    });
    
    // Reset the file input to allow selecting the same file again
    fileInput.value = '';
  }
  
  // Add file to the list
  function addFileToList(file) {
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    
    // Get file extension
    const extension = file.name.split('.').pop().toLowerCase();
    
    // File icon based on type
    let fileIcon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>';
    
    // Use specific icons for common file types
    if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg'].includes(extension)) {
      fileIcon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>';
    } else if (['pdf'].includes(extension)) {
      fileIcon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><path d="M9 15L12 15 12 18M12 15L12 12M15 12L15 18"></path></svg>';
    } else if (['zip', 'rar', '7z', 'tar', 'gz'].includes(extension)) {
      fileIcon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="7.5 4.21 12 6.81 16.5 4.21"></polyline><polyline points="7.5 19.79 7.5 14.6 3 12"></polyline><polyline points="21 12 16.5 14.6 16.5 19.79"></polyline><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>';
    }
    
    // Format file size
    const fileSize = formatFileSize(file.size);
    
    // Create file item content
    fileItem.innerHTML = `
      ${fileIcon}
      <div class="file-name">${file.name}</div>
      <div class="file-size">${fileSize}</div>
      <button type="button" class="file-remove">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </button>
    `;
    
    // Add remove button functionality
    fileItem.querySelector('.file-remove').addEventListener('click', () => {
      fileItem.remove();
    });
    
    // Add to the list
    fileList.appendChild(fileItem);
  }
  
  // Format file size
  function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}

/**
 * Initialize back to top button
 */
function initBackToTop() {
  const backToTopBtn = document.querySelector('.back-to-top');
  
  if (!backToTopBtn) return;
  
  // Show/hide button based on scroll position
  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
      backToTopBtn.classList.add('visible');
    } else {
      backToTopBtn.classList.remove('visible');
    }
  });
  
  // Scroll to top when clicked
  backToTopBtn.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

/**
 * Initialize scroll animation
 */
function initScrollAnimation() {
  // Get all elements to animate
  const animatedElements = document.querySelectorAll('.fade-in, .slide-up, .slide-in-left, .slide-in-right');
  
  if (animatedElements.length === 0) return;
  
  // Check if element is in viewport
  function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    const offset = 100; // Start animation before the element is fully in view
    return (
      rect.top <= window.innerHeight - offset &&
      rect.bottom >= 0
    );
  }
  
  // Add animation class when element is in viewport
  function handleScroll() {
    animatedElements.forEach(element => {
      if (isInViewport(element)) {
        element.classList.add('animate');
      }
    });
  }
  
  // Initial check
  handleScroll();
  
  // Check on scroll
  window.addEventListener('scroll', handleScroll);
}
  // Add swipe functionality for touch devices
  let touchStartX = 0;
  let touchEndX = 0;

  const slider = document.querySelector('.hero-slider');

  slider.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
  }, {passive: true});

  slider.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  }, {passive: true});

  function handleSwipe() {
    const threshold = 50; // Minimum swipe distance

    if (touchEndX < touchStartX - threshold) {
      // Swipe left
      nextSlide();
      stopAutoSlide();
      startAutoSlide();
    } else if (touchEndX > touchStartX + threshold) {
      // Swipe right
      prevSlide();
      stopAutoSlide();
      startAutoSlide();
    }
  }

  // Pause auto sliding when hovering over the slider
  slider.addEventListener('mouseenter', stopAutoSlide);
  slider.addEventListener('mouseleave', startAutoSlide);

  // Initialize
  showSlide(0);
  startAutoSlide();
/**
 * Initialize testimonials slider functionality
 */
function initTestimonialsSlider() {
  const testimonials = document.querySelectorAll('.testimonials-slider .testimonial-card');
  const dots = document.querySelectorAll('.testimonials-dots .testimonial-dot');
  const nextBtn = document.querySelector('.testimonials-next');
  const prevBtn = document.querySelector('.testimonials-prev');
  
  if (testimonials.length === 0) return;
  
  let currentTestimonial = 0;
  
  // Show a specific testimonial
  function showTestimonial(index) {
    if (index >= testimonials.length) {
      currentTestimonial = 0;
    } else if (index < 0) {
      currentTestimonial = testimonials.length - 1;
    } else {
      currentTestimonial = index;
    }
    
    // Hide all testimonials
    testimonials.forEach(testimonial => {
      testimonial.classList.remove('active');
    });
    
    // Deactivate all dots
    dots.forEach(dot => {
      dot.classList.remove('active');
    });
    
    // Show current testimonial
    testimonials[currentTestimonial].classList.add('active');
    
    // Activate current dot
    if (dots[currentTestimonial]) {
      dots[currentTestimonial].classList.add('active');
    }
  }
  
  // Go to the next testimonial
  function nextTestimonial() {
    showTestimonial(currentTestimonial + 1);
  }
  
  // Go to the previous testimonial
  function prevTestimonial() {
    showTestimonial(currentTestimonial - 1);
  }
  
  // Add event listeners
  if (nextBtn) {
    nextBtn.addEventListener('click', nextTestimonial);
  }
  
  if (prevBtn) {
    prevBtn.addEventListener('click', prevTestimonial);
  }
  
  // Add event listeners to dots
  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      showTestimonial(index);
      stopAutoSlide();
      startAutoSlide();
    });
  });

  // Start auto sliding
  function startAutoSlide() {
    interval = setInterval(() => {
      nextTestimonial();
    }, 7000); // Auto slide every 7 seconds
  }

  // Stop auto sliding
  function stopAutoSlide() {
    clearInterval(interval);
  }

  // Pause auto sliding when hovering over the slider
  const slider = document.querySelector('.testimonials-slider');
  if (slider) {
    slider.addEventListener('mouseenter', stopAutoSlide);
    slider.addEventListener('mouseleave', startAutoSlide);
  }

  // Initialize
  showTestimonial(0);
  startAutoSlide();
}

/**
 * Add client-side validation for the contact form.
 */
function initContactFormValidation() {
  const contactForm = document.querySelector('#contact-form');

  if (!contactForm) return;

  contactForm.addEventListener('submit', function(event) {
    let isValid = true;
    const nameInput = contactForm.querySelector('#name');
    const emailInput = contactForm.querySelector('#email');
    const messageInput = contactForm.querySelector('#message');

    // Simple validation: check if fields are not empty
    if (!nameInput.value.trim()) {
      displayError(nameInput, 'Name is required.');
      isValid = false;
    } else {
      clearError(nameInput);
    }

    if (!emailInput.value.trim()) {
      displayError(emailInput, 'Email is required.');
      isValid = false;
    } else if (!isValidEmail(emailInput.value.trim())) {
      displayError(emailInput, 'Please enter a valid email address.');
      isValid = false;
    } else {
      clearError(emailInput);
    }

    if (!messageInput.value.trim()) {
      displayError(messageInput, 'Message is required.');
      isValid = false;
    } else {
      clearError(messageInput);
    }

    if (!isValid) {
      event.preventDefault(); // Prevent form submission if invalid
    }
  });

  // Helper function to display error messages
  function displayError(inputElement, message) {
    // Remove existing error messages
    clearError(inputElement);

    const errorElement = document.createElement('div');
    errorElement.classList.add('error-message');
    errorElement.style.color = 'red'; // Simple styling
    errorElement.textContent = message;

    // Insert error message after the input element
    inputElement.parentNode.insertBefore(errorElement, inputElement.nextSibling);
  }

  // Helper function to clear error messages
  function clearError(inputElement) {
    const existingError = inputElement.nextElementSibling;
    if (existingError && existingError.classList.contains('error-message')) {
      existingError.remove();
    }
  }

  // Helper function to validate email format
  function isValidEmail(email) {
    // Basic email regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}

/**
 * Add client-side validation for the file upload form.
 */
function initFileUploadValidation() {
  const uploadForm = document.querySelector('#upload-form');

  if (!uploadForm) return;

  uploadForm.addEventListener('submit', function(event) {
    const fileInput = uploadForm.querySelector('#file-input');
    const fileList = uploadForm.querySelector('.file-list'); // Assuming file list shows selected files

    // Check if any files have been added to the list
    if (!fileList || fileList.children.length === 0) {
      alert('Please select a file to upload.'); // Simple alert for now
      event.preventDefault(); // Prevent form submission
    }
  });
}

/**
 * Implement smooth animations for dropdown menus.
 * Assumes CSS transitions/animations are defined for .dropdown-menu.active
 */
function initAnimatedDropdowns() {
  const dropdownToggles = document.querySelectorAll('nav .dropdown > a');

  dropdownToggles.forEach(toggle => {
    const dropdownMenu = toggle.nextElementSibling;

    if (!dropdownMenu || !dropdownMenu.classList.contains('dropdown-menu')) return;

    // Prevent default link behavior for dropdown toggles
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      // Toggle active class to trigger CSS animation
      dropdownMenu.classList.toggle('active');

      // Close other dropdowns
      dropdownToggles.forEach(otherToggle => {
        const otherDropdownMenu = otherToggle.nextElementSibling;
        if (otherToggle !== toggle && otherDropdownMenu && otherDropdownMenu.classList.contains('dropdown-menu')) {
          otherDropdownMenu.classList.remove('active');
        }
      });
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
      if (!toggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.classList.remove('active');
      }
    });
  });

  // Close dropdowns on window resize if they become non-mobile
  window.addEventListener('resize', function() {
    if (window.innerWidth > 992) { // Assuming 992px is the mobile breakpoint
      document.querySelectorAll('.dropdown-menu').forEach(menu => {
        menu.classList.remove('active');
      });
    }
  });
}

// Add new initializations to DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
  // Initialize mobile menu
  initMobileMenu();

  // Initialize dropdowns (replace with animated version)
  // initDropdowns(); // Commented out or removed

  // Initialize animated dropdowns
  initAnimatedDropdowns();

  // Initialize hero slider if it exists
  if (document.querySelector('.hero-slider')) {
    initHeroSlider();
  }

  // Initialize testimonials slider if it exists
  if (document.querySelector('.testimonials-slider')) {
    initTestimonialsSlider();
  }

  // Initialize industries accordions if they exist
  if (document.querySelector('.industries-list-page')) {
    initIndustriesAccordion();
  }

  // Initialize file upload if it exists
  if (document.querySelector('.file-upload-section')) {
    initFileUpload();
  }

  // Initialize back to top button
  initBackToTop();

  // Add animation on scroll
  initScrollAnimation();

  // Initialize form validations
  initContactFormValidation();
  initFileUploadValidation();
  initFileUploadValidation();
  initQuoteRequestFormValidation(); // Add call to quote request form validation
});

/**
 * Initialize quote request form validation
 */
function initQuoteRequestFormValidation() {
  const form = document.querySelector('form[method="POST"]'); // Target the quote request form

  if (!form) return;

  form.addEventListener('submit', function(event) {
    let isValid = true;

    // Clear previous errors
    form.querySelectorAll('.error-message').forEach(error => error.remove());
    form.querySelectorAll('.form-control').forEach(input => input.classList.remove('is-invalid'));

    // Get form elements
    const nameInput = form.querySelector('#name');
    const emailInput = form.querySelector('#email');
    const industryInput = form.querySelector('#industry');
    const serviceTypeInput = form.querySelector('#service_type');
    const detailsInput = form.querySelector('#details');

    // Validate Name
    if (nameInput && nameInput.value.trim() === '') {
      displayError(nameInput, 'Name is required.');
      isValid = false;
    }

    // Validate Email
    if (emailInput) {
      if (emailInput.value.trim() === '') {
        displayError(emailInput, 'Email is required.');
        isValid = false;
      } else if (!isValidEmail(emailInput.value)) {
        displayError(emailInput, 'Please enter a valid email address.');
        isValid = false;
      }
    }

    // Validate Industry
    if (industryInput && industryInput.value.trim() === '') {
       displayError(industryInput, 'Industry is required.');
       isValid = false;
    }

    // Validate Service Type
    if (serviceTypeInput && serviceTypeInput.value.trim() === '') {
       displayError(serviceTypeInput, 'Service Type is required.');
       isValid = false;
    }

    // Validate Details
    if (detailsInput && detailsInput.value.trim() === '') {
       displayError(detailsInput, 'Details are required.');
       isValid = false;
    }


    if (!isValid) {
      event.preventDefault(); // Prevent form submission if invalid
    }
  });

  // Helper function to display error messages
  function displayError(inputElement, message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message text-danger'; // Add a class for styling
    errorElement.textContent = message;
    inputElement.classList.add('is-invalid'); // Add a class to the input for styling
    inputElement.parentNode.insertBefore(errorElement, inputElement.nextSibling);
  }

  // Helper function to clear error messages (already handled at the start of submit)
  // function clearError(inputElement) {
  //   const errorElement = inputElement.parentNode.querySelector('.error-message');
  //   if (errorElement) {
  //     errorElement.remove();
  //     inputElement.classList.remove('is-invalid');
  //   }
  // }

  // Basic email validation regex
  function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  }
}
// --- Mega Menu Logic ---
document.addEventListener('DOMContentLoaded', () => {
    const servicesDropdown = document.querySelector('.nav-dropdown a[href*="services_index"]'); // Find the main P&S link
    if (!servicesDropdown) return; // Exit if not found

    const megaMenuContainer = servicesDropdown.closest('.nav-dropdown'); // Get the parent li.nav-dropdown
    if (!megaMenuContainer) return;

    const leftColumnItems = megaMenuContainer.querySelectorAll('.mega-menu-column-left ul li[data-category-slug]');
    const submenuDisplayArea = megaMenuContainer.querySelector('#submenu-display-area');
    const serviceDataElement = document.getElementById('service-categories-data');

    if (!leftColumnItems.length || !submenuDisplayArea || !serviceDataElement) {
        console.error("Mega menu elements not found.");
        return; // Exit if essential elements are missing
    }

    // Parse the embedded service data
    let serviceCategoriesData = {};
    try {
        serviceCategoriesData = JSON.parse(serviceDataElement.textContent);
    } catch (e) {
        console.error("Error parsing service categories JSON data:", e);
        return; // Exit if data parsing fails
    }

    // Function to generate URL (basic version, assumes standard Flask routing)
    // In a real Flask app, you might pass url_for endpoints via JS variables if needed
    function generateServiceUrl(categorySlug, serviceSlug) {
        // Adjust this path based on your actual Flask route structure if different
        return `/services/${categorySlug}/${serviceSlug}`;
    }

    // Function to update the right column
    function updateSubmenu(categorySlug) {
        submenuDisplayArea.innerHTML = ''; // Clear previous items
        const category = serviceCategoriesData[categorySlug];

        if (category && category.services) {
            // Check if it has 'real' sub-services
            const hasSubServices = category.services.length > 1 || (category.services.length === 1 && category.services[0].slug !== 'main');

            if (hasSubServices) {
                category.services.forEach(service => {
                    const li = document.createElement('li');
                    const a = document.createElement('a');
                    a.href = generateServiceUrl(category.slug, service.slug);
                    a.textContent = service.name;
                    li.appendChild(a);
                    submenuDisplayArea.appendChild(li);
                });
            } else {
                // If only 'main' service or no 'real' subs, maybe show category description or link?
                // For now, show a message or leave blank. Let's show a message.
                 const li = document.createElement('li');
                 li.classList.add('submenu-placeholder'); // Reuse placeholder class
                 // Link the main category name directly if no distinct sub-services
                 if (category.services.length === 1 && category.services[0].slug === 'main') {
                     const a = document.createElement('a');
                     a.href = generateServiceUrl(category.slug, 'main');
                     a.textContent = `View ${category.name} Details`;
                     li.appendChild(a);
                 } else {
                    li.textContent = category.description || `Explore ${category.name}`; // Show description or default text
                 }
                 submenuDisplayArea.appendChild(li);
            }
        } else {
            // Handle case where category data might be missing or has no services array
             const li = document.createElement('li');
             li.classList.add('submenu-placeholder');
             li.textContent = 'No services listed for this category.';
             submenuDisplayArea.appendChild(li);
        }
    }

    // Add hover listeners to left column items
    leftColumnItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            // Remove active class from all items
            leftColumnItems.forEach(i => i.classList.remove('active'));
            // Add active class to the hovered item
            item.classList.add('active');
            // Update the right column
            const categorySlug = item.getAttribute('data-category-slug');
            updateSubmenu(categorySlug);
        });
    });

    // Optional: Clear submenu when mouse leaves the entire mega menu
    megaMenuContainer.addEventListener('mouseleave', () => {
        // Reset to default placeholder or clear
        submenuDisplayArea.innerHTML = '<li class="submenu-placeholder">Hover over a category to see services.</li>';
        leftColumnItems.forEach(i => i.classList.remove('active')); // Remove active class
    });
});
// --- End Mega Menu Logic ---