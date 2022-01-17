function abreOcorrencia(url_abre, setor, nome, numero) {
    valores = {
        'setor' : setor,
        'leito' : numero,
        'nome' : nome
    };

    $.ajax({
        url : url_abre,
        datatype : 'json',
        data : valores,
        type : 'post',
        success : function (response) {
            if (response.ocorrencia == ''){
                $('#modalOcorrencias').modal('show');
            } else {
                $("#txt_oc_diagnostico").text(response.diagnostico);
                $("#txt_oc_dieta").text(response.dieta);
                $("#txt_oc_acesso_venoso").text(response.acesso_venoso);
                $("#txt_oc_atb").text(response.antibiotico);
                $("#txt_oc_medic").text(response.medicamentos);
                $("#txt_oc_vent").text(response.ventilacao);
                $("#txt_oc_exames").text(response.exames);

                if (response.fototerapia == "S"){
                    $('input:radio[name="rd_ocor_foto"][value="S"]').attr('checked', true);
                } else {
                    $('input:radio[name="rd_ocor_foto"][value="N"]').attr('checked', true);
                }

                if (response.vacina == "S"){
                    $('input:radio[name="rd_ocor_vacina"][value="S"]').attr('checked', true);
                } else {
                    $('input:radio[name="rd_ocor_vacina"][value="N"]').attr('checked', true);
                }

                if (response.fono == "S"){
                    $('input:radio[name="rd_ocor_fono"][value="S"]').attr('checked', true);
                } else {
                    $('input:radio[name="rd_ocor_fono"][value="N"]').attr('checked', true);
                }

                $("#txt_oc_cond").text(response.conduta);
                $("#txt_oc_recom").text(response.recomendacoes);

                $("#modalOcorrencias").modal('show');
            }
        },
        error : function (response) {
            console.log(response.ocorrencia);
        }
    });

}
