// Initialize form select2 elements
$(document).ready(function() {
    // Enable select2 for select elements with class 'select2'
    $('.select2').select2({
        theme: 'bootstrap-5',
        width: '100%'
    });

    // Initialize date pickers
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true
    });

    // Initialize datetime pickers
    $('.datetimepicker').datetimepicker({
        format: 'yyyy-mm-dd hh:ii',
        autoclose: true,
        todayHighlight: true
    });

    // Confirm before delete actions
    $('.confirm-delete').click(function() {
        return confirm('Are you sure you want to delete this record? This action cannot be undone.');
    });

    // Dynamic form handling for paper selection based on exam
    $('#id_exam').change(function() {
        var examId = $(this).val();
        if (examId) {
            $.ajax({
                url: '/ajax/load-papers/',
                data: {
                    'exam_id': examId
                },
                success: function(data) {
                    $('#id_paper').html(data);
                }
            });
        } else {
            $('#id_paper').html('<option value="">---------</option>');
        }
    });
});