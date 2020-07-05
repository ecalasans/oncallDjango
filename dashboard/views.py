from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from dashboard.models import Leito, Hospital, Setor, Medico, Paciente
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import MedicoForm, LeitoForm, PacienteForm
from django.contrib import messages
from django.http import JsonResponse
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

    # Seleção de setores do hospital do usuário
    setores = Setor.objects.filter(hospital_id=hosp_id).values('setor', 'pk', 'ativo')
    total_setores = Setor.objects.filter(hospital_id=hosp_id, ativo=True).count

    # Total de leitos do hospital do usuário
    total_leitos = Leito.objects.filter(hospital_id=hosp_id).count()

    # Situação dos leitos por setor(Ativos e Inativos)
    situacao_por_setor = {}
    for setor in setores:
        if not setor['ativo']:
            pass
        else:
            situacao = {}
            leitos_ativos = Leito.objects.filter(hospital_id=hosp_id, setor=setor['pk'], situacao='A') \
                .values('status').annotate(Count('status'))
            ativos_setor = Leito.objects.filter(hospital_id=hosp_id, setor=setor['pk'], situacao='A').count()
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

    #return JsonResponse({'status': status}, safe=False)