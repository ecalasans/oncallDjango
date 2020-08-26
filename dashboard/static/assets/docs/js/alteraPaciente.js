function getPaciente(url_abre, setor, nome, numero){
    valores = {
        'setor' : setor,
        'leito' : numero,
        'nome' : nome
    };

    $.ajax({
        url: url_abre,
        datatype: 'json',
        data: valores,
        type: 'post',
        success: function (response){
            console.log(response);
        },
        error: function (response){
            console.log("Nada");
        },
    });

}