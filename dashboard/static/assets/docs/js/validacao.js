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

    $('#id_ig').focusout(function (e) {
        let regex_ig = /(^([2-4][1-9]sem)$)|(^([2-4][1-9]sem[0-6]d)$)/gmi;
        var ig = $(this).val();
        let resultado = ig.match(regex_ig) || [];

        if(!resultado.length){
            alert("Dado fora dos padrões!  Veja o exemplo!");
            $('#ig_ig').focus();
        }
    });


});