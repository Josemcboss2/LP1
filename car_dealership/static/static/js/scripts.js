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
// Obtén el interruptor de modo oscuro
const darkModeToggle = document.getElementById('darkModeToggle');

// Verifica si el modo oscuro está activo en el localStorage
if (localStorage.getItem('darkMode') === 'enabled') {
    document.body.classList.add('dark-mode');
    darkModeToggle.checked = true;
}

// Escucha el cambio en el interruptor
darkModeToggle.addEventListener('change', function() {
    if (this.checked) {
        document.body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'enabled');  // Guarda la preferencia en el localStorage
    } else {
        document.body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', 'disabled');  // Guarda la preferencia en el localStorage
    }
});