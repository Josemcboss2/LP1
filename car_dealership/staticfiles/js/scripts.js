// Welcome alert
function showWelcomeAlert() {
    Swal.fire({
        title: '¡Bienvenido a Auto Elite!',
        text: 'Estamos aquí para ayudarte a encontrar el vehículo de tus sueños.',
        icon: 'info',
        confirmButtonText: 'Gracias'
    });
}

// Car inquiry modal
function inquireAboutCar(carId, carName) {
    // Set the car name in the modal
    document.getElementById('inquiryCarName').innerText = carName;
    document.getElementById('carIdInput').value = carId;
    
    // Show the modal
    var inquiryModal = new bootstrap.Modal(document.getElementById('inquiryModal'));
    inquiryModal.show();
}

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            let valid = true;
            const requiredFields = contactForm.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            // Email validation
            const emailField = contactForm.querySelector('[type="email"]');
            if (emailField && emailField.value) {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(emailField.value)) {
                    valid = false;
                    emailField.classList.add('is-invalid');
                }
            }
            
            if (!valid) {
                event.preventDefault();
                alert('Por favor, completa todos los campos requeridos correctamente.');
            }
        });
    }
});

// Hover effects for navigation items
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.color = '#dc3545';
            this.style.transform = 'scale(1.05)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.color = '';
            this.style.transform = 'scale(1)';
        });
    });
});

// Animaciones al hacer scroll
document.addEventListener('DOMContentLoaded', function() {
    // Agregar clase animate-on-scroll a elementos que queremos animar
    const elements = [
        '.card',
        '.article-content',
        '.comment',
        '.sidebar-widget',
        '.recent-article',
        '.category-item',
        'h1, h2, h3',
        '.btn-primary',
        '.form-control'
    ];

    elements.forEach((selector, index) => {
        document.querySelectorAll(selector).forEach(element => {
            element.classList.add('animate-on-scroll');
            // Agregar retardos diferentes para crear un efecto cascada
            element.style.transitionDelay = `${index * 0.1}s`;
        });
    });

    // Función para verificar si un elemento está en el viewport
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.8 &&
            rect.bottom >= 0
        );
    }

    // Función para animar elementos cuando son visibles
    function animateOnScroll() {
        document.querySelectorAll('.animate-on-scroll').forEach(element => {
            if (isElementInViewport(element)) {
                element.classList.add('visible');
            }
        });
    }

    // Ejecutar animación al cargar y al hacer scroll
    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll, { passive: true });
    window.addEventListener('resize', animateOnScroll, { passive: true });
});