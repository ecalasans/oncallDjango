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
                console.log(response.ocorrencia);
            }
        },
        error : function (response) {
            console.log(response.ocorrencia);
        }
    });

}