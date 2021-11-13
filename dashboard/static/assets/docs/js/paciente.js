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

    $('#alt_pac_setor').change(function () {
        var setor_id = $(this).val();
        var opcoes = '';
        $('#alt_pac_leito').empty().append('<option value="0">------</option>');

        $.ajax({
            url: '/patients/list/',
            type: 'get',
            data: {'setor_id': setor_id},
            dataType: 'json',
            success: function (response) {
                $.each(response, function (chave, valor) {
                    opcoes += '<option value=' + valor.id + '>' + 'Leito ' + valor.label + '</option>';
                });
                $('#alt_pac_leito').append(opcoes);
            }
        });
    });
});

function getLeitosPaciente(setor){
    var opcoes = '';
    $('#alt_pac_leito').empty().append('<option value="0">------</option>');

    $.ajax({
        url: '/patients/list/',
        type: 'get',
        data: {'setor_id': setor},
        dataType: 'json',
        success: function (response) {
            $.each(response, function (chave, valor) {
                opcoes += '<option value=' + valor.id + '>' + 'Leito ' + valor.label + '</option>';
            });
            $('#alt_pac_leito').append(opcoes);
        }
    });
}

function getPaciente(url_abre, setor, nome, numero){
    valores = {
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
            $("#alt_id").attr('value', response.pac_id);
            $("#alt_nome").attr('value', response.pac_nome);
            $("#alt_idade").attr('value', response.pac_idade);
            $("#alt_ig").attr('value', response.pac_ig);
            $("#alt_peso_nasc").attr('value', response.pac_peso_nasc);
            $("#alt_peso_atual").attr('value', response.pac_peso_atual);
            $("#alt_pac_setor").attr('value', response.pac_setor);

            getLeitosPaciente(response.pac_setor);

            $("#alt_pac_leito").attr('value', response.pac_leito);

            $("#modalAlteraPaciente").modal('show');
        },
        error: function (response){
            console.log("Nada");
        },
    });
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

