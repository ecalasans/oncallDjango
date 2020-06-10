$(document).ready(function () {
    $("#conf_pass").blur(function (e) {
        if (!$("#conf_pass").val()){
            alert("Confirme a senha!");
        }
    });

    //Validação do formulário de pacientes
    $('#id_nome').focusout(function (e) {
        if(!$(this).val()){
            alert('Nome vazio! Este dado é obrigatório!');
        }
    });

});