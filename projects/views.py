from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Project, CustomUser
from .forms import ProjectForm, CustomUserForm
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('project_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'registration/login.html', context)


def project_list(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()

    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects, 'form': form})

from .models import Step

def add_step(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        name = request.POST.get('step_name')
        status = request.POST.get('step_status')
        step = Step(name=name, status=status, project=project)
        step.save()
        project.update_status()
        return redirect('project_list')
    return redirect('project_list')


def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    project.delete()
    return redirect('project_list')
def delete_step(request, step_id):
    step = get_object_or_404(Step, id=step_id)
    project = step.project
    step.delete()
    project.update_status()
    return redirect('project_list')


def edit_project_status(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ["Not Started", "Incompleted", "Completed"]:
            project.status = new_status
            project.save()
            project.update_status()

    return redirect('project_list')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
def edit_step_status(request, step_id):
    step = get_object_or_404(Step, id=step_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ["Not Started", "In Progress", "Completed"]:
            step.status = new_status
            step.save()
            step.project.update_status()
    return redirect('project_list')

@login_required
def user_management(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    else:
        form = CustomUserForm()

    query = request.GET.get('search', '')
    if query:
        users = CustomUser.objects.filter(Q(username__icontains=query) | Q(study_id__icontains=query))
    else:
        users = CustomUser.objects.all()

    context = {
        'form': form,
        'users': users
    }

    return render(request, 'user_management.html', context)


def delete_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    return redirect('user_management')


