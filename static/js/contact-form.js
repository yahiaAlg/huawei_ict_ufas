document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    const submitButton = document.getElementById('submitButton');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const successMessage = document.getElementById('successMessage');
    const errorMessage = document.getElementById('errorMessage');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Clear previous messages
            successMessage.textContent = '';
            errorMessage.textContent = '';
            
            // Show loading indicator
            submitButton.disabled = true;
            loadingIndicator.classList.remove('d-none');
            
            // Get form data
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                message: document.getElementById('message').value
            };
            
            // Send AJAX request
            fetch('/contact/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                // Hide loading indicator
                loadingIndicator.classList.add('d-none');
                submitButton.disabled = false;
                
                if (data.success) {
                    // Show success message
                    successMessage.textContent = data.message;
                    // Reset form
                    contactForm.reset();
                } else {
                    // Show error message
                    errorMessage.textContent = data.message;
                }
            })
            .catch(error => {
                // Hide loading indicator
                loadingIndicator.classList.add('d-none');
                submitButton.disabled = false;
                
                // Show error message
                errorMessage.textContent = 'An error occurred while sending your message. Please try again later.';
                console.error('Error:', error);
            });
        });
    }
});