// Form-specific JavaScript for CSMS application

document.addEventListener('DOMContentLoaded', function() {
    // Dynamic form fields
    const subjectSelect = document.getElementById('id_subject');
    const weightInput = document.getElementById('id_weight');

    if (subjectSelect && weightInput) {
        subjectSelect.addEventListener('change', function() {
            // You could add AJAX here to fetch current weight for the subject
            // and update the max value of the weight input
        });
    }

    // Toggle fields based on other fields
    const isActiveSwitches = document.querySelectorAll('.form-check-input[name="is_active"]');
    isActiveSwitches.forEach(function(switchEl) {
        switchEl.addEventListener('change', function() {
            // You could add logic here to show/hide fields based on is_active
        });
    });

    // Character counters for textareas
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(function(textarea) {
        const maxLength = textarea.getAttribute('maxlength');
        const counter = document.createElement('small');
        counter.className = 'form-text text-muted float-end';
        counter.textContent = `0/${maxLength}`;

        textarea.parentNode.insertBefore(counter, textarea.nextSibling);

        textarea.addEventListener('input', function() {
            const currentLength = textarea.value.length;
            counter.textContent = `${currentLength}/${maxLength}`;

            if (currentLength >= maxLength) {
                counter.classList.add('text-danger');
            } else {
                counter.classList.remove('text-danger');
            }
        });
    });
});