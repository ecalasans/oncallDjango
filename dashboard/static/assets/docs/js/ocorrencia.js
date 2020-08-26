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
                $("#txt_oc_diagnostico").attr('value', response.diagnostico);
                $("#txt_oc_dieta").attr('value', response.dieta);
                $("#txt_oc_acesso_venoso").attr('value', response.acesso_venoso);
                $("#txt_oc_atb").attr('value', response.antibiotico);
                $("#txt_oc_medic").attr('value', response.medicamentos);
                $("#txt_oc_vent").attr('value', response.ventilacao);
                $("#txt_oc_exames").attr('value', response.exames);

                if (response.fototerapia == "S"){
                    $('input:radio[name="rd_ocor_foto"][value="S"]').attr('checked', true);
                } else {
                    $('input:radio[name="rd_ocor_foto"][value="N"]').attr('checked', true);
                }

                $("#txt_oc_cond").attr('value', response.conduta);
                $("#txt_oc_recom").attr('value', response.recomendacoes);

                $("#modalOcorrencias").modal('show');
            }
        },
        error : function (response) {
            console.log(response.ocorrencia);
        }
    });

}
