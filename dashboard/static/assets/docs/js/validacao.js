$(document).ready(function () {
    /*$("#conf_email").blur(function (e) {
        if (!$("#conf_email").val()){
            alert("Confirme seu email!");
            $("#conf_email").focus();
        }
    });*/

    $("#conf_pass").blur(function (e) {
        if (!$("#conf_pass").val()){
            alert("Confirme a senha!");
        }
    });
});