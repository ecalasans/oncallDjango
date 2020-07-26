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
        success : function () {
            $("#modalOcorrencias").modal("show");
        },
        error : function () {
            alert('Não consegui abrir!')
        }
    });

}