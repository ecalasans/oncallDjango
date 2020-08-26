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
                    opcoes += '<option value=' + valor.id + '>' + 'Leito ' + valor.numero + '</option>';
                });
                $('#select_pac_leito').append(opcoes);
            }
        });
    });
})

function getPaciente(url_abre, setor, nome, numero){
    /*valores = {
        'setor' : setor,
        'leito' : numero,
        'nome' : nome
    };

    $.ajax({
        url: url_abre,
        datatype: 'json',
        data: valores,
        type: 'post',
        success: function (response){
            $("#modalAlteraPaciente").modal("show");
        },
        error: function (response){
            console.log("Nada");
        },
    });*/
    $("#modalAlteraPaciente").modal("show");

}

function altaPaciente(setor, numero, url_alta) {

    $("#form_alta_paciente").append('<input type="hidden" name="setor_paciente" value="' + setor + '">');
    $("#form_alta_paciente").append('<input type="hidden" name="numero_paciente" value="' + numero + '">');

    $("#modalAltaPaciente").modal('show');

    $("#form_alta_paciente").submit(function (e) {
        /*e.preventDefault();

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
        });*/

    });
}

