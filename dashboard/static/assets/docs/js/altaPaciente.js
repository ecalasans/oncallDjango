function altaPaciente(setor, numero, url_alta) {

    $("#form_alta_paciente").append('<input type="hidden" name="setor_paciente" value="' + setor + '">');
    $("#form_alta_paciente").append('<input type="hidden" name="numero_paciente" value="' + numero + '">');

    $("#modalAltaPaciente").modal('show');

    $("#form_alta_paciente").submit(function (e) {
        e.preventDefault();

        $.ajax({
            url: url_alta,
            type: 'get',
            data: {'setor_paciente': setor,
                    'numero_leito': numero,
                    'status': $("input[name='rd_status_alta']:checked").val(),
            },
            success: function () {
                window.location.reload();
            },
            error: function () {
                alert('Erro no servidor!');
            }
        });

    });
}