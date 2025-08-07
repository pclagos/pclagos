// Custom JavaScript for PC Repair Services

document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add fade-in animation to cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="loading"></span> Enviando...';
                submitBtn.disabled = true;
            }
        });
    });

    // WhatsApp button functionality
    const whatsappButtons = document.querySelectorAll('a[href*="wa.me"]');
    whatsappButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add tracking or analytics here if needed
            console.log('WhatsApp button clicked');
        });
    });

    // Contact form enhancement
    const contactForm = document.querySelector('#contact-form');
    if (contactForm) {
        const phoneInput = contactForm.querySelector('input[name="phone"]');
        if (phoneInput) {
            phoneInput.addEventListener('input', function(e) {
                // Format phone number
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 0) {
                    value = '+' + value;
                }
                e.target.value = value;
            });
        }
    }

    // Appointment form date validation
    const appointmentForm = document.querySelector('#appointment-form');
    if (appointmentForm) {
        const dateInput = appointmentForm.querySelector('input[type="date"]');
        if (dateInput) {
            // Set minimum date to today
            const today = new Date().toISOString().split('T')[0];
            dateInput.min = today;
            
            dateInput.addEventListener('change', function(e) {
                const selectedDate = new Date(e.target.value);
                const today = new Date();
                
                if (selectedDate < today) {
                    alert('Por favor selecciona una fecha futura.');
                    e.target.value = '';
                }
            });
        }
    }

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // Service cards hover effect
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Gallery image modal
    const galleryImages = document.querySelectorAll('.gallery-img');
    galleryImages.forEach(img => {
        img.addEventListener('click', function() {
            const modal = document.createElement('div');
            modal.className = 'modal fade';
            modal.innerHTML = `
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${this.alt || 'Imagen'}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body text-center">
                            <img src="${this.src}" class="img-fluid" alt="${this.alt}">
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
            
            const bootstrapModal = new bootstrap.Modal(modal);
            bootstrapModal.show();
            
            modal.addEventListener('hidden.bs.modal', function() {
                document.body.removeChild(modal);
            });
        });
    });

    // Contact form auto-fill detection
    const contactInputs = document.querySelectorAll('input[name="name"], input[name="email"], input[name="phone"]');
    contactInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value.trim() !== '') {
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
            }
        });
    });

    // Service price formatting
    const priceElements = document.querySelectorAll('.service-price');
    priceElements.forEach(element => {
        const price = parseFloat(element.textContent.replace(/[^\d.]/g, ''));
        if (!isNaN(price)) {
            element.textContent = `$${price.toLocaleString('es-MX')}`;
        }
    });

    // Mobile menu enhancement
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
        
        // Close mobile menu when clicking on a link
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navbarCollapse.classList.remove('show');
            });
        });
    }

    // Scroll to top button
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollToTopBtn.className = 'btn btn-primary position-fixed';
    scrollToTopBtn.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000; border-radius: 50%; width: 50px; height: 50px; display: none;';
    document.body.appendChild(scrollToTopBtn);

    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            scrollToTopBtn.style.display = 'block';
        } else {
            scrollToTopBtn.style.display = 'none';
        }
    });

    scrollToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Form field focus effects
    const formFields = document.querySelectorAll('.form-control');
    formFields.forEach(field => {
        field.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        field.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.parentElement.classList.remove('focused');
            }
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    console.log('PC Repair Services website loaded successfully!');
}); 