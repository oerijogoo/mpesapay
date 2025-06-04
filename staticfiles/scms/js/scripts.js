// Menu Toggle
$(document).ready(function() {
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // Auto-calculate end date based on start date and duration
    $('.duration-field').on('change', function() {
        const startDate = new Date($('#id_start_date').val());
        if (!isNaN(startDate.getTime())) {
            const duration = parseInt($(this).val());
            if (!isNaN(duration)) {
                const endDate = new Date(startDate);
                endDate.setFullYear(endDate.getFullYear() + duration);
                $('#id_end_date').val(endDate.toISOString().split('T')[0]);
            }
        }
    });

    // Form validation
    $('.needs-validation').on('submit', function(e) {
        if (this.checkValidity() === false) {
            e.preventDefault();
            e.stopPropagation();
        }
        $(this).addClass('was-validated');
    });

    // Dynamic grade selection based on marks
    $(document).on('change', '#id_marks', function() {
        const marks = parseFloat($(this).val());
        if (!isNaN(marks)) {
            $('#id_grade option').each(function() {
                const min = parseFloat($(this).data('min'));
                const max = parseFloat($(this).data('max'));
                if (marks >= min && marks <= max) {
                    $('#id_grade').val($(this).val()).trigger('change');
                    return false; // break the loop
                }
            });
        }
    });

    // Institution type change handler
    $('#id_institution_type').on('change', function() {
        const institutionTypeId = $(this).val();
        if (institutionTypeId) {
            // Update academic levels dropdown
            $.get(`/scms/api/academic-levels/?institution_type=${institutionTypeId}`, function(data) {
                const $academicLevel = $('#id_academic_level');
                $academicLevel.empty();
                $academicLevel.append('<option value="">---------</option>');
                data.forEach(function(level) {
                    $academicLevel.append(`<option value="${level.id}">${level.name}</option>`);
                });
            });

            // Update years of study dropdown
            $.get(`/scms/api/years-of-study/?institution_type=${institutionTypeId}`, function(data) {
                const $yearOfStudy = $('#id_year_of_study');
                $yearOfStudy.empty();
                $yearOfStudy.append('<option value="">---------</option>');
                data.forEach(function(year) {
                    $yearOfStudy.append(`<option value="${year.id}">${year.name}</option>`);
                });
            });
        }
    });

    // Course change handler
    $('#id_course').on('change', function() {
        const courseId = $(this).val();
        if (courseId) {
            // Update papers multi-select
            $.get(`/scms/api/course-papers/${courseId}/`, function(data) {
                const $papers = $('#id_papers');
                $papers.empty();
                data.forEach(function(paper) {
                    $papers.append(`<option value="${paper.id}">${paper.name}</option>`);
                });
            });
        }
    });

    // Print report button
    $('.print-report').on('click', function() {
        window.print();
    });

    // Export to PDF button
    $('.export-pdf').on('click', function() {
        const studentId = $(this).data('student-id');
        window.location.href = `/scms/students/${studentId}/report/pdf/`;
    });
});

// Datepicker initialization
$(function () {
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true
    });
});

// AJAX CSRF setup
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});