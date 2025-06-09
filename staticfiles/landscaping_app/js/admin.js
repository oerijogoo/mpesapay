// static/landscaping_app/js/admin.js
document.addEventListener('DOMContentLoaded', function() {
    // Preview image when selected
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', function(e) {
            const preview = this.closest('.field-image').nextElementSibling.querySelector('img');
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
                reader.readAsDataURL(this.files[0]);
            }
        });
    });
});