function showModalSelecionaHospital() {
    $(window).load(function () {
       $("#modal_hospitais").modal('show');
    });
}

$(document).ready(function () {
    $("#btn_seleciona_hospital").click(function () {
        $("#form_seleciona_hospital").submit();
    })
})