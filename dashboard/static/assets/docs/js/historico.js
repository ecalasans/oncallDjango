function alertaTeste(){
    alert("Clicado");
}

const getOcurrencies = (url_abre, id_paciente) => {
    $.ajax(
        {
            url : url_abre,
            data : { 'id_paciente' : id_paciente},
            datatype : 'json',
            type : 'post',
            success : (response) => {
                console.log(response.mensagem);
            },
            error : (response) => {
                console.log('Não chegou lá!');
            }
        }
    );
}