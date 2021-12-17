const pac_hist_ocor = document.getElementById('pac_hist_ocor');
pac_hist_ocor.style.display = 'none';

const getOcurrencies = (url_abre, id_paciente) => {
    $.ajax(
        {
            url : url_abre,
            data : { 'id_paciente' : id_paciente},
            datatype : 'json',
            type : 'post',
            success : (response) => {
                // $("#hist_nome_pac").text(response.nome_paciente);
                $.each(response.historico, (ano, meses) => {
                    console.log(meses);
                    $.each(meses, (mes, ocor) => {
                        console.log(ocor);
                    });
                });



                pac_hist_ocor.style.display = 'block';
            },
            error : (response) => {
                console.log('Não chegou lá!');
            }
        }
    );
}