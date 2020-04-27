
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from dashboard.models import Leito, Hospital,  Setor, Medico
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import MedicoForm
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
    else:
        # Autentica usuário com base nos dados recebidos
        user = authenticate(request, username=request.POST['user_login'], password=request.POST['pass_login'])

        #Verifica se o usuário existe
        if user is not None:
            # Faz o login
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'dashboard/registration/login.html',
                          context={'form': AuthenticationForm(),
                                   'hospitais': hospitais,
                                   'error': 'Usuário não encontrado ou dados conflitantes!'})

def signupUser(request):
    if request.method == 'GET':
        return render(request, 'dashboard/registration/login.html',
                      context={'form': MedicoForm(),
                               'error': 'Clique no link para fazer o cadastro!'})
    elif request.method == 'POST':
        form = MedicoForm()

        dados = request.POST.dict()

        form.username = dados['user_cad']
        form.first_name = dados['first_name_cad']
        form.last_name = dados['last_name_cad']
        form.email = dados['email_cad']
        form.password = dados['pass_cad']
        form.crm = dados['crm_cad']
        form.hospital = dados['select_hosp_cad']

        print(form.crm)
        print(form.username)

        # if form.is_valid():
        #     new_medico = form.save(commit=False)
        #
        #     new_medico.username = form.cleaned_data['username']
        #     new_medico.first_name = form.cleaned_data['first_name']
        #     new_medico.last_name = form.cleaned_data['last_name']
        #     new_medico.email = form.cleaned_data['email']
        #     new_medico.crm = form.cleaned_data['crm']
        #     new_medico.set_password(form.cleaned_data['password'])
        #
        #     new_medico.save()
        #
        #     new_medico.hospital.set(form.cleaned_data['hospital'])
        #     new_medico.save()
        #
        #     return redirect('home')
        # else:
        #     print(form.errors)
    return render(request, 'dashboard/registration/login.html')
