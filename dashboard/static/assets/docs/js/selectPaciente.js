$(document).ready(function () {
    $('#select_pac_setor').change(function () {
        var setor_id = $(this).val();

        $.ajax({
            url: '/patients/list/',
            type: 'get',
            data: {'setor_id': setor_id},
            dataType: 'json',
            success: function (response) {
                console.log(response);
            }
        });
    });
})