from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Project, CustomUser,Step
from .forms import ProjectForm, CustomUserForm
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta


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

@login_required
def project_list(request):
    topic_options = [
        "Living with memory loss, community resources and care coordination",
        "Progression of Alzheimer’s Disease and related dementias",
        "Legal and financial planning",
        "Managing independent activities of daily living (IADLs)",
        "Communication",
        "Driving safety",
        "Stress management",
        "Managing activities of daily living (ADLs)",
        "Care recipient wandering",
        "Care recipient aggression/repeated questioning",
        "Care recipient depression",
        "Caregiving transitions: legal issues, placement, hospice/end of life, bereavement",
        "Home safety"
    ]
    user_selected_topics = request.user.Topic.split('; ') if request.user.Topic else []


    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.week = form.cleaned_data['week']
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()

    if request.user.start_date:
        delta = datetime.now().date() - request.user.start_date
        current_week = delta.days // 7 + 1
    else:
        current_week = 1

    incomplete_projects = Project.objects.filter(
        user=request.user,
        status__in=["Not Started", "Incompleted"],
        week=current_week
    )
    projects = Project.objects.filter(user=request.user)



    context = {
        'form': form,
        'projects': projects,
        'incomplete_projects': incomplete_projects,
        'topic_options': topic_options,
        'user_selected_topics': user_selected_topics,
        'weeks': range(1, 11),
        'user_start_date': request.user.start_date
    }

    return render(request, 'projects/project_list.html', context)

def add_step(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        name = request.POST.get('step_name')
        status = request.POST.get('step_status')
        step = Step(name=name, status=status, project=project)
        step.save()
        project.update_status()
        return redirect('project_management')
    return redirect('project_management')


def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    project.delete()
    return redirect('project_management')
def delete_step(request, step_id):
    step = get_object_or_404(Step, id=step_id)
    project = step.project
    step.delete()
    project.update_status()
    return redirect('project_management')


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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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
@login_required
def project_management(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            form.save()
            return redirect('project_management')
    else:
        form = ProjectForm()

    projects = Project.objects.all()
    return render(request, 'project_management.html', {'form': form, 'projects': projects})


def delete_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    return redirect('user_management')


@login_required
@require_POST
def save_user_topics(request):
    user = request.user
    if user.start_date:
        delta = datetime.now().date() - user.start_date
        current_week = delta.days // 7 + 1
        if current_week not in [1, 2]:
            messages.error(request, "Topic Selection is not allowed at this time, please contact manager")
            return redirect('project_list')

    selected_topics = request.POST.getlist('topics')
    user.Topic = '; '.join(selected_topics) if selected_topics else ''
    user.save()
    messages.success(request, "Topics updated successfully!")
    return redirect('project_list')

@login_required
def update_user_start_date(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, pk=user_id)
        user.start_date = request.POST.get('start_date')
        user.save()
        #messages.success(request, "Start date updated successfully!")
    return redirect('user_management')
