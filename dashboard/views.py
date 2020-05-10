from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from dashboard.models import Leito, Hospital,  Setor, Medico
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import MedicoForm
from django.contrib import messages
import datetime
import json

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
@login_required
def home(request):
    return render(request, 'dashboard/index.html')

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

            #Pega o hospital do usuário
            hospital = request.POST['select_hosp_cad']
            hosp_id = Medico.objects.get(hospital_id=hospital).hospital_id
            hosp_user = Hospital.objects.get(pk=hosp_id).nome

            #Seleção de setores do hospital do usuário
            setores = Setor.objects.filter(hospital_id=hosp_id).values('setor', 'pk')
            total_setores = Setor.objects.filter(hospital_id=hosp_id).count

            #Total de leitos do hospital do usuário
            total_leitos = Leito.objects.filter(hospital_id=hosp_id).count()

            #Situação dos leitos por setor(Ativos e Inativos)
            situacao_por_setor = {}
            for setor in setores:
                situacao = {}
                leitos_ativos = Leito.objects.filter(hospital_id=hosp_id, setor=setor['pk'], situacao='A')\
                    .values('status').annotate(Count('status'))
                ativos_setor = Leito.objects.filter(hospital_id=hosp_id, setor=setor['pk'], situacao='A').count()
                inativos_setor = Leito.objects.filter(hospital_id=hosp_id, setor=setor['pk'], situacao='D').count()

                for qset in leitos_ativos.values('status', 'status__count'):
                    situacao[qset['status']] = qset['status__count']
                    p = (qset['status__count'] / ativos_setor) * 100
                    situacao['porcentagem'] = p
                situacao['ativos'] = ativos_setor
                situacao['inativos'] = inativos_setor

                situacao_por_setor[setor['setor']] = situacao

            return render(request, 'dashboard/index.html',
                          context={'usuario': user,
                                   'primeiro': primeiro,
                                   'saudacao': saudacao,
                                   'hosp_user': hosp_user,
                                   'total_leitos': total_leitos,
                                   'setores': setores,
                                   'total_setores': total_setores})
        else:
            return render(request, 'dashboard/registration/login.html',
                          context={'form': AuthenticationForm(),
                                   'hospitais': hospitais,
                                   'error': 'Usuário não encontrado ou dados conflitantes!'})

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

def sysLogout(request):
    logout(request)
    return redirect('login')