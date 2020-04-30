$(document).ready(function () {
    $("#conf_email").blur(function (e) {
        if (!$("#conf_email").val()){
            alert("Confirme seu email!");
        }
    });
});