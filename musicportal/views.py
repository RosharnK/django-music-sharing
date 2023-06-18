from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Musicdata
from django.db.models import Q
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MusicFileForm

# Create your views here.


def registerpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

    context = {'form': form}
    return render(request, 'musicportal/register.html', context)


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'username OR  password is incorrect')

        context = {}
        return render(request, 'musicportal/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def upload_music(request):
    if request.method == 'POST':
        form = MusicFileForm(request.POST, request.FILES)
        if form.is_valid():
            music_file = form.save(commit=False)
            music_file.user = request.user
            music_file.save()
            return redirect('home')
    else:
        form = MusicFileForm()
    return render(request, 'music/home.html', {'form': form})


@login_required(login_url='login')
def home(request):
    user = request.user
    music_files = Musicdata.objects.filter(Q(visibility='public') | Q(
        user=user) | Q(visibility='protected', access_emails__contains=user.email))
    return render(request, 'musicportal/home.html', {'music_files': music_files})
