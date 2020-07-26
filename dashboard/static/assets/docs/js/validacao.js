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
        let regex_ig = /^(([2-4][0-9])sem([0-6]d)?)$/gmi;
        var ig = $(this).val();
        let resultado = ig.match(regex_ig) || [];

        if(!resultado.length){
            alert("IG digitada fora dos padrões!  Veja o exemplo!");
            $('#ig_ig').focus();
        }
    });

    $('#id_idade').focusout(function (e) {
        let regex_idade = /^(([0-1][aA])?([1]?[0-9]?[mM])?([0-3]?[0-9]*[dD]))$|^([0-4]?[0-9]?[hH])$/gmi;
        var idade = $(this).val();
        let resultado = idade.match(regex_idade) || [];

        if(!resultado.length){
            alert("Idade digitada fora dos padrões!  Veja o exemplo!");
            $('#ig_idade').focus();
        }
    });


});