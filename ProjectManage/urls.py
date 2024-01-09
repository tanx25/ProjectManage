"""ProjectManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from projects import views
from projects.views import project_list, delete_project, register, add_step, edit_step_status, edit_project_status
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', project_list, name='project_list'),
    path('project_management/', views.project_management, name='project_management'),

    path('add_step/<int:project_id>/', add_step, name='add_step'),
    path('delete/<int:pk>/', delete_project, name='delete_project'),
    path('edit_step_status/<int:step_id>/', edit_step_status, name='edit_step_status'),
    #path('edit_status/<int:pk>/', edit_project_status, name='edit_project_status'),
    path('', views.login_view, name='login_view'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('delete_step/<int:step_id>/', views.delete_step, name='delete_step'),
    path('users/', views.user_management, name='user_management'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('save_user_topics/', views.save_user_topics, name='save_user_topics'),
    path('update_user_start_date/<int:user_id>/', views.update_user_start_date, name='update_user_start_date'),



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

