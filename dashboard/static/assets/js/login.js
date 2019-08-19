function showModalSelecionaHospital() {
    $(window).load(function () {
       $("#modal_hospitais").modal('show');
    });
}

$("#btn_seleciona_hospital").click(function () {
    var selecao = $("#select_seleciona_hospital").val();

    console.log("selecao" + selecao);
})