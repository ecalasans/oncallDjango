const pac_hist_ocor = document.getElementById('pac_hist_ocor');
pac_hist_ocor.style.display = 'none';

const nome_meses = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'];

const toggleList = () => {
    console.log(param);
}

const getOcurrencies = (url_abre, id_paciente) => {
    $.ajax(
        {
            url : url_abre,
            data : { 'id_paciente' : id_paciente},
            datatype : 'json',
            type : 'post',
            success : (response) => {
                pac_hist_ocor.innerHTML = "";
                const anos = response.historico;
                console.log(response.historico);

                let hist_nome_pac = document.createElement('h2');
                hist_nome_pac.setAttribute('id', 'hist_nome_pac');
                hist_nome_pac.setAttribute('class', 'x_panel');
                hist_nome_pac.innerText = response.nome_paciente;
                pac_hist_ocor.appendChild(hist_nome_pac);

                for (const ano in anos) {
                    let ano_container = document.createElement('div');
                    ano_container.setAttribute('class', 'x_panel');
                    ano_container.setAttribute('id', 'ano' + ano + '_container');
                    pac_hist_ocor.appendChild(ano_container);

                    let ano_title = document.createElement('div');
                    ano_title.setAttribute('id', 'ano' + ano + '_title');
                    ano_title.setAttribute('class', 'x_title');
                    ano_container.appendChild(ano_title);

                    let ano_title_h2 = document.createElement('h2');
                    ano_title_h2.setAttribute('id', 'ano' + ano + '_h2');
                    ano_title_h2.innerText = ano;
                    ano_title.appendChild(ano_title_h2);

                    let ano_title_ul = document.createElement('ul');
                    ano_title_ul.setAttribute('id', 'ano' + ano + '_ul');
                    ano_title_ul.setAttribute('class', 'nav navbar-right panel_toolbox');
                    ano_title.appendChild(ano_title_ul);

                    let ano_title_li = document.createElement('li');
                    ano_title_li.setAttribute('id', 'ano' + ano + '_li');
                    const param = ano + "seta";
                    ano_title_li.innerHTML = '<a class="collapse-link"><i class="fa fa-chevron-up" id="' + param + '">';
                    ano_title_li.innerHTML += '</i></a>'
                    ano_title_ul.appendChild(ano_title_li);


                    let div_clearfix = document.createElement('div');
                    div_clearfix.setAttribute('class', 'clearfix');
                    ano_title.appendChild(div_clearfix);

                    let meses_container = document.createElement('div');
                    meses_container.setAttribute('id', 'ano' + ano + '_meses');
                    meses_container.setAttribute('class', 'x_content');
                    ano_container.appendChild(meses_container);

                    const ano_seta = document.getElementById(param);
                    ano_seta.addEventListener("click", () => {
                        let classe = ano_seta.getAttribute('class');

                        if (classe == 'fa fa-chevron-up'){
                            ano_seta.className = 'fa fa-chevron-down';
                            meses_container.style.display = 'none';
                        } else {
                            ano_seta.className = 'fa fa-chevron-up';
                            meses_container.style.display = 'block';
                        }
                    });

                    const meses = anos[ano];

                    for (const mes in meses) {
                        let div_accordion = document.createElement('div');
                        div_accordion.setAttribute('id', 'accordion');
                        div_accordion.setAttribute('class', 'accordion');
                        div_accordion.setAttribute('role', 'tablist');
                        meses_container.appendChild(div_accordion);

                        let mes_div = document.createElement('div');
                        mes_div.setAttribute('class', 'panel');
                        div_accordion.appendChild(mes_div);

                        let mes_title = document.createElement('h2');
                        mes_title.setAttribute('id', nome_meses[mes-1] + '_' + ano);
                        const param_mes = ano + mes + "seta";
                        mes_title.innerHTML = '<a href="#"><i class="fa fa-chevron-down" id="' + param_mes + '">' +
                            "  " + nome_meses[mes-1] + '</i></a>'
                        mes_div.appendChild(mes_title);

                        let dashboad_widget_content = document.createElement('div');
                        dashboad_widget_content.setAttribute('class', 'dashboard-widget-content');
                        mes_div.appendChild(dashboad_widget_content);

                        let ul_widget_list = document.createElement('ul');
                        ul_widget_list.setAttribute('class', 'list-unstyled timeline widget');
                        dashboad_widget_content.appendChild(ul_widget_list);

                        const mes_seta = document.getElementById(param_mes);
                        mes_seta.addEventListener('click', () => {
                            let classe = mes_seta.getAttribute('class');

                            if (classe == 'fa fa-chevron-down') {
                                mes_seta.className = 'fa fa-chevron-right';
                                dashboad_widget_content.style.display = 'none';
                            } else {
                                mes_seta.className = 'fa fa-chevron-down';
                                dashboad_widget_content.style.display = 'block';
                            }
                        });

                        const dias = meses[mes];

                        for (const diasKey in dias) {
                            const ocor_info = dias[diasKey];

                            let li_widget_list = document.createElement('li');
                            ul_widget_list.appendChild(li_widget_list);

                            let div_block = document.createElement('div')
                            div_block.setAttribute('class', 'block');
                            li_widget_list.appendChild(div_block);

                            let div_block_content = document.createElement('div')
                            div_block_content.setAttribute('class', 'block-content');
                            div_block.appendChild(div_block_content);

                            let h2_data = document.createElement('h2');
                            h2_data.setAttribute('id', 'ocor_' + ocor_info.id);
                            h2_data.setAttribute('class', 'title');
                            let data_add = new Date(ocor_info.data_add);
                            h2_data.innerHTML = '<a href="#">' + data_add.toLocaleString('pt-BR') + '</a>';
                            div_block_content.appendChild(h2_data);

                            h2_data.addEventListener('click', () => {
                                Ocurrency('occurrency', ocor_info.id);
                            });

                            let div_byline = document.createElement('div');
                            div_byline.setAttribute('class', 'byline');
                            div_byline.innerText = 'por ' + ocor_info.med__first_name + ' ' + ocor_info.med__last_name;
                            div_block_content.appendChild(div_byline);
                        }

                    }
                }

                pac_hist_ocor.style.display = 'block';

            },
            error : (response) => {
                alert('Sem conexão com o servidor.\nTente mais tarde!');
            }
        }
    );
}

const Ocurrency = (url_abre, id_ocorr) => {
    $.ajax(
        {
            url: url_abre,
            datatype: 'json',
            data: {'id_ocorr': id_ocorr},
            type: 'post',
            success: (response) => {
                $("#nomePacOcorr").text(response.ocorrencia.pac__nome + '\n');

                const data_ocorr = new Date(response.ocorrencia.data_add);
                $("#dataOcorr").text(data_ocorr.toLocaleString('pt-BR') +' por ' +
                response.ocorrencia.med__first_name + ' ' + response.ocorrencia.med__last_name);

                $("#idadePacOcorr").html(
                    "<span class=\"font-weight-bold\">Idade:  </span>" + response.ocorrencia.pac__idade
                );

                $("#pesoNascPacOcorr").html(
                    "<span class=\"font-weight-bold\">Peso Nasc.:  </span>" + response.ocorrencia.pac__peso_nasc + "<span>g</span>"
                );

                $("#pesoAtualPacOcorr").html(
                    "<span class=\"font-weight-bold\">Peso Nasc.:  </span>" + response.ocorrencia.pac__peso_atual + "<span>g</span>"
                );

                $("#modalOcorrPaciente").modal('show');
            },
            error: (error) => {
                alert('Falha de conexão');
            }
        }
    );
}