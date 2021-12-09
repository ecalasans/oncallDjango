$(document).ready(function () {
    $('#select_pac_setor').change(function () {
        var setor_id = $(this).val();
        var opcoes = '';
        $('#select_pac_leito').empty().append('<option value="0">------</option>');

        $.ajax({
            url: '/patients/list/',
            type: 'get',
            data: {'setor_id': setor_id},
            dataType: 'json',
            success: function (response) {
                $.each(response, function (chave, valor) {
                    opcoes += '<option value=' + valor.id + '>' + 'Leito ' + valor.label + '</option>';
                });
                $('#select_pac_leito').append(opcoes);
            }
        });
    });
})