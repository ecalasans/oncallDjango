from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from dashboard.models import Leito, Hospital, Setor, Medico, Paciente, Ocorrencia
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import MedicoForm, PacienteForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt # Usado para evitar checar csfr_token
import datetime

'''
class LoginView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts/login/'
    template_name = 'registration/login.html'
    extra_context = {
        'next': '/',
    }

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        user_id = self.request.user.id

        hospitais_id = Medico.objects.filter(id=user_id).values('hospitais')

        hospitais_nomes = {}

        for h in hospitais_id.all():
            hospitais_nomes[h['hospitais']] = Hospital.objects.get(id=h['hospitais']).nome

        context['hospitais_nomes'] = hospitais_nomes
        context['usuario'] = Medico.objects.get(id=user_id).first_name

        return context


#Classe de logout
class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

class MainView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)

        hosp_recebido = self.request.POST.get('select_seleciona_hospital')

        hosp = Hospital.objects.get(sigla='HJPB')

        setores = Setor.objects.filter(hospital_id=hosp)

        leitos = {}

        for setor in setores:
            leitos[setor] = Leito.objects.filter(hospital_id=hosp, setor_id=setor.id).values('status')\
                .annotate(Count('setor'))

        context = {
            'setores': setores,
            'leitos': leitos,
        }

        return context


#Médicos
#Criação
class CreateUser(CreateView):
    template_name = 'dashboard/medicos/medicos.html'
    form_class = UsuarioForm
    success_url = 'medicos/'

    def get_context_data(self, **kwargs):
        context = super(CreateUser, self).get_context_data(**kwargs)

        hospitais = Hospital.objects.all().order_by('id')

        form_usuario = UsuarioForm()

        context['form'] = form_usuario
        context['hospitais'] = hospitais

        return context

class ModalView(TemplateView):
    template_name = 'dashboard/medicos/modal.html'


'''

########################################################################################################################
#   Seção HOME
########################################################################################################################
@login_required
def home(request):
    # Pega variáveis de sessão
    hosp_id = request.session.get('hosp_id')
    hosp_sigla = request.session.get('hosp_sigla')
    primeiro = request.session.get('primeiro')
    saudacao = request.session.get('saudacao')

    dia_anterior = datetime.date.today() - datetime.timedelta(days=1)

    # Seleção de setores do hospital do usuário
    setores = Setor.objects.filter(hospital_id=hosp_id).values('setor', 'pk', 'ativo')
    total_setores = Setor.objects.filter(hospital_id=hosp_id, ativo=True).count

    # Total de leitos do hospital do usuário
    total_leitos = Leito.objects.filter(hospital_id=hosp_id).count()

    # Situação dos leitos por setor(Ativos e Inativos)
    situacao_por_setor = {}
    ocorrencias = {}
    for setor in setores:
        if not setor['ativo']:
            pass
        else:
            situacao = {}
            # Lista os leitos do setor
            leitos_setor = Leito.objects.filter(hospital_id=hosp_id, setor=setor['pk'])

            lista_ocorr = []

            # Pesquisa os leitos do setor:  se estiver ocupado pega o paciente;  se não, registra como vago
            for leito in leitos_setor:
                if leito.status == 'O':
                    paciente_do_leito = Paciente.objects.get(leito_id=leito.id, status='I')
                    ocor_paciente = Ocorrencia.objects.filter(pac_id=paciente_do_leito.id).last()

                    if not ocor_paciente:
                        pac_ocorr = {'situacao': 'Não há ocorrência registrada no banco de dados!'}
                    else:
                        medico_responsavel = "{} {}".format(Medico.objects.get(pk=ocor_paciente.med_id).first_name,
                                                            Medico.objects.get(pk=ocor_paciente.med_id).last_name)

                        pac_ocorr = {
                            'situacao': 'OCUPADO',
                            'num_leito': paciente_do_leito.leito.numero,
                            'nome_pac' : paciente_do_leito.nome,
                            'diagnostico': ocor_paciente.diagnostico,
                            'dieta': ocor_paciente.dieta,
                            'acesso_venoso': ocor_paciente.acesso_venoso,
                            'antibiotico': ocor_paciente.antibiotico,
                            'medicamentos': ocor_paciente.medicamentos,
                            'ventilacao': ocor_paciente.ventilacao,
                            'fototerapia': ocor_paciente.fototerapia,
                            'exames': ocor_paciente.exames,
                            'conduta': ocor_paciente.conduta,
                            'medico': medico_responsavel
                        }
                elif leito.status == 'B':
                    pac_ocorr = {'situacao': 'BLOQUEADO'}
                elif leito.status == 'L':
                    pac_ocorr = {'situacao': 'VAGO'}

                lista_ocorr.append({str(leito.numero): pac_ocorr})

            ocorrencias[str(setor['setor'])] = lista_ocorr
            leitos_ativos = Leito.objects.filter(hospital_id=hosp_id, setor=setor['pk'], situacao='A') \
                .values('status').annotate(Count('status'))
            ativos_setor = Leito.objects.filter(hospital_id=hosp_id, setor=setor['pk'], situacao='A')
            ativos_setor = ativos_setor.count()
            ocupacao = Leito.objects.filter(hospital_id=hosp_id, setor=setor['pk'], status='O').count()
            inativos_setor = Leito.objects.filter(hospital_id=hosp_id, setor=setor['pk'], situacao='D').count()

            for qset in leitos_ativos.values('status', 'status__count'):
                situacao[qset['status']] = qset['status__count']
                p = int((ocupacao/ ativos_setor) * 100)
                situacao['porcentagem'] = p
            situacao['ativos'] = ativos_setor
            situacao['inativos'] = inativos_setor

            situacao_por_setor[setor['setor']] = situacao

    return render(request, 'dashboard/index.html',
                  context={'usuario': request.user.username,
                           'primeiro': primeiro,
                           'saudacao': saudacao,
                           'hosp_sigla': hosp_sigla,
                           'total_leitos': total_leitos,
                           'setores': setores,
                           'total_setores': total_setores,
                           'situacao_por_setor': situacao_por_setor})

########################################################################################################################
#   Seção LOGIN
########################################################################################################################

def sysLogin(request):
    hospitais = Hospital.objects.all().order_by('nome')

    if request.method == 'GET':
        return render(request, 'dashboard/registration/login.html',
                      context={'form': AuthenticationForm(),
                               'hospitais': hospitais})
    if request.method == 'POST':
        # Autentica usuário com base nos dados recebidos
        user = authenticate(request, username=request.POST['user_login'], password=request.POST['pass_login'])

        #Verifica se o usuário existe
        if user is not None:
            # Faz o login
            login(request, user)
            hosp_id = Medico.objects.get(hospital_id=request.POST['select_hosp_cad']).hospital_id
            hosp_sigla = Hospital.objects.get(id=hosp_id).sigla

            primeiro = request.user.first_name

            agora = datetime.datetime.now()
            data = agora.strftime("%d/%m%Y")
            saudacao = ''

            if (agora.hour >= 0) and (agora.hour < 12):
                saudacao = "Bom dia,"

            if (agora.hour >= 12) and (agora.hour < 18):
                saudacao = "Boa tarde,"

            if (agora.hour >= 18):
                saudacao = "Boa noite,"

            request.session['hosp_id'] = hosp_id
            request.session['hosp_sigla'] = hosp_sigla
            request.session['primeiro'] = primeiro
            request.session['saudacao'] = saudacao

            return redirect('home')
        else:
            return render(request, 'dashboard/registration/login.html',
                          context={'form': AuthenticationForm(),
                                   'hospitais': hospitais,
                                   'error': 'Usuário não encontrado ou dados conflitantes!'})

def sysLogout(request):
    logout(request)
    return redirect('login')

########################################################################################################################
#   Seção CADASTRO DE USUÁRIO
########################################################################################################################

def signupUser(request):
    hospitais = Hospital.objects.all().order_by('nome')

    if request.method == 'GET':
        return render(request, 'dashboard/registration/signup.html',
                      context={'form': MedicoForm(),
                               'hospitais': hospitais})
    if request.method == 'POST':
        form = MedicoForm(request.POST)

        if form.is_valid():
            new_medico = form.save(commit=False)

            new_medico.set_password(form.cleaned_data['password'])
            new_medico.save()

            sucesso = "Seu cadastro foi enviado com sucesso!\nProcure o administrador para liberação do login!"
            messages.success(request, sucesso)

            return render(request, 'dashboard/registration/signup.html',
                          context={'form':form,
                                   'hospitais': hospitais})
        else:
            erros = []
            for erro in form.errors:
                frase = "{} - {}".format(erro, form.errors[erro])
                erros.append(frase)
            return render(request, 'dashboard/registration/signup.html',
                          context={'form': form,
                                   'hospitais': hospitais,
                                   'errors': erros})


########################################################################################################################
#   Seção LEITOS
########################################################################################################################
def refreshBeds(request):
    # Pega variáveis de sessão
    hosp_id = request.session.get('hosp_id')
    hosp_sigla = request.session.get('hosp_sigla')
    primeiro = request.session.get('primeiro')
    saudacao = request.session.get('saudacao')

    situacao = {'Ativo': 'A', 'Desativado': 'D'}
    status = {'Livre': 'L', 'Ocupado': 'O', 'Bloqueado': 'B'}

    hosp_id = request.session.get('hosp_id')

    # Pega leitos do hospital
    setores = Setor.objects.filter(hospital_id=hosp_id, ativo=True).values('id', 'setor')

    leitos = {}

    for valores in setores.values('id', 'setor'):
        leitos_setor = {}

        lpesq = Leito.objects.filter(hospital_id=hosp_id, setor=valores['id']) \
            .values('numero', 'situacao', 'status')

        for valor in lpesq.values('numero', 'situacao', 'status'):
            leitos_setor[valor['numero']] = {'situacao': valor['situacao'], 'status': valor['status']}

            leitos[valores['setor']] = leitos_setor

    return [primeiro, saudacao, hosp_sigla, leitos, situacao, status]


def bedsMmanager(request):
    # # Pega variáveis de sessão
    # hosp_id = request.session.get('hosp_id')
    # hosp_sigla = request.session.get('hosp_sigla')
    # primeiro = request.session.get('primeiro')
    # saudacao = request.session.get('saudacao')
    #
    # situacao = {'Ativo': 'A', 'Desativado': 'D'}
    # status = {'Livre': 'L', 'Ocupado': 'O', 'Bloqueado': 'B'}
    #
    # hosp_id = request.session.get('hosp_id')
    #
    # # Pega leitos do hospital
    # setores = Setor.objects.filter(hospital_id=hosp_id, ativo=True).values('id', 'setor')
    #
    # leitos = {}
    #
    # for valores in setores.values('id', 'setor'):
    #     leitos_setor = {}
    #
    #     lpesq = Leito.objects.filter(hospital_id=hosp_id, setor=valores['id']) \
    #         .values('numero', 'situacao', 'status')
    #
    #     for valor in lpesq.values('numero', 'situacao', 'status'):
    #         leitos_setor[valor['numero']] = {'situacao': valor['situacao'], 'status': valor['status']}
    #
    #         leitos[valores['setor']] = leitos_setor

    if request.method == 'GET':
        primeiro, saudacao, hosp_sigla, leitos, situacao, status = refreshBeds(request)

        return render(request, 'dashboard/beds/beds.html',
                      context={
                          'usuario': request.user.username,
                          'primeiro': primeiro,
                          'saudacao': saudacao,
                          'hosp_sigla': hosp_sigla,
                          'leitos': leitos,
                          'situacao': situacao,
                          'status': status
                      })

    if request.method == 'POST':
        hosp_id = request.session.get('hosp_id')

        recebidos = request.POST

        s = Setor.objects.get(setor=recebidos['hidden_set'], hospital_id=hosp_id).id

        leito_alterar = Leito.objects.get(numero=recebidos['num_leito'], setor_id=s)

        if 'sit_rd' not in request.POST:
            leito_alterar.situacao = recebidos['hidden_sit']
        else:
            leito_alterar.situacao = recebidos['sit_rd']

        leito_alterar.status = recebidos['select_status']

        leito_alterar.save()

        primeiro, saudacao, hosp_sigla, leitos, situacao, status = refreshBeds(request)

        return render(request, 'dashboard/beds/beds.html',
                      context={
                          'usuario': request.user.username,
                          'primeiro': primeiro,
                          'saudacao': saudacao,
                          'hosp_sigla': hosp_sigla,
                          'leitos': leitos,
                          'situacao': situacao,
                          'status': status
                      })

########################################################################################################################
#   Seção PACIENTES
########################################################################################################################
def refreshPatients(request):
    # Pega variáveis de sessão
    hosp_id = request.session.get('hosp_id')
    hosp_sigla = request.session.get('hosp_sigla')
    primeiro = request.session.get('primeiro')
    saudacao = request.session.get('saudacao')

    # Pega setores do hospital
    setores_qs = {str(s['id']): s['setor'] for s in
                  Setor.objects.filter(hospital_id=hosp_id, ativo=True).values('id', 'setor')}

    pacientes = {}

    for id, setor in setores_qs.items():
        p = {}
        leitos_queryset = Leito.objects.filter(hospital_id=hosp_id, setor_id=id).order_by('numero')

        for leito in leitos_queryset:
            if leito.status == 'L':
                p[str(leito.numero)] = 'VAGO'
            elif leito.status == 'B':
                p[str(leito.numero)] = 'BLOQUEADO'
            else:
                if Paciente.objects.filter(leito__numero=leito.numero, status="I").exists():
                    p[str(leito.numero)] = Paciente.objects.get(leito_id=leito.id, status="I").nome
                else:
                    leito.status = 'L'
                    leito.save()
                    p[str(leito.numero)] = 'VAGO'
                    #p[str(leito.numero)] = 'INDEFINIDO'
        pacientes[setor] = p

    return [primeiro, saudacao, hosp_sigla, pacientes, setores_qs]


def patientsManager(request):
    # # Pega variáveis de sessão
    # hosp_id = request.session.get('hosp_id')
    # hosp_sigla = request.session.get('hosp_sigla')
    # primeiro = request.session.get('primeiro')
    # saudacao = request.session.get('saudacao')
    #
    # # Pega setores do hospital
    # setores_qs = {str(s['id']): s['setor'] for s in
    #                     Setor.objects.filter(hospital_id=hosp_id, ativo=True).values('id', 'setor')}
    #
    # pacientes = {}
    #
    # for id, setor in setores_qs.items():
    #     p = {}
    #     leitos_queryset = Leito.objects.filter(hospital_id=hosp_id, setor_id=id).order_by('numero')
    #
    #     for leito in leitos_queryset:
    #         if leito.status == 'L':
    #             p[str(leito.numero)] = 'VAGO'
    #         elif leito.status == 'B':
    #             p[str(leito.numero)] = 'BLOQUEADO'
    #         else:
    #             if Paciente.objects.filter(leito__numero=leito.numero).exists():
    #                 p[str(leito.numero)] = Paciente.objects.get(leito_id=leito.id).nome
    #             else:
    #                 p[str(leito.numero)] = 'INDEFINIDO'
    #     pacientes[setor] = p

    if request.method == 'GET':
        primeiro, saudacao, hosp_sigla, pacientes, setores_qs = refreshPatients(request)
        return render(request, 'dashboard/patients/patients.html',
                      context={
                          'usuario': request.user.username,
                          'primeiro': primeiro,
                          'saudacao': saudacao,
                          'hosp_sigla': hosp_sigla,
                          'pacientes': pacientes,
                          'setores': setores_qs,
                          'pac_form': PacienteForm(),
                      })

    if request.method == 'POST':
        form = PacienteForm(request.POST)
        form.status = "I"
        form.data_modif = datetime.datetime.now()
        form.log_med = request.user.id

        form.save(commit=False)

        if form.is_valid():
            new_patient = form.save(commit=False)

            leito_paciente = Leito.objects.get(id=request.POST.get('leito'))
            leito_paciente.status = 'O'
            leito_paciente.save()

            new_patient.peso_nasc = int(form.cleaned_data['peso_nasc'])
            new_patient.peso_atual = int(form.cleaned_data['peso_atual'])
            new_patient.log_med = Medico.objects.get(id=request.user.id)
            new_patient.status = "I"
            new_patient.tcle = 'chk_pac_tcle' in request.POST

            new_patient.save()

            primeiro, saudacao, hosp_sigla, pacientes, setores_qs = refreshPatients(request)

            return render(request, 'dashboard/patients/patients.html',
                          context={
                              'usuario': request.user.username,
                              'primeiro': primeiro,
                              'saudacao': saudacao,
                              'hosp_sigla': hosp_sigla,
                              'pacientes': pacientes,
                              'setores': setores_qs,
                              'pac_form': PacienteForm(),
                          })
        else:
            primeiro, saudacao, hosp_sigla, pacientes, setores_qs = refreshPatients(request)
            return render(request, 'dashboard/patients/patients.html',
                          context={
                              'usuario': request.user.username,
                              'primeiro': primeiro,
                              'saudacao': saudacao,
                              'hosp_sigla': hosp_sigla,
                              'pacientes': pacientes,
                              'setores': setores_qs,
                              'pac_form': PacienteForm(),
                          })

def patientsList(request):
    hosp_id = request.session.get('hosp_id')

    setor_id = request.GET.get('setor_id')

    leitos_setor = Leito.objects.filter(hospital_id=hosp_id, setor_id=setor_id, situacao='A', status='L')\
        .values('id', 'numero').order_by('numero')

    lista_leitos = [l for l in leitos_setor]

    return JsonResponse(lista_leitos, safe=False)

def patientsDischarge(request):
    status = request.POST.get('rd_status_alta')
    setor_paciente = Setor.objects.get(setor=request.POST.get('setor_paciente')).id
    numero_leito = Leito.objects.get(numero=request.POST.get('numero_paciente'), setor_id=setor_paciente)

    paciente_para_alta = Paciente.objects.get(leito_id=numero_leito.id, status="I")
    paciente_para_alta.status = status
    numero_leito.status = 'L'
    paciente_para_alta.save()
    numero_leito.save()

    primeiro, saudacao, hosp_sigla, pacientes, setores_qs = refreshPatients(request)

    return render(request, 'dashboard/patients/patients.html',
                  context={
                      'usuario': request.user.username,
                      'primeiro': primeiro,
                      'saudacao': saudacao,
                      'hosp_sigla': hosp_sigla,
                      'pacientes': pacientes,
                      'setores': setores_qs,
                      'pac_form': PacienteForm(),
                  })

@csrf_exempt
def patientsOpenOccurrence(request):
    # Recebe os dados de abreOcorrencia
    dados_recebidos = request.POST

    # Pesquisa no banco de dados as pk's correspondentes às variáveis recebidas:
    setor_id = Setor.objects.get(setor=dados_recebidos['setor']).id
    leito_id = Leito.objects.get(numero=dados_recebidos['leito'], setor_id=setor_id, status='O').id
    paciente_id = Paciente.objects.get(nome=dados_recebidos['nome'], leito_id=leito_id).id

    # Registra numa variável de sessão para ser usada em patientsRecord
    request.session['setor'] = setor_id
    request.session['leito'] = leito_id
    request.session['paciente'] = paciente_id

    if (paciente_id):
        # Pesquisa ocorrência para o paciente e retorna a última ocorrência pra ele ou um json em branco
        ocorrencia = Ocorrencia.objects.filter(pac_id=paciente_id).last()
        if (ocorrencia):
            resposta = {
                'diagnostico': ocorrencia.diagnostico,
                'dieta': ocorrencia.dieta,
                'acesso_venoso': ocorrencia.acesso_venoso,
                'antibiotico': ocorrencia.antibiotico,
                'medicamentos': ocorrencia.medicamentos,
                'ventilacao': ocorrencia.ventilacao,
                'fototerapia': ocorrencia.fototerapia,
                'exames': ocorrencia.exames,
                'conduta': ocorrencia.conduta
            }
            return JsonResponse(resposta, safe=False)
        else:
            return JsonResponse({'ocorrencia': ''}, safe=False)
    else:
        return JsonResponse({'ocorrencia': 'Paciente não encontrado!'})


def patientsRecord(request):
    # Pesquisa campos necessários para o registro da ocorrência
    medico = Medico.objects.get(hospital=request.session.get('hosp_id'), username=request.user.username)
    paciente = Paciente.objects.get(pk=request.session.get('paciente'))

    # Recebe os dados vindos do formulário de ocorrencias
    ocorr_form = request.POST

    # Se tiver dados cria o objeto formulário e salva os campos
    if (ocorr_form):
        form_oc = Ocorrencia()

        form_oc.diagnostico = request.POST.get("txt_oc_diagnostico")
        form_oc.dieta = request.POST.get("txt_oc_dieta")
        form_oc.acesso_venoso = request.POST.get("txt_oc_acesso_venoso")
        form_oc.antibiotico = request.POST.get("txt_oc_atb")
        form_oc.medicamentos = request.POST.get("txt_oc_medic")
        form_oc.ventilacao = request.POST.get("txt_oc_vent")
        form_oc.fototerapia = request.POST.get("rd_ocor_foto")
        form_oc.exames = request.POST.get("txt_oc_exames")
        form_oc.conduta = request.POST.get("txt_oc_cond")
        form_oc.med = medico
        form_oc.pac = paciente

        form_oc.save()

    primeiro, saudacao, hosp_sigla, pacientes, setores_qs = refreshPatients(request)
    return render(request, 'dashboard/patients/patients.html',
                  context={
                      'usuario': request.user.username,
                      'primeiro': primeiro,
                      'saudacao': saudacao,
                      'hosp_sigla': hosp_sigla,
                      'pacientes': pacientes,
                      'setores': setores_qs,
                      'pac_form': PacienteForm(),
                  })
